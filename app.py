# Karma Bot by Christina Aiello, 2017. cjaiello@wpi.edu

from flask import Flask, request, Response, jsonify
import slack
import re
import psycopg2
from flask_sqlalchemy import SQLAlchemy
import os
from time import localtime, strftime

SLACK_CLIENT = slack.WebClient(os.environ["SLACK_BOT_TOKEN"], timeout=30)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
oauth_scope = "users:read"

# Create our database model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    karma = db.Column(db.Integer)

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
    users_total_karma = 0
    username_match = ""
    channel_event = request.json["event"]
    channel_id = channel_event["channel"]
    is_bot_message = "subtype" in channel_event and channel_event["subtype"] != "bot_message"

    if "text" in channel_event and not is_bot_message:
        text = str(channel_event["text"])
        log("text was: " + str(text))
        log("channel_id was: " + str(channel_id))

        if text.find("++") > -1 or text.find("--") > -1:
            log("This is a potential karma message! " + str(text))

            if text.find("<@") > -1:
                # Person was tagged and we actually received an ID
                log("User ID of person we want to give karma to:" + text)
                username_match_group = re.search( r"<@([\w\d_]+)>[\s+]?(\+\+|--).?", text, re.M|re.I)
                user_id = username_match_group.group(1)
                user_info = SLACK_CLIENT.users_info(user=user_id)
                log(str(user_info))
                if user_info != None:
                    username_match = user_info["user"]["name"]
                else:
                    log(user_info)
                    return jsonify("Error in giving karma. Please contact caiello@vistaprint.com")
            else:
                # Person wasn"t tagged, so we have the actual name
                username_match_group = re.search( r"[\W+]?([\w\d_]+)[\s]?(\+\+|--).?", text, re.M|re.I)
                if username_match_group == None:
                    log("No karma added because we can't pull a name")
                    return jsonify(text="No karma added because we can't pull a name")
                else:
                    username_match = username_match_group.group(1)

            # Determine karma amount based on + or -
            karma_given = (text.count("+")-1) if ("+" in text) else (-1 * (text.count("-")-1))
            was_karma_limited = False
            if karma_given > 5:
                log("Karma given was: " + str(karma_given) + " but we are limiting it.")
                karma_given = 5
                was_karma_limited = True
            elif karma_given < -5:
                log("Karma given was: " + str(karma_given) + " but we are limiting it.")
                karma_given = -5
                was_karma_limited = True
            log("Karma given to " + username_match + " was " + str(karma_given))

            # Look for user in database
            if not db.session.query(User).filter(User.username == username_match).count():
                log("Adding to database: " + username_match)
                # User isn"t in database. Create our user object
                user = User(username_match, karma_given)
                # Add them to the database
                db.session.add(user)
                db.session.commit()
                users_total_karma = karma_given
            else:
                log("Updating in database: " + username_match)
                # If user is in database, get user's karma from database
                user = User.query.filter_by(username = username_match).first()
                user.karma = user.karma + karma_given
                db.session.commit()
                users_total_karma = user.karma
            
            # Return karma
            karma_message = ("Karma given was too much! Max of 5 and -5 allowed. " if was_karma_limited else "") + username_match + "'s karma is now " + str(users_total_karma) + "."
            log(karma_message)

            response = SLACK_CLIENT.chat_postMessage(
                channel=str(channel_id),
                text= karma_message,
                username="Karma Bot",
                icon_emoji=":plus:"
            )
            return jsonify(text="karma_message")
    log("Not a karma message")
    return jsonify(text="Not a karma message")


# This will send logs to the "karma_bot_log" channel in our workspace
def log(log_message):
    log_message = "[" + strftime("%Y-%m-%d %H:%M:%S", localtime()) + "] " + log_message
    print(log_message)
    # response = SLACK_CLIENT.chat_postMessage(
    #     channel="karma_bot_log",
    #     text= log_message,
    #     username="Karma Bot",
    #     icon_emoji=":plus:"
    # )

if __name__ == "__main__":
    app.run(host="0.0.0.0")
