# Karma Bot by Christina Aiello, 2017-2020

from flask import Flask, request, Response, jsonify
import slack
import re
import psycopg2
from flask_sqlalchemy import SQLAlchemy
import os
from time import localtime, strftime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
DATABASE = SQLAlchemy(app)

SLACK_CLIENT = slack.WebClient(os.environ["SLACK_BOT_TOKEN"], timeout=30)
BOT_USER_ID = "@U01AN5ZJP0X"
KARMA_BOT_CHANNEL = "C01B3N2ENAX"
BOT_EMOJI = ":up-and-down-votes:"
UPPER_BOUND_ON_KARMA_AT_A_TIME = 5
LOWER_BOUND_ON_KARMA_AT_A_TIME = -5

# Create our database model
class User(DATABASE.Model):
    __tablename__ = "users"
    id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    username = DATABASE.Column(DATABASE.String(120), unique=True)
    karma = DATABASE.Column(DATABASE.Integer)

    def __init__(self, username, karma):
        self.username = username
        self.karma = karma

    def __repr__(self):
        return "<Username %r>" % self.username

@app.route("/")
def homepage():
    return """
    KarmaBot
    """

@app.route("/karma", methods=["POST"])
def karma():
    username_of_karma_recipient = ""
    channel_event = request.json["event"]
    channel_id = channel_event["channel"]
    is_text_event = "text" in channel_event
    is_bot_message = "subtype" in channel_event and channel_event["subtype"] == "bot_message"
    is_in_bot_channel = channel_event['channel'] == KARMA_BOT_CHANNEL
    is_neither_bot_message_nor_bot_channel = not is_bot_message and not is_in_bot_channel

    if is_text_event and is_neither_bot_message_nor_bot_channel:
        text = str(channel_event["text"])

        # We are specifically looking for messages with "++" and "--" (or more pluses and minuses in a row) in them
        if text.find("++") > -1 or text.find("--") > -1:
            log("New non-bot and non-bot-channel message with ++ or -- came in!: " + str(channel_event))

            # When a person is @'ed in Slack, it shows up as <@USER_ID>. We want to grab that user
            # id from the message if we can.
            if text.find("<@") > -1:
                log("User ID of person we want to give karma to: " + text)
                username_match_groups = re.search( r"<@([\w\d_]+)>[\s+]?(\+\+|--).?", text, re.M|re.I)
                user_id = username_match_groups.group(1)
                # Call the Slack API to get this person's actual username, using their user_id
                user_info = SLACK_CLIENT.users_info(user=user_id)
                if user_info != None:
                    log("User info of person receiving karma: " + str(user_info))
                    username_of_karma_recipient = user_info["user"]["name"]
                else:
                    message = "Error in giving karma to: " + user_id + ". Could not find username based on user_id."
                    log(message)
                    return jsonify(message)
            else:
                # Person wasn"t tagged, so we are now going to check for just the username. Must be in the
                # format of USERNAME++, USERNAME ++, USERNAME--, or USERNAME --, e.g. christinajaiello ++
                username_match_groups = re.search( r"[\W+]?([\w\d_]+)[\s]?(\+\+|--).?", text, re.M|re.I)
                if username_match_groups == None:
                    error_message = "No karma added because we can't pull a name from the message."
                    log(error_message)
                    return jsonify(text=error_message)
                else:
                    username_of_karma_recipient = username_match_groups.group(1)

            # Determine karma amount based on + or -
            positive_karma_given = (text.count("+")-1) if ("+" in text) else 0
            negative_karma_given = (-1 * (text.count("-")-1)) if ("-" in text) else 0
            log("Positive given: " + str(positive_karma_given) + " and negative given: " + str(negative_karma_given))
            karma_given = positive_karma_given + negative_karma_given
            was_karma_limited = False
            if karma_given > UPPER_BOUND_ON_KARMA_AT_A_TIME:
                log("Karma given was: " + str(karma_given) + " but we are limiting it.")
                karma_given = UPPER_BOUND_ON_KARMA_AT_A_TIME
                was_karma_limited = True
            elif karma_given < LOWER_BOUND_ON_KARMA_AT_A_TIME:
                log("Karma given was: " + str(karma_given) + " but we are limiting it.")
                karma_given = LOWER_BOUND_ON_KARMA_AT_A_TIME
                was_karma_limited = True
            log("Karma given to " + username_of_karma_recipient + " was " + str(karma_given)) + "."

            # Look for user in database
            if not DATABASE.session.query(User).filter(User.username == username_of_karma_recipient).count():
                # User isn't in database. Create our user object
                log("Adding new user to karma database: " + username_of_karma_recipient)
                user = User(username_of_karma_recipient, karma_given)
                # Add them to the database
                DATABASE.session.add(user)
                DATABASE.session.commit()
            else:
                log("Updating existing user in karma database: " + username_of_karma_recipient)
                # If user is in database, get user's karma from database
                user = User.query.filter_by(username = username_of_karma_recipient).first()
                user.karma = user.karma + karma_given
                DATABASE.session.commit()
            
            # Return karma message
            karma_message = username_of_karma_recipient + "'s karma is now " + str(user.karma) + "."
            if was_karma_limited:
                karma_message = "Karma given was too much. Max of 5 and -5 allowed. " + karma_message
            log(karma_message)
            SLACK_CLIENT.chat_postMessage(
                channel=str(channel_id),
                text=karma_message,
                username="Karma Bot",
                icon_emoji=BOT_EMOJI
            )
            return jsonify(text="karma_message")
        elif channel_event['type'] == 'app_mention' and text.find(BOT_USER_ID) > -1:
            # If somebody @'ed our Karma Bot
            pinged_bot_message = channel_event['user'] + " pinged the bot at timestamp " + channel_event['event_ts'] + "."
            log(pinged_bot_message + str(channel_event))
            all_users = DATABASE.session.query(User)
            users_and_karma = ""
            for user in all_users:
                username_and_karma = (user.username) + ": " + str(user.karma) + "\n"
                users_and_karma += username_and_karma
                print(username_and_karma)
            print(users_and_karma)
            log(users_and_karma)
            SLACK_CLIENT.chat_postMessage(
                channel=str(channel_id),
                text=users_and_karma,
                username="Karma Bot",
                icon_emoji=BOT_EMOJI
            )
            return jsonify(text="Not a karma message")
        else:   
            not_karma_message = "Not a karma message"
            log(not_karma_message + ": " + str(channel_event))
            return jsonify(text=not_karma_message)
    else:   
        not_karma_message = "Not a karma message"
        # THIS MUST BE A PRINT, NOT A LOG
        print(not_karma_message + ": " + str(channel_event))
        return jsonify(text=not_karma_message)


# This will send logs to the "karma_bot_log" channel in our workspace
def log(log_message):
    log_message = "[" + strftime("%Y-%m-%d %H:%M:%S", localtime()) + "] " + log_message
    print(log_message)
    SLACK_CLIENT.chat_postMessage(
        channel="karma_bot_log",
        text= log_message,
        username="Karma Bot",
        icon_emoji=BOT_EMOJI
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0")
