import pandas as pd
import re
import requests

# Download media tracking file as .xlsx and convert to .csv
read_file = pd.read_excel('data/2021 GW Media Tracking.xlsx', sheet_name='media_tracking', engine='openpyxl')
# read_file.to_csv('data/2021 GW Media Tracking.csv', index = None, header=True)

# print(read_file.head())

# Extract relevant content (master id from ID column of rows labeled 'Album')
albums = read_file[read_file["Medium"]=="Album"]
albums["master_id"] = 'm' + albums["Standardised ID"].str.extract(r'\/([0-9]{6,7})-')

# Create tidier df with just the relevant info
albums = albums.loc[:,["Num", "Title", "Creator/Season", "Date Started", "Date Finished","Days", "Month", "master_id"]]
print(albums.head())

# 1. Get info (Genre, Release Year, Album Cover) from API using master id. 
test_id = albums.iloc[0]["master_id"]
# print(test_id)
response = requests.get(f'https://api.discogs.com/database/search?q=Nirvana&token=abcxyz123456 --user-agent "allmusic-artist-association/1.0 +https://github.com/geraldwogan/allmusic-artist-association"')
print(response.status_code)
print(response.json())

