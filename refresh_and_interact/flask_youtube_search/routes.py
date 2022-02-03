import requests
from isodate import parse_duration

from flask import Blueprint, render_template, current_app, request, redirect

import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# from .start import connexion

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():

    search_url = 'https://www.googleapis.com/youtube/v3/search'
    video_url = 'https://www.googleapis.com/youtube/v3/videos'

    videos = []

    if request.method == 'POST':
        search_params = {
            'key' : current_app.config['YOUTUBE_API_KEY'],
            'q' : request.form.get('query'),
            'part' : 'snippet',
            'maxResults' : 9,
            'type' : 'video'
        }

        r = requests.get(search_url, params=search_params)

        results = r.json()['items']

        video_ids = []

        for result in results:
            video_ids.append(result['id']['videoId'])
        
        if request.form.get('submit') == 'lucky':
            return redirect(f'https://www.youtube.com/watch?v={video_ids[0]}')
        
        if request.form.get('submit') == 'connexion':
            return redirect('/login')
        
        video_params = {
            'key' : current_app.config['YOUTUBE_API_KEY'],
            'id' : ','.join(video_ids),
            'part' : 'snippet,contentDetails',
            'maxResults' : 9
        }
    
        r = requests.get(video_url, params=video_params)
        results = r.json()['items']

        for result in results:
            video_data = {
                'id' : result['id'],
                'url' : f'https://www.youtube.com/watch?v={result["id"]}',
                'thumbnails' : result['snippet']['thumbnails']['high']['url'],
                'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'title' : result['snippet']['title']
            }
            videos.append(video_data)


    return render_template('index.html', videos=videos)

@main.route('/login')
def connexion():
    credentials = None

    # token.pickle stores the user's credentials from previously successful logins
    if os.path.exists('token.pickle'):
        print('Loading Credentials From File...')
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)

    # If there are no valid credentials available, then either refresh the token or log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print('Refreshing Access Token...')
            credentials.refresh(Request())
        else:
            print('Fetching New Tokens...')
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json',
                scopes=[
                    'https://www.googleapis.com/auth/youtube.readonly'
                ]
            )

            # flow.run_local_server(port=8080, prompt='consent',
            #                     authorization_prompt_message='')
            credentials = flow.credentials

            # Save the credentials for the next run
            with open('token.pickle', 'wb') as f:
                print('Saving Credentials for Future Use...')
                pickle.dump(credentials, f)

    youtube = build("youtube", "v3", credentials=credentials)

    request = youtube.playlistItems().list(part="status, contentDetails", playlistId="UUCezIgC97PvUuR4_gbFUs5g")

    response = request.execute()

    for item in response['items']:
        vid_id = item["contentDetails"]["videoId"]
        yt_link = f"https://youtu.be/{vid_id}"
        print(yt_link)