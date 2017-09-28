from flask import Flask, request, Response, jsonify
import re
import psycopg2
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

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
    karma_recipient = ""
    karma_number = 1
    text = request.form.get('text', '')
    # Get username from message
    # https://pythex.org/
    username_match_group = re.search( r'[\s+]?\+\+[\W+]?([\w\d_]+)[\s]?', text, re.M|re.I)
    username_match = username_match_group.group(1)
    print(username_match)

    if '++' in text:

        # Look for user in database
        if not db.session.query(User).filter(User.username == username_match).count():
            # User isn't in database.
            # Start them off with 1 karma point
            user = User(username_match, 1)
            db.session.add(user)
            db.session.commit()
            karma_recipient = username_match
        else:
            # If user is in database, get user's karma from database
            user = User.query.filter_by(username = username_match).first()
            user.karma = user.karma + 1
            db.session.commit()
            karma_number = user.karma
            karma_recipient = user.username
    elif "--" in text:
        # If user is in database, get user's karma from database
        user = User.query.filter_by(username = username_match).first()
        user.karma = user.karma - 1
        db.session.commit()
        karma_number = user.karma
        karma_recipient = user.username
        # Return karma
    return jsonify(text=karma_recipient + "'s karma is now " + str(karma_number))
    return Response(), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0')
