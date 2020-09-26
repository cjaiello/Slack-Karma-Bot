# Slack Karma Bot
### By Christina

## Technologies Used
Python, Flask, PostgreSQL

## Description
Simple slack karma bot running on Heroku.

## Local Setup
* `git clone git@github.com:cjaiello/Slack-Karma-Bot.git`
* `cd Slack-Karma-Bot`
* Make sure you have the latest Python, version 3.8.6, and install it if you don't: https://www.python.org/downloads/release/python-386/
* `pip install -r requirements.txt`
* `export FLASK_APP=app.py`
* You'll now need the SLACK_BOT_TOKEN and a DATABASE_URL for the test workspace for this project. Email me (cjaiello@wpi.edu) for the token. Then you can run `export SLACK_BOT_TOKEN=TOKEN-I-GIVE-YOU` and `export DATABASE_URL=URL-I-GIVE-YOU`
* `python -m flask run`

## Usage: 
@christina_aiello++ or @christina_aiello-- (or +++, ++++, etc)

![How to Use Karma Bot](https://github.com/cjaiello/Slack-Karma-Bot/blob/master/karma-bot-usage.gif)
