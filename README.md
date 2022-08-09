# Using Artist + Album name to get album cover, genre, release year from API.

- discogs.com is a music database that has an api which we can use to get images, release year, etc. of an album. (https://www.discogs.com/master/1127593-Loyle-Carner-Yesterdays-Gone)

## Brief outline
1. Download media tracking file as xlsx
1. Extract relevant content (master id from ID column of rows labeled 'Album')
1. Get info (Genre, Release Year, Album Cover) from API.

### Excel file format
|Title|Creator/Season|
|-|-|
|The Green Mile|Frank Darabont|
|Jurassic Park|Steven Spielberg|
|Home Alone|Chris Columbus|
