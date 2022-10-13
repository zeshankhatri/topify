import webbrowser

import streamlit as st
import numpy as np
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random, string
import requests
import os


# Generates state value (state parameter serves security purposes)
def generate_random_string(length):
    characters = string.ascii_letters + string.digits + "_.-~"
    return ''.join(random.choice(characters) for i in range(length))


# Gets time range parameter
def get_term():
    # Radio button to select time range parameter for parsing data
    length = st.radio(
        "How far back would you like to go?",
        ('Past Month', 'Past Six Months', 'All Time'),
        horizontal=True
    )

    if length == 'Past Month':
        t = 'short_term'
    elif length == 'Past Six Months':
        t = 'medium_term'
    else:
        t = 'long_term'

    return t

# Makes POST request to get authorization token
def get_token(oauth, code):
    token = oauth.get_access_token(code, as_dict=False)
    # remove cached token saved in directory
    os.remove(".cache")

    # return the token
    return token


# Uses token to get user data according to scope
def sign_in(token):
    sp = spotipy.Spotify(auth=token)
    return sp


# Page configuration
st.set_page_config(
    page_title = "Topify",
    page_icon='assets/Spotify_Icon_RGB_Green.png',
    layout="centered",
    menu_items = {
        'Get Help' : 'https://docs.streamlit.io/',
        'About' : '# Developed by Julio Arroyo and Zeshan Khatri'
    }
)

# Establishes request parameters from Streamlit secrets
CLIENT_ID = st.secrets['CLIENT_ID']
CLIENT_SECRET = st.secrets['CLIENT_SECRET']
REDIRECT_URI = st.secrets['REDIRECT_URI']

# Gets URL parameters following authentication
url_params = st.experimental_get_query_params()

scope = "user-library-read user-top-read"

oauth = SpotifyOAuth(scope=scope,
                     redirect_uri=REDIRECT_URI,
                     client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET)

# /authorize
auth_url = oauth.get_authorize_url()

st.title("Topify")

add_selectbox = st.sidebar.selectbox(
    "What Would You Like to Know?",
    ["Favorite Tracks and Artists", "Some Fun General Spotify Data"]
)

if add_selectbox == "Some Fun General Spotify Data":
    st.write("In progress")
else:
    if "code" not in url_params:
        st.write("Click the green button to view your top artists and tracks from Spotify!")
        # Login button using HTML for ability to incorporate authorization link
        link_html = "<style> "
        link_html += " button { display: inline-block; background-color: #1db954; border-radius: 10px; border: 4px single #cccccc; color: #eeeeee;"
        link_html += " text-align: center; font-size: 16px; padding: 10px; transition: all 0.1s; cursor: pointer; margin-bottom: 10px; transition: 0.5s; }"
        link_html += " button:hover { cursor: pointer; padding: 12.5px; }"
        link_html += "</style>"
        link_html += f" <a href=\"{auth_url}\" > <button> <span>Login to Spotify</span> </button> </a>"

        st.markdown(link_html, unsafe_allow_html=True)

        # User did not grant authorization.
        if "error" in url_params:
            st.error("This app will not work without authorization! Please grant permission via the button above.")
    else:
        # Get user data
        if 'user' not in st.session_state:
            code = url_params['code'][0]
            token = get_token(oauth, code)
            st.session_state['user'] = sign_in(token)
            st.success("Sign in successful.")

        user = st.session_state['user'].current_user()
        name = user["display_name"]
        username = user["id"]

        st.subheader("Happy to see you, {n}!".format(n=name))
        st.write("Use the options below to learn more about your music.")

        tracks, artists = st.tabs(["Your Top Tracks", "Your Top Artists"])

        with tracks:
            term = get_term()

            # Get top tracks during given term
            results = st.session_state['user'].current_user_top_tracks(
                limit=10,
                time_range=term
            )

            # # Display top tracks
            track = []
            artist = []

            for item in results['items']:
                track.append(item['name'])
                artist.append(item['artists'][0]['name'])

            show_tracks = pd.DataFrame(
                {
                    "Song": track,
                    "Artist": artist
                },
            )
            show_tracks.index += 1

            # Displaying the dataframe
            st.dataframe(show_tracks, use_container_width=True)

        with artists:
            term = get_term()

            # Get top artists during given term
            results = st.session_state['user'].get_user_top_artists(
                limit=10,
                time_range=term
            )

            artist = []

            for item in results['items']:
                artist.append(item['name'])

            show_artists = pd.DataFrame(
                {
                    "Artist": artist
                },
            )
            show_artists.index += 1

            # Displaying the dataframe
            st.dataframe(show_artists, use_container_width=True)