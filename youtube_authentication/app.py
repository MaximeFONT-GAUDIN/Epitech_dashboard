import requests
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from os import access
from flask import Flask, url_for, redirect, session, render_template
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = 'random secret'
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
youtube_api_key = 'AIzaSyAw4tEbC_2Grr-CZ5efq9mcuNTNFzs_Gpo'


# oauth config
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='644351998442-iumfbnpi6jm91pvec0d3gn8clhh88j6a.apps.googleusercontent.com',
    client_secret='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',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid profile email'},
)

@app.route('/')
def hello_world():
    email = dict(session).get('email', None)
    return f'Hello, {email} !'

@app.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    resp.raise_for_status()
    user_info = resp.json()
    print(user_info)
    # do something with the token and profile
    session['email'] = user_info['email']
    return redirect('/')
    # return resp.json()


@app.route('/sub_number', methods=["GET"])
def sub_number():
    data = []
    r = requests.get(f'https://www.googleapis.com/youtube/v3/channels?part=statistics&mine=true&key={ youtube_api_key }&access_token={ token }')       #(f'https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&mine=true&key={ youtube_api_key }')               (f'https://www.googleapis.com/youtube/v3/channels?part=id&mine=true&access_token={user.}')
    #https://www.googleapis.com/youtube/v3/channels?part=statistics&id={CHANNEL_ID}&key={YOUR_API_KEY}
    responses = r.json()

    # for response in responses:
    #     channel_info = {
    #         'title' : response['snippet']['title'],
    #         'subscribers' : response['statistics']['subscriberCount']
    #     }
    #     data.append(channel_info)
    # return render_template('index.html', data=data[0])

    return responses

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')