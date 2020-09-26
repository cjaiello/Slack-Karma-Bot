# Slack Karma Bot
### By Christina

## Technologies Used
Python, Flask, PostgreSQL

## Description
Simple slack karma bot running on Heroku.

## Usage: 
@christina_aiello++ or @christina_aiello-- (or +++, ++++, etc)

![How to Use Karma Bot](https://github.com/cjaiello/Slack-Karma-Bot/blob/master/static/karma-bot-usage.gif)


## Local Setup
(This is long, but most of it is what you'd do to set up any Slack bot.)

### Fork the Repository
* Fork this repository so it's in your account
![Fork repository](https://github.com/cjaiello/Slack-Karma-Bot/blob/master/static/fork-repository.png)
* Clone it to your machine using `git clone` (More help available at https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository)
* `cd Slack-Karma-Bot` to get into the directory of the code you just cloned

### Make Heroku app
* Install the Heroku CLI (command line interface) https://devcenter.heroku.com/articles/heroku-cli
* Go to https://dashboard.heroku.com/apps (register if you haven't)
* Click `New` and then `Create New App`
* Give it a name and click `Create`
* You will be dropped onto the `Deploy` tab. Note your app name and how to access your app via web browser:
![Your App Name](https://github.com/cjaiello/Slack-Karma-Bot/blob/master/static/this-is-your-app-name.png)
* In the `Deployment method` section, click `GitHub` `Connect to Github`
![Connect to Github](https://github.com/cjaiello/Slack-Karma-Bot/blob/master/static/deployment-method-github.png)
* Choose your repository
* Click `Enable Automatic Deploys`. Now, anytime you push to Github, your code will be automatically deployed to Heroku!
* Go to the Resources tab
* In the `Add-Ons` section, type in `Heroku Postgres` and install the `Hobby Dev - Free` version
![Install Postgres](https://github.com/cjaiello/Slack-Karma-Bot/blob/master/static/database-heroku-install-postgres.png)
* Go back to the `Settings` tab and click `Reveal config vars` again
* The new `DATABASE_URL` config var (environment variable) has been added for you! Now when you access `os.environ["DATABASE_URL"]` in the Slack Karma Bot app code, the application will pull in the value of that new `DATABASE_URL`
![Postgres](https://github.com/cjaiello/Slack-Karma-Bot/blob/master/static/config-vars-database-url.png)


### Make Slack Workspace and Slack Bot
* Make a Slack workspace (They're free, don't worry!) at https://slack.com/create
![Create Slack App](https://github.com/cjaiello/Slack-Karma-Bot/blob/master/static/create-slack-app.png)
* Go to `https://api.slack.com/apps`
* Make your app and attach it to your workspace you just made
* On the Basic Information page, go to `Permissions`
* Scroll down to `Bot Token Scopes`
* Add: app_mentions:read, channels:history, channels:join, channels:read, chat:write, chat:write.customize, chat:write.public, groups:history, incoming-webhook, users.profile:read, users:read
* Now scroll up and click `Install App to Workspace`
![Install App to Workspace](https://github.com/cjaiello/Slack-Karma-Bot/blob/master/static/permissions-tokens-access-token-install-to-workspace.png)
* You now have a bot token! 
![Bot Token](https://github.com/cjaiello/Slack-Karma-Bot/blob/master/static/permissions-tokens-access-token-to-copy.png)
* On the Heroku Settings tab `https://dashboard.heroku.com/apps/christinastest/settings` (or whatever your URL is, which will have something other than `christinastest` and will instead have your app's name in it), go to `Reveal config vars` again and add the Slackbot token: `SLACK_BOT_TOKEN` and value is whatever your value is
![Slackbot Token](https://github.com/cjaiello/Slack-Karma-Bot/blob/master/static/config-vars-slack-bot-token.png)
* Back on the Basic Information page in Slack when managing your new Slack app, go to `Event Subscriptions`
* Click the switch to turn event subscriptions on
![Event Subscriptions](https://github.com/cjaiello/Slack-Karma-Bot/blob/master/static/event-subscriptions-enable-events.png)
* Paste in the URL in the box: `https://christinastest.herokuapp.com/karma` (but replace `christinastest` with whatever you named your app)

![Event Subscriptions](https://github.com/cjaiello/Slack-Karma-Bot/blob/master/static/event-subscriptions-enable-events-endpoint-unverified.png)
* Go back to the code you cloned onto your computer.
* Open `app.py`
* Go to `def karma():` and uncomment this line: `return request.json['challenge']`
![Event Subscriptions](https://github.com/cjaiello/Slack-Karma-Bot/blob/master/static/event-subscriptions-enable-events-line-to-uncomment.png)
* Save and push to git
* Wait for it to deploy (takes... ~1min, sometimes 30 seconds?). You can monitor the build and deploy by going onto the Heroku website, going to your app, and clicking on the "Activity" tab
![Monitor Build and Deploy](https://github.com/cjaiello/Slack-Karma-Bot/blob/master/static/monitor-build-and-deploy.png)
* Go back to the Slack `Event Subscriptions` page for your app (URL example: https://api.slack.com/apps/A01BFFWKQ4T/event-subscriptions?)
* Click the `Retry` button to the right of the URL you pasted in to verify

![Event Subscriptions](https://github.com/cjaiello/Slack-Karma-Bot/blob/master/static/event-subscriptions-enable-events-endpoint-unverified-retry-button.png)
* When it succeeds, you'll see this:
![Event Subscriptions](https://github.com/cjaiello/Slack-Karma-Bot/blob/master/static/event-subscriptions-enable-events-endpoint-verified.png)
* Once it says your url is verified, go back and comment out (or just remove) that `return request.json['challenge']` line again in `app.py`'s `karma` function
* Scroll down and click on `Subscribe to bot events`, and then add `app_mention`, `message.channels`, and `message.groups`. This will let your bot listen for messages.
![Event Subscriptions](https://github.com/cjaiello/Slack-Karma-Bot/blob/master/static/event-subscriptions-subscribe-to-bot-events.png)
* Click the green `Save Changes` button at the bottom right of the page
* Now you'll see a message in a yellow box at the top of the screen that says, "You’ve changed the permission scopes your app uses. Please reinstall your app for these changes to take effect (and if your app is listed in the Slack App Directory, you’ll need to resubmit it as well)." Click on `Reinstall your app` and reinstall it.

### Final Setup Steps
* Go to the #general channel in Slack and tag the bot, example: 
```
your-username  9:56 PM
@Name Your App
```
* After tagging the bot, you'll be asked to invite it to the channel. Invite it.
* Make a channel called `karma_bot_log` in Slack
* Go back to the Heroku `Resources` tab (Ex: https://dashboard.heroku.com/apps/christinastest/resources)
* Click on your database
* At the top of the page you're brought to, copy the name (Example: `postgresql-cubed-27245`)
* Open up a new terminal and run `heroku pg:psql postgresql-cubed-27245 --app christinastest`, where `postgresql-cubed-27245` is the name of your database and `christinastest` is the name of your app
![Get Database Name](https://github.com/cjaiello/Slack-Karma-Bot/blob/master/static/get-database-name.png)
* Now that you're connected to your database, run `CREATE TABLE users (id SERIAL PRIMARY KEY, username varchar(128), karma int);` to create your table
* Finally, go back to Slack, give yourself karma via `@username ++`, and watch your bot respond!

### Debugging
* If you're having issues and need to debug, run `heroku logs --tail --app christinastest` in a terminal window, where `christinastest` is the name of your app on heroku
