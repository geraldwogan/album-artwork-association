import pandas as pd
import json
import oauth2
import sys
import requests
import re

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
    json_file = open("discogs_auths.json")
    secrets = json.load(json_file)
    json_file.close()
    return secrets

def setup_auth_client():
    # create oauth token, Consumer and Client objects needed for use with the Discogs API.
    consumer = oauth2.Consumer(secrets["consumer_key"], secrets["consumer_secret"])
    token = oauth2.Token(key=secrets['oauth_token'], secret=secrets['oauth_token_secret'])
    client = oauth2.Client(consumer, token)

    return client

def get_data_from_api(album, client, secrets):
    # values
    print(f'search_album: {album["Title"]}')
    print(f'search_artist: {album["Creator/Season"]}')

    # API endpoint 'master'
    resp, content = client.request(f'https://api.discogs.com/masters/2452996', headers={'User-Agent': secrets['user_agent']})

    # API endpoint 'search'
    resp, content = client.request(f'https://api.discogs.com/database/search?release_title={album["search_album"]}&artist={album["search_artist"]}&type=master', headers={'User-Agent':secrets['user_agent']})

    if resp['status'] != '200':
        sys.exit('Invalid API response {0}.'.format(resp['status']))
    
    return content

def format_data(album, content):

    releases = json.loads(content.decode('utf-8'))

    master = releases['results'][0]

    # Get info (Genre, Release Year, Album Cover) from API
    album['genres'] = master['genre']
    album['release_year'] = master['year']

    try:
        secrets = get_secrets()

        img_type = re.findall(r'[^.]+$',  master['cover_image'])[0] # Get file type of image (.jpeg, .png, etc.)
        album['album_cover'] = f"resources/{album['master_id']}_album_cover.{img_type}"

        headers = {'user-agent': secrets['user_agent']}
        r = requests.get( master['cover_image'], headers=headers)

        with open(album['album_cover'], 'wb') as f:
            f.write(r.content)

        print(f"Image downloaded successfully to -> {album['album_cover']}")

    except Exception as e:
        sys.exit(f'Unable to download image {master["cover_image"]}, error {e}')

    return album

albums_final = []
all_media = pd.read_excel('data/2021 GW Media Tracking.xlsx', sheet_name='media_tracking', engine='openpyxl')
albums = data_cleaning(all_media)

secrets = get_secrets()
client = setup_auth_client()

album = albums.iloc[0,:].copy()
content = get_data_from_api(album, client, secrets)
albums_final.append(format_data(album, content))

album = albums.iloc[1,:].copy()
content = get_data_from_api(album, client, secrets)
albums_final.append(format_data(album, content))

df = pd.DataFrame(albums_final)

print(df)