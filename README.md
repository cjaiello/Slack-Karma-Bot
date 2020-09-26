# Slack Karma Bot
### By Christina

## Technologies Used
Python, Flask, PostgreSQL

## Description
Simple slack karma bot running on Heroku.

## Usage: 
@christina_aiello++ or @christina_aiello-- (or +++, ++++, etc)

![How to Use Karma Bot](https://github.com/cjaiello/Slack-Karma-Bot/blob/master/karma-bot-usage.gif)


## Local Setup
(This is long, but most of it is what you'd do to set up any Slack bot.)

Fork the Repository
* Fork this repository so it's in your account
* Clone it to your machine using `git clone`
* `cd Slack-Karma-Bot`

Make Heroku app
* Install the Heroku CLI (command line interface) https://devcenter.heroku.com/articles/heroku-cli
* Go to https://dashboard.heroku.com/apps (register if you haven't)
* Click `New` and then `Create New App`
* Give it a name and click `Create`
* You will be dropped onto the `Deploy` tab
* In the `Deployment method` section, click `GitHub` `Connect to Github`
* Choose your repository
* Click `Enable Automatic Deploys`
* Go to the Resources tab
* In the `Add-Ons` section, type in `Heroku Postgres` and install the `Hobby Dev - Free` version
* Go back to the `Settings` tab and click `Reveal config vars` again
* The new DATABASE_URL has been added for you!


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
* Go back to the code you cloned onto your computer.
* Open `app.py`
* Go to `def karma():` and uncomment this line: `return request.json['challenge']`
* Save and push to git
* Go back to the Slack `Event Subscriptions` page for your app (URL example: https://api.slack.com/apps/A01BFFWKQ4T/event-subscriptions?)
* Click the `Retry` button
* Once it says your url is verified, go back and comment out that `return request.json['challenge']` line again in `app.py`'s `karma` function
* Click on `Subscribe to bot events` and select `message.channels` and `message.groups`. This will let your bot listen for messages.
* Click the green `Save Changes` button
* Now you'll see a message in a yellow box at the top of the screen that says, "You’ve changed the permission scopes your app uses. Please reinstall your app for these changes to take effect (and if your app is listed in the Slack App Directory, you’ll need to resubmit it as well)." Click on `Reinstall your app` and reinstall it.
* Go to the #general channel and tag the bot, example: 
```
christinajaiello  9:56 PM
@Name Your App
```
* After tagging the bot, you'll be asked to invite it to the channel. Invite it.
* Go back to the Heroku `Resources` tab (Ex: https://dashboard.heroku.com/apps/christinastest/resources)
* Click on your database
* At the top of the page you're brought to, copy the name (Example: `postgresql-cubed-27245`)
* Open up a new terminal and run `heroku pg:psql postgresql-cubed-27245 --app christinastest`, where `postgresql-cubed-27245` is the name of your database and `christinastest` is the name of your app
* Now that you're connected to your database, run `CREATE TABLE users (id SERIAL PRIMARY KEY, username varchar(128), karma int);` to create your table
* Finally, give yourself karma via `@username ++` and watch your bot respond!
* If you're having issues and need to debug, run `heroku logs --tail --app christinastest` in a terminal window, where `christinastest` is the name of your app on heroku
