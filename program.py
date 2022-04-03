import pandas as pd
import json
import oauth2
import sys


# Download media tracking file as .xlsx and convert to .csv
read_file = pd.read_excel('data/2021 GW Media Tracking.xlsx', sheet_name='media_tracking', engine='openpyxl')

# Extract relevant content (master id from ID column of rows labeled 'Album')
albums = read_file[read_file["Medium"]=="Album"]
albums["master_id"] = 'm' + albums["Standardised ID"].str.extract(r'\/([0-9]{6,7})-')

# Create tidier df with just the relevant info
albums = albums.loc[:,["Num", "Title", "Creator/Season", "Date Started", "Date Finished","Days", "Month", "master_id"]]
print(albums.head())

# 1. Get info (Genre, Release Year, Album Cover) from API using master id. 
test_id = albums.iloc[0]["master_id"]

# credentials
json_file = open("discogs_auths.json")
secrets = json.load(json_file)
json_file.close()

# create oauth Consumer and Client objects using
consumer = oauth2.Consumer(secrets["consumer_key"], secrets["consumer_secret"])

token = oauth2.Token(key=secrets['oauth_token'], secret=secrets['oauth_token_secret'])
client = oauth2.Client(consumer, token)

print(f'master id: "{test_id}".')
# resp, content = client.request(f'https://api.discogs.com/masters/2452996', headers={'User-Agent': secrets['user_agent']})

resp, content = client.request('https://api.discogs.com/database/search?release_title=House+For+All&artist=Blunted+Dummies', headers={'User-Agent':secrets['user_agent']})

if resp['status'] != '200':
    sys.exit('Invalid API response {0}.'.format(resp['status']))

master = json.loads(content.decode('utf-8'))

print(master)