# Using Artist + Album Name from Excel records and getting link (+ data?) from music database

- discogs.com -> https://www.discogs.com/master/1127593-Loyle-Carner-Yesterdays-Gone
discogs.com is a music database that has an api which can use to get images, release year, etc. of an album. 
https://www.discogs.com/developers/#

## Git Initiliazation
https://gist.github.com/alexpchin/102854243cd066f8b88e

1. Create directory on local
1. Create identical repo on remote (GitHub)
1. Follow these commands

```
$ git init
$ git add README.md
$ git commit -m "first commit"
$ git remote add origin https://github.com/geraldwogan/allmusic-artist-association.git
$ git push --set-upstream origin master
```

## Virtual Env init
$ python -m venv venv
$ echo /venv/ >> .gitignore
$ venv\scripts\activate
(venv) $ pip install ...
(venv) $ deactivate
$ pip freeze > requirements.txt (Run this each time you install a new package)


## Brief outline
1. Download media tracking file as xlsx and convert to .csv
1. Extract relevant content (master id from ID column of rows labeled 'Album')
1. Get info (Genre, Release Year, Album Cover) from API using master id. 
1. Add album data to excel file as a seperate sheet.

