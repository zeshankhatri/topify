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
    token = oauth.get_access_token(code, as_dict=False, check_cache=False)
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
    # layout="wide",
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
state = generate_random_string(16)

oauth = SpotifyOAuth(scope=scope,
                     state=state,
                     redirect_uri=REDIRECT_URI,
                     client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET)

# /authorize
auth_url = oauth.get_authorize_url()

st.title("Topify")

add_selectbox = st.sidebar.selectbox(
    "Change Request:",
    ["Top Tracks", "Top Artists", "Spotify's Available Markets"]
)

if add_selectbox == "Top Artists":
    st.write("In progress")
elif add_selectbox == "Spotify's Available Markets":
    st.write("In progress")
else:
    # login = st.button("Login to Spotify")
    #
    # if login:
    #     webbrowser.open_new_tab(auth_url)
    link_html = "<style> "
    link_html += " button { display: inline-block; background-color: #1db954; border-radius: 10px; border: 4px single #cccccc; color: #eeeeee;"
    link_html += " text-align: center; font-size: 16px; padding: 10px; transition: all 0.5s; cursor: pointer; margin-bottom: 10px; }"
    link_html += " button span { cursor: pointer; display: inline-block; position: relative; transition: 0.5s; }"
    link_html += " button span:after { content: '>>'; position: absolute; opacity: 0; top: 0; right: -20px; transition: 0.5s; }"
    link_html += " button:hover span { padding-right: 25px; }"
    link_html += " button:hover span:after { opacity: 1; right: 0; }"
    link_html += "</style>"
    link_html += f" <a href=\"{auth_url}\" > <button> <span>Login to Spotify</span> </button> </a>"

    if "code" not in url_params:
        st.markdown(link_html, unsafe_allow_html=True)
    else:
        # Get user data
        code = url_params['code'][0]
        token = get_token(oauth, code)
        sp = sign_in(token)

        user = sp.current_user()
        name = user["display_name"]
        username = user["id"]

        st.write("Current user is: {n}".format(n=name))

        # Get top tracks during given term
        results = sp.current_user_top_tracks(
            limit=10,
            time_range='short_term'
        )

        # Display top tracks with artist
        st.success("It works!")
        st.text(f"No.\tSong\t\t\t\t\t\tArtist")
        for idx, item in enumerate(results['items']):
            track = item['name']
            artist = item['artists'][0]['name']
            st.text("%i\t%-47s %-50s" % (idx + 1, track, artist))  # st.text used as st.write doesn't support \t