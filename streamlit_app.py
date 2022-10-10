import streamlit as st
import numpy as np
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests

st.set_page_config(
    page_title = "Topify",
    layout="wide",
    menu_items = {
        'Get Help' : 'https://docs.streamlit.io/',
        'About' : '# Developed by Julio Arroyo and Zeshan Khatri'
    }
)

st.write("Hello. Testing")

sliders = st.checkbox("Sliders")

if sliders:
    scope = "user-library-read"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    results = sp.current_user_saved_tracks()
    st.success("It works!")
    for idx, item in enumerate(results['items']):
        track = item['track']
        st.write(f"{idx + 1} {track['artists'][0]['name']} - {track['name']}")