from flask import Flask, request, Response, jsonify
import re
from flask.ext.sqlalchemy import SQLAlchemy
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
    if '++' in text:
        # Get username from message
        # https://pythex.org/
        matchObj = re.match( r'\+\+[\s]?([a-z A-Z 0-9]+)', text, re.M|re.I)

        # Look for user in database
        if not db.session.query(User).filter(User.username == username).count():
            # User isn't in database.
            # Start them off with 1 karma point
            user = User(username, 1)
            db.session.add(user)
            db.session.commit()
        else:
            # If user is in database, get user's karma from database
            user = User.query.filter_by(User.username == username).first()
            user.karma = user.karma + 1
            db.session.commit()
            karma_number = user.karma
            karma_recipient = user.username
        # Return karma
        return jsonify(text=karma_recipient + "'s karma is now " + karma_number)
    return Response(), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0')
