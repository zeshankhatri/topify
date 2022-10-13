import webbrowser

import streamlit as st
import numpy as np
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random, string
import requests
import os


# Generates state value
def generate_random_string(length):
    characters = string.ascii_letters + string.digits + "_.-~"
    return ''.join(random.choice(characters) for i in range(length))


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
        st.subheader("Click the green button to view your top artists and tracks from Spotify!")
        # Login button using HTML for ability to incorporate authorization link
        link_html = "<style> "
        link_html += " button { display: inline-block; background-color: #1db954; border-radius: 10px; border: 4px single #cccccc; color: #eeeeee;"
        link_html += " text-align: center; font-size: 16px; padding: 10px; transition: all 0.5s; cursor: pointer; margin-bottom: 10px; }"
        link_html += " button span { cursor: pointer; display: inline-block; position: relative; transition: 0.5s; }"
        link_html += " button span:after { content: '>>'; position: absolute; opacity: 0; top: 0; right: -20px; transition: 0.5s; }"
        link_html += " button:hover span { padding-right: 25px; }"
        link_html += " button:hover span:after { opacity: 1; right: 0; }"
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
            length = st.radio(
                "How far back would you like to go?",
                ('Past Month', 'Past Six Months', 'All Time'),
                horizontal=True
            )
            # Display top tracks with artist
            short_term = st.button("Short Term")
            long_term = st.button("Long Term")

            if length == 'Past Month':
                term = 'short_term'
            elif length == 'Past Six Months':
                term = 'medium_term'
            else:
                term = 'long_term'

            # Get top tracks during given term
            results = st.session_state['user'].current_user_top_tracks(
                limit=10,
                time_range=term
            )

            st.text(f"No.\tSong\t\t\t\t\t\tArtist")
            for idx, item in enumerate(results['items']):
                track = item['name']
                artist = item['artists'][0]['name']
                st.text("%i\t%-47s %-50s" % (idx + 1, track, artist))  # st.text used as st.write doesn't support \t

        with artists:
            st.write("Show top artists here")