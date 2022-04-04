import pandas as pd
import json
import oauth2
import sys
import requests
import re

# Download media tracking file as .xlsx
read_file = pd.read_excel('data/2021 GW Media Tracking.xlsx', sheet_name='media_tracking', engine='openpyxl')

def data_cleaning(read_file):
    
    # Extract relevant content (master id from ID column of rows labeled 'Album')
    albums = read_file[read_file["Medium"]=="Album"]
    albums["master_id"] = albums["Standardised ID"].str.extract(r'\/([0-9]{6,7})-')

    # Create 'search friendly' columns for artist and album
    albums['search_artist'] = albums['Creator/Season'].str.replace(' ', '+')
    albums['search_album'] = albums['Title'].str.replace(' ', '+')

    # Create tidy df with just the relevant info
    tidy_albums = albums.loc[:,["Num", "Title", "Creator/Season", "Date Started", "Date Finished","Days", "Month", "master_id", "search_artist", "search_album"]]

    print(tidy_albums.head())

    return tidy_albums

albums = data_cleaning(read_file)

# test values
test_id = albums.iloc[0]["master_id"]
test_search_artist = albums.iloc[0]["search_artist"]
test_search_album = albums.iloc[0]["search_album"]
print(f'test_id: "{test_id}".')
print(f'test_search_artist: "{test_search_artist}"')
print(f'test_search_album: "{test_search_album}"')

# credentials
json_file = open("discogs_auths.json")
secrets = json.load(json_file)
json_file.close()

# create oauth token, Consumer and Client objects needed for use with the Discogs API.
consumer = oauth2.Consumer(secrets["consumer_key"], secrets["consumer_secret"])
token = oauth2.Token(key=secrets['oauth_token'], secret=secrets['oauth_token_secret'])
client = oauth2.Client(consumer, token)

# resp, content = client.request(f'https://api.discogs.com/masters/2452996', headers={'User-Agent': secrets['user_agent']})

resp, content = client.request(f'https://api.discogs.com/database/search?release_title={test_search_album}&artist={test_search_artist}', headers={'User-Agent':secrets['user_agent']})

if resp['status'] != '200':
    sys.exit('Invalid API response {0}.'.format(resp['status']))

releases = json.loads(content.decode('utf-8'))

# print(releases['results'][0])

# Get master release
master = ''
for release in releases['results']:
    if release['type'] == 'master':
        master = release
# print(master)

# Get info (Genre, Release Year, Album Cover) from API
genres = master['genre']
release_year = master['year']
print('genres:', genres)
print('release_year:', release_year)

album_cover = master['cover_image']
try:
    # urllib.URLopener.version = secrets['user_agent']
    # request.urlretrieve(album_cover, test_id+'album_cover')

    headers={'user-agent': secrets['user_agent']}
    r=requests.get(album_cover, headers=headers)

    img_type = re.findall(r'[^.]+$', album_cover)[0]
    with open(f"resources/{test_id}_album_cover.{img_type}", 'wb') as f:
        f.write(r.content)
    print(f"{test_id}_album_cover.{img_type} saved successfully in resources directory.")

except Exception as e:
    sys.exit(f'Unable to download image {album_cover}, error {e}')