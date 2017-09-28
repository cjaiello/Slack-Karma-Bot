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
    users_total_karma = 0
    text = request.form.get('text', '')

    # Get username from message
    # https://pythex.org/
    username_match_group = re.search( r'[\s+]?(\+\+|--)[\W+]?([\w\d_]+)[\s]?', text, re.M|re.I)
    username_match = username_match_group.group(2)

    # Determine karma amount based on ++ or --
    karma_given = 1 if ('++' in text) else -1

    # Look for user in database
    if not db.session.query(User).filter(User.username == username_match).count():
        # User isn't in database. Create our user object
        user = User(username_match, karma_given)
        # Add them to the database
        db.session.add(user)
        db.session.commit()
        users_total_karma = karma_given
    else:
        # If user is in database, get user's karma from database
        user = User.query.filter_by(username = username_match).first()
        user.karma = user.karma + karma_given
        db.session.commit()
        users_total_karma = user.karma
    # Return karma
    return jsonify(text=username_match + "'s karma is now " + str(users_total_karma))
    return Response(), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0')
