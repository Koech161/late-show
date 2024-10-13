# The Late Show

A flask application that manages shows, guests and appearance .

# Features

- Get all episode details.
- Get episode by their id.
- Get guest details.
- Add appearances
- Delete appearances

# How to install and run the project

- Install Python 3.12  or higher
- git clone git@github.com:Koech161/late-show.git  to your local enivorment
- Activate virtual enviroment:
    pipenv install
    pipenv shell
- cd to server
- Already done migration,  no need to run again:   
        - flask db init
        - flask db migrate -m 'initial migration'
        - flask db upgrade
- Populate  database:
     python seed.py
- Run the applications
     python app.py

# API Endpoints
- GET  /episodes - Get a list of episodes.
- GET /episodes/<int:id> - GET a specific episode by ID.
- DELETE /episodes/<int:id> - Remove episode from database
- GET /guests - Get a list of guests
- POST /appearances - Add a new appearnce to the database

