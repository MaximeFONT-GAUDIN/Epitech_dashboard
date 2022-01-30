from flask import Flask, abort, request
from uuid import uuid4
import requests
import requests.auth
import urllib
CLIENT_ID = "KyPJ3AbmMCmov7glXWbiwg" # Fill this in with your client ID
CLIENT_SECRET = "V1TT973BHOf6fxJ0FwVy-0O0gf1lEg" # Fill this in with your client secret
REDIRECT_URI = "http://127.0.0.1:5000/authorize_callback"


def user_agent():
    '''reddit API clients should each have their own, unique user-agent
    Ideally, with contact info included.
    
    e.g.,
    return "oauth2-sample-app by /u/%s" % your_reddit_username
    '''
    return "oauth2-dashboard by myself"
    raise NotImplementedError()

def base_headers():
    return {"User-Agent": user_agent()}


app = Flask(__name__)
@app.route('/')
def homepage():
    text = '<a href="%s">Authenticate with reddit</a>'
    return text % make_authorization_url()


def make_authorization_url():
    # Generate a random string for the state parameter
    # Save it for use later to prevent xsrf attacks
    """state = str(uuid4())
    save_created_state(state)"""
    params = {"client_id": CLIENT_ID,
              "response_type": "code",
              "state": "state",
              "redirect_uri": REDIRECT_URI,
              "duration": "temporary",
              "scope": "identity"}
    url = "https://www.reddit.com/api/v1/authorize?" + "client_id=" + CLIENT_ID + "&response_type=code" + "&state=state" + "&redirect_uri=" + REDIRECT_URI + "&duration=temporary" + "&scope=identity"      #urllib.urlencode(params)
    return url


# Left as an exercise to the reader.
# You may want to store valid states in a database or memcache.
def save_created_state(state):
    pass
def is_valid_state(state):
    return True

@app.route('/authorize_callback')
def reddit_callback():
    error = request.args.get('error', '')
    if error:
        return "Error: " + error
    state = request.args.get('state', '')
    if not is_valid_state(state):
        # Uh-oh, this request wasn't started by us!
        abort(403)
    code = request.args.get('code')
    access_token = get_token(code)
    # Note: In most cases, you'll want to store the access token, in, say,
    # a session for use in other parts of your web app.
    return "Your reddit username is: %s" % get_username(access_token)

def get_token(code):
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {"grant_type": "authorization_code",
                 "code": code,
                 "redirect_uri": REDIRECT_URI}
    headers = base_headers()
    response = requests.post("https://www.reddit.com/api/v1/access_token",
                             auth=client_auth,
                             headers=headers,
                             data=post_data)
    token_json = response.json()
    return token_json["access_token"]
    
    
def get_username(access_token):
    headers = base_headers()
    headers.update({"Authorization": "bearer " + access_token})
    response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
    me_json = response.json()
    return me_json['name']


if __name__ == '__main__':
    app.run(debug=True, port=5000)