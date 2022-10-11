import streamlit as st
import numpy as np
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random, string
import os
import requests

def generate_random_string(length):
    characters = string.ascii_letters + string.digits + "_.-~"
    return ''.join(random.choice(characters) for i in range(length))


def get_token(oauth, code):
    token = oauth.get_access_token(code, as_dict=False, check_cache=False)
    # remove cached token saved in directory
    os.remove(".cache")

    # return the token
    return token


def sign_in(token):
    sp = spotipy.Spotify(auth=token)
    return sp


st.set_page_config(
    page_title = "Topify",
    page_icon='assets/Spotify_Icon_RGB_Green.png',
    layout="wide",
    menu_items = {
        'Get Help' : 'https://docs.streamlit.io/',
        'About' : '# Developed by Julio Arroyo and Zeshan Khatri'
    }
)

CLIENT_ID = st.secrets['CLIENT_ID']
CLIENT_SECRET = st.secrets['CLIENT_SECRET']
REDIRECT_URI = st.secrets['REDIRECT_URI']

url_params = st.experimental_get_query_params()

st.write("Hello. Testing")

sliders = st.checkbox("Test Me!")

if sliders:
    scope = "user-library-read user-top-read"
    state = generate_random_string(16)

    oauth = SpotifyOAuth(scope=scope,
                         state=state,
                         redirect_uri=REDIRECT_URI,
                         client_id=CLIENT_ID,
                         client_secret=CLIENT_SECRET)

    auth_url = oauth.get_authorize_url()

    link_html = " <a href=\"{url}\" >{msg}</a> ".format(
        url=auth_url,
        msg="Click me to authenticate!"
    )

    st.markdown(link_html, unsafe_allow_html=True)

    if 'code' not in url_params:
        st.error("Please Reauthenticate")
    else:
        code = url_params['code'][0]
        token = get_token(oauth, code)
        sp = sign_in(token)

        user = sp.current_user()
        name = user["display_name"]
        username = user["id"]

        st.write("Current user is: {n}".format(n=name))

        results = sp.current_user_top_tracks(
            limit=10,
            time_range='short_term'
        )

        st.success("It works!")
        st.text(f"No.\tSong\t\t\t\tArtist")
        for idx, item in enumerate(results['items']):
            track = item['name']
            artist = item['artists'][0]['name']
            st.text(f"{idx + 1} {track:<20} {artist:<20}")