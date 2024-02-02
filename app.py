import os

from flask import Flask, request, jsonify, render_template, redirect, url_for,send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from werkzeug.utils import secure_filename

app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')

# Add your Twilio credentials
@app.route('/token')
def generate_token():
    TWILIO_ACCOUNT_SID = 'ACb1d1db82ba1d51b753d3b6f1aa7db5bb'
    TWILIO_SYNC_SERVICE_SID = 'IS1fee0f0d38e86b4de6855ee8f8dd474a'
    TWILIO_API_KEY = 'SKcf0c7997830edb02237b4be72efecd09'
    TWILIO_API_SECRET = 'q0sOLQeMDg2k7a3qxA7R3qvSSnLBXZwT'

    username = request.args.get('username', fake.user_name())

    # create access token with credentials
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    # create a Sync grant and add to token
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())

# Write the code here
@app.route('/', methods=['POST'])
def download_text():
    d = request.form['text']
    with open('andrew.txt', 'w') as f:
        f.write(d)
    b = 'andrew.txt'
    return send_file(b, as_attachment = True)



if __name__ == "__main__":
    app.run(host='localhost', port='5001', debug=True)
