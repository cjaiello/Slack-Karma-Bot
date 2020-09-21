# Karma Bot by Christina Aiello, 2017. cjaiello@wpi.edu

from flask import Flask, request, Response, jsonify
import slack
import re
import psycopg2
from flask_sqlalchemy import SQLAlchemy
import os

SLACK_CLIENT = slack.WebClient(os.environ["SLACK_BOT_TOKEN"], timeout=30)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
        return '<Username %r>' % self.username

@app.route('/')
def homepage():
    return """
    KarmaBot
    """

@app.route('/karma', methods=['POST'])
def karma():
    users_total_karma = 0
    username_match = ''
    channel_event = request.json['event']
    print("channel_event was: " + str(channel_event))
    text = channel_event['text']
    print("text was: " + str(text))

    if '++' in text:
        print("This is a potential karma message!")
        # Get username from message
        # https://pythex.org/
        if '<@' in text:
            # Person was tagged and we actually received an ID
            print("User ID of person we want to give karma to:" + text)
            username_match_group = re.search( r'<@([\w\d_]+)>[\s+]?(\+\+|--).?', text, re.M|re.I)
            user_id = username_match_group.group(1)
            user_info = SLACK_CLIENT.users_info(user=user_id)
            print(str(user_info))
            if user_info != None:
                username_match = user_info['user']['profile']['name']
            else:
                print(user_info)
                return jsonify("Error in giving karma. Please contact caiello@vistaprint.com")
        else:
            # Person wasn't tagged, so we have the actual name
            username_match_group = re.search( r'[\W+]?([\w\d_]+)[\s]?(\+\+|--).?', text, re.M|re.I)
            username_match = username_match_group.group(1)
            if username_match_group == None:
                return

        # Determine karma amount based on + or -
        karma_given = (text.count('+')-1) if ('+' in text) else (-1 * (text.count('-')-1))
        print("Karma given to " + username_match + " was " + str(karma_given))

        # Look for user in database
        if not db.session.query(User).filter(User.username == username_match).count():
            print("Adding to database: " + username_match)
            # User isn't in database. Create our user object
            user = User(username_match, karma_given)
            # Add them to the database
            db.session.add(user)
            db.session.commit()
            users_total_karma = karma_given
        else:
            print("Updating in database: " + username_match)
            # If user is in database, get user's karma from database
            user = User.query.filter_by(username = username_match).first()
            user.karma = user.karma + karma_given
            db.session.commit()
            users_total_karma = user.karma
        # Return karma
        print(jsonify(text=username_match + "'s karma is now " + str(users_total_karma)))

        response = SLACK_CLIENT.chat_postMessage(
            channel=str(channel_name),
            text= ("Please reply here with your standup status!" if (message == None) else message),
            username="Standup Bot",
            icon_emoji=":memo:"
        )
    else:
        return jsonify(text="No karma added")

if __name__ == '__main__':
    app.run(host='0.0.0.0')
