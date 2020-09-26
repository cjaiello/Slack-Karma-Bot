# Slack Karma Bot
### By Christina

## Technologies Used
Python, Flask, PostgreSQL

## Description
Simple slack karma bot running on Heroku.

## Local Setup

Make Slack Workspace and Slack Bot
* Make a Slack workspace (They're free, don't worry!)
* Go to `https://api.slack.com/apps`
* Make your app and attach it to your workspace 
* On the Basic Information page and then go to `Permissions`
* Scroll down to `Bot Token Scopes`
* Add: app_mentions:read, channels:history, channels:join, channels:read, chat:write, chat:write.customize, chat:write.public, groups:history, incoming-webhook, users.profile:read, users:read
* Now scroll up and click `Install App to Workspace`
* You now have a bot token! On `https://dashboard.heroku.com/apps/christinastest/settings` (or whatever your URL is), go to `Reveal config vars` again and add the Slackbot token: SLACK_BOT_TOKEN and value is whatever your value is
* Back on the Basic Information page, go to `Event Subscriptions`
* Click the switch to turn event subscriptions on
* Paste in the URL: `https://christinastest.herokuapp.com/karma` (but replace christinastest with whatever you named your app)
* In `Subscribe to bot events` select `messages.channel` and `messages.group`. This will let your bot listen for messages.
* In 

Fork the Repository
* Fork this repository so it's in your account
* Clone it to your machine using `git clone`
* `cd Slack-Karma-Bot`
* Open `app.py`
* Go to `def karma():` and uncomment this line: `return request.json['challenge']`
* Save and push to git

Make Heroku app
* Go to https://dashboard.heroku.com/apps (register if you haven't)
* Click `New` and then `Create New App`
* Give it a name and click `Create`
* You will be dropped onto the `Deploy` tab
* In the `Deployment method` section, click `GitHub` `Connect to Github`
* Choose your repository
* Click `Enable Automatic Deploys`
* Go to the `Settings` tab
* Scroll down a bit to `Config Vars`
* Click `Reveal config vars`
* Add your SLACK_BOT_TOKEN and its value
* Go to the Resources tab
* In the `Add-Ons` section, type in `Heroku Postgres` and install the `Hobby Dev - Free` version
* Go back to the `Settings` tab and click `Reveal config vars` again
* The new DATABASE_URL has been added for you!

## Usage: 
@christina_aiello++ or @christina_aiello-- (or +++, ++++, etc)

![How to Use Karma Bot](https://github.com/cjaiello/Slack-Karma-Bot/blob/master/karma-bot-usage.gif)
