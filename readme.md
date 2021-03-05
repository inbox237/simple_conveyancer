# Simple Conveyancer

## Description

This Flask REST API is an extension to the Spotify REST API.

The extension includes the addition of new tables and relationships including two tables that formulate both seasonal-based discount suggestions or seasonal-based playlist suggestions.

The endpoints for this project are located in docs/endpoints.md.

The GitHub repository for this can be found here: https://github.com/inbox237/T3A3


![erd](/docs/erd.png)

## Instructions

The instructions for Ubuntu 20:

Update repositories on Ubuntu: ```sudo apt-get update```

Clone GitHub repository: ```git clone https://github.com/inbox237/SC ```

Install python virtual environment: ```cd T3A3```

Install python virtual environment: ```sudo apt-get install python3-venv```

Create virtual environment: ```python3 -m venv venv```

Activate the virtual environment ```source venv/bin/activate```

Install pip: ```python -m pip install --upgrade pip```

Install modules from requirements.txt: ```pip install -r requirements.txt```

To connect to the database locally, please fill in the "exampleenv" file like this example, then rename the file to ".env":
DB_URI="postgresql+psycopg2://postgres:coder@13.211.86.126/simple_conveyancer"
FLASK_APP=main.py
FLASK_ENV=development
JWT_SECRET_KEY = "duck"
AWS_ACCESS_KEY_ID=1
AWS_SECRET_ACCESS_KEY=1
AWS_S3_BUCKET=1


**To create the database and seed all values with one command, run ONLY the following command:**
Note: This will complete all steps required to run the program including starting flask and opening a local browser.

```flask db-custom start``` (to complete all steps in order)

**Alternatively the following commands can be run separately:**

```flask db-custom drop``` (If there are any tables in the database previously)

```flask db upgrade``` (to add the tables in the migrations directory)

```flask db-custom seed``` (to seed the database)


Note: seeding includes populating these tables:
1. 10 users in Users, 
2. 10 artists in Artists,
3. 10 albums in Albums,
4. 10 tracks in Tracks,
5. 10 playlists in Playlists,
6. Associations in all 4 joint tables,
7. 4 seasonal playlists in SeasonalP,
8. 4 seasonal discount offers in SeasonalD


The front end consists of the following endpoints:
```/artists/``` which shows a list of artists
```/albums/``` which shows a list of albums
```/tracks/``` which shows a list of tracks
```/playlists/``` which shows a list of playlists

