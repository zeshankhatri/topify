import streamlit as st
import numpy as np
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random, string
from urllib.parse import urlparse, parse_qs
import requests

def generate_random_string(length):
    characters = string.ascii_letters + string.digits + "_.-~"
    return ''.join(random.choice(characters) for i in range(length))

st.set_page_config(
    page_title = "Topify",
    layout="wide",
    menu_items = {
        'Get Help' : 'https://docs.streamlit.io/',
        'About' : '# Developed by Julio Arroyo and Zeshan Khatri'
    }
)

CLIENT_ID = st.secrets['CLIENT_ID']
CLIENT_SECRET = st.secrets['CLIENT_SECRET']
REDIRECT_URI = st.secrets['REDIRECT_URI']

st.write("Hello. Testing")

sliders = st.checkbox("Sliders")

if sliders:
    authorize_url = 'https://accounts.spotify.com/authorize'
    scope = "user-library-read"
    state = generate_random_string(16)

    oauth = SpotifyOAuth(scope=scope,
                         redirect_uri=REDIRECT_URI,
                         client_id=CLIENT_ID,
                         client_secret=CLIENT_SECRET)

    auth_url = oauth.get_authorize_url()

    link_html = " <a target=\"_self\" href=\"{url}\" >{msg}</a> ".format(
        url=auth_url,
        msg="Click me to authenticate!"
    )

    st.markdown(link_html, unsafe_allow_html=True)

    # authorized = requests.get(authorize_url, {
    #     'client_id' : CLIENT_ID,
    #     'response_type' : 'code',
    #     'redirect_uri' : REDIRECT_URI,
    #     'state' : state,
    #     'scope' : scope,
    #     'show_dialog' : 'true',
    # })

    # authorized_data = parse_qs(urlparse(authorized).query)

    # st.write(authorized)

    # sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    # results = sp.current_user_saved_tracks()
    # st.success("It works!")
    # for idx, item in enumerate(results['items']):
    #     track = item['track']
    #     st.write(f"{idx + 1} {track['artists'][0]['name']} - {track['name']}")