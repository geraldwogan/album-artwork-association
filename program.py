import json
import re
import sys

import oauth2
import pandas as pd
import requests

def data_cleaning(all_media):
    # Extract relevant content (master id from ID column of rows labeled 'Album')
    albums = all_media[all_media["Medium"]=="Album"].copy()
    albums.loc[:,"master_id"] = albums["Standardised ID"].str.extract(r'\/([0-9]{6,7})-')

    # Create 'search friendly' columns for artist and album
    albums.loc[:,'search_artist'] = albums['Creator/Season'].str.replace(' ', '+')
    albums.loc[:,'search_album'] = albums['Title'].str.replace(' ', '+')

    # Create tidy df with just the relevant info
    tidy_albums = albums.loc[:,["Num", "Title", "Creator/Season", "Date Started", "Date Finished","Days", "Month", "master_id", "search_artist", "search_album"]]

    print(tidy_albums.head())

    return tidy_albums

def get_secrets():
    # credentials
    json_file = open("resources/discog_auths.json")
    secrets = json.load(json_file)
    json_file.close()

    return secrets

def setup_auth_client():
    # create oauth Token, Consumer and Client objects needed for use with the Discogs API.
    consumer = oauth2.Consumer(secrets["consumer_key"], secrets["consumer_secret"])
    token = oauth2.Token(key=secrets['oauth_token'], secret=secrets['oauth_token_secret'])
    client = oauth2.Client(consumer, token)

    return client

def get_data_from_api(album, client, secrets):
    # search query
    print(f'Searching Discogs API for ... {album["Creator/Season"]} - {album["Title"]}')

    # API endpoint 'master'
    # resp, content = client.request(f'https://api.discogs.com/masters/{album["master_id"]}', headers={'User-Agent': secrets['user_agent']})

    # API endpoint 'search'
    resp, content = client.request(f'https://api.discogs.com/database/search?release_title={album["search_album"]}&artist={album["search_artist"]}&type=master', headers={'User-Agent':secrets['user_agent']})

    if resp['status'] != '200':
        sys.exit('Invalid API response {0}.'.format(resp['status']))
    
    return content

def get_master_from_reponse(content):
    releases = json.loads(content.decode('utf-8'))

    master = releases['results'][0]

    return master

def get_values_from_response(album, content):

    master = get_master_from_reponse(content)

    # Get info (Genre, Release Year, Album Cover) from API
    album['Genres'] = master['genre']
    album['Release Year'] = master['year']
    img_type = re.findall(r'[^.]+$',  master['cover_image'])[0] # Get file type of image (.jpeg, .png, etc.)
    album['Album Cover'] = f"album_covers/{album['master_id']}.{img_type}"

    try:
        secrets = get_secrets()
        headers = {'user-agent': secrets['user_agent']}
        req = requests.get(master['cover_image'], headers=headers)

        with open(album['Album Cover'], 'wb') as f:
            f.write(req.content)

        print(f"Image download successful -> {album['Album Cover']}")

    except Exception as e:
        album['Album Cover'] = 'Download Failure'
        sys.exit(f'Unable to download image {master["cover_image"]}, error {e}')

    return album

albums_final = []
all_media = pd.read_excel('data/2021 GW Media Tracking.xlsx', sheet_name='media_tracking', engine='openpyxl')
albums = data_cleaning(all_media)

secrets = get_secrets()
client = setup_auth_client()

# for idx, album in albums.iterrows():
#     print(album)
#     content = get_data_from_api(album, client, secrets)
#     albums_final.append(get_values_from_response(album, content))

album = albums.iloc[0,:].copy()
content = get_data_from_api(album, client, secrets)
albums_final.append(get_values_from_response(album, content))

album = albums.iloc[1,:].copy()
content = get_data_from_api(album, client, secrets)
albums_final.append(get_values_from_response(album, content))

df = pd.DataFrame(albums_final)

print(df)