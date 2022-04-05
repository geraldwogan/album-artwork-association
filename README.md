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

## Git Initiliazation
https://gist.github.com/alexpchin/102854243cd066f8b88e

1. Create directory on local
1. Create identical repo on remote (GitHub)
1. Follow these commands
```
$ git init
$ git add README.md
$ git commit -m "first commit"
$ git remote add origin https://github.com/geraldwogan/album-artwork-association.git
$ git push --set-upstream origin master
```

## Virtual Env init
```
$ python -m venv venv
$ echo /venv/ >> .gitignore
$ venv\scripts\activate
(venv) $ pip install ...
(venv) $ deactivate
$ pip freeze > requirements.txt (Run this each time you install a new package)
```

## Using APIs in Python
- https://www.dataquest.io/blog/python-api-tutorial/
- https://www.discogs.com/developers/#
- More info: get_discog_auth.py file
