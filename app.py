from flask import Flask, request, Response, jsonify
#import re
#from flask.ext.sqlalchemy import SQLAlchemy
app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/karma_database'
#db = SQLAlchemy(app)

@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return """
    <h1>Hello heroku</h1>
    <p>It is currently {time}.</p>
    <img src="http://loremflickr.com/600/400" />
    """.format(time=the_time)

@app.route('/karma', methods=['POST'])
def karma():
    text = request.form.get('text', '')
    if '++' in text:
        # Get username from message
        # https://pythex.org/
        matchObj = re.match( r'[\s]?([a-zA-Z0-9]*)\+\+*', text, re.M|re.I)

        # Look for user in database

            # If user is in database, get user's karma from database
            # Else return
        # Add 1 to karma
        # Update user's karma in database
        # Return karma
        return jsonify(text="test")
    else:
        return jsonify(text="no match")
    return Response(), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0')
