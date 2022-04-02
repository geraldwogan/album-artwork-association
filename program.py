import pandas as pd
import requests
import oauth2
import sys
from urllib import request
from urllib.parse import parse_qsl
from urllib.parse import urlparse
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

# Consumer Key & Secret from https://www.discogs.com/settings/developers
parameters = {
    "Consumer Key": "MyVgXQbTbpSHOQHuqWGL",
    "Consumer Secret": "mQrzxHuAPZQMOQiqGWTboVAPWUamxrqJ"
} 

consumer_key = 'MyVgXQbTbpSHOQHuqWGL'
consumer_secret = 'mQrzxHuAPZQMOQiqGWTboVAPWUamxrqJ'
request_token_url = 'https://api.discogs.com/oauth/request_token'
authorize_url = 'https://www.discogs.com/oauth/authorize'
access_token_url = 'https://api.discogs.com/oauth/access_token'
user_agent = 'album-artwork-association/1.0'

# create oauth Consumer and Client objects using
consumer = oauth2.Consumer(consumer_key, consumer_secret)
client = oauth2.Client(consumer)

resp, content = client.request(request_token_url, 'POST', headers={'User-Agent': user_agent})

if resp['status'] != '200':
    sys.exit('Invalid response {0}.'.format(resp['status']))

request_token = dict(parse_qsl(content.decode('utf-8')))

print(' == Request Token == ')
print(f'    * oauth_token        = {request_token["oauth_token"]}')
print(f'    * oauth_token_secret = {request_token["oauth_token_secret"]}')
print()

print(f'Please browse to the following URL {authorize_url}?oauth_token={request_token["oauth_token"]}')


print(f'Please browse to the following URL {authorize_url}?oauth_token={request_token["oauth_token"]}')

# Waiting for user input
accepted = 'n'
while accepted.lower() == 'n':
    print()
    accepted = input(f'Have you authorized me at {authorize_url}?oauth_token={request_token["oauth_token"]} [y/n] :')

oauth_verifier = input('Verification code : ')

token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
token.set_verifier(oauth_verifier)
client = oauth2.Client(consumer, token)

resp, content = client.request(access_token_url, 'POST', headers={'User-Agent': user_agent})

access_token = dict(parse_qsl(content.decode('utf-8')))

print(' == Access Token ==')
print(f'    * oauth_token        = {access_token["oauth_token"]}')
print(f'    * oauth_token_secret = {access_token["oauth_token_secret"]}')
print(' Authentication complete. Future requests must be signed with the above tokens.')
print()




response = requests.get(f'http://api.discogs.com/oauth/request_token?key=MyVgXQbTbpSHOQHuqWGL&secret=mQrzxHuAPZQMOQiqGWTboVAPWUamxrqJ --user-agent "album-artwork-association/1.0 +https://github.com/geraldwogan/album-artwork-association"') # failing currently
print(response.status_code)
print(response.json())
