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


def get_token(oauth, code):
    token = oauth.get_access_token(code, as_dict=False, check_cache=False)
    # remove cached token saved in directory
    os.remove(".cache")

    # return the token
    return token


def sign_in(token):
    sp = spotipy.Spotify(auth=token)
    return sp
#
#
# def app_get_token():
#     try:
#         token = get_token(st.session_state["oauth"], st.session_state["code"])
#     except Exception as e:
#         st.error("An error occurred during token retrieval!")
#         st.write("The error is as follows:")
#         st.write(e)
#     else:
#         st.session_state["cached_token"] = token
#
#
# def app_sign_in():
#     try:
#         sp = sign_in(st.session_state["cached_token"])
#     except Exception as e:
#         st.error("An error occurred during sign-in!")
#         st.write("The error is as follows:")
#         st.write(e)
#     else:
#         st.session_state["signed_in"] = True
#         authorize()
#         st.success("Sign in success!")
#
#     return sp
#
# def authorize():
#     oauth = SpotifyOAuth(scope=scope,
#                          redirect_uri=REDIRECT_URI,
#                          client_id=CLIENT_ID,
#                          client_secret=CLIENT_SECRET)
#
#     st.session_state["oauth"] = oauth
#
#     auth_url = oauth.get_authorize_url()
#
#     link_html = " <a target=\"_self\" href=\"{url}\" >{msg}</a> ".format(
#         url=auth_url,
#         msg="Click me to authenticate!"
#     )
#
#     if not st.session_state["signed_in"]:
#         st.markdown(link_html, unsafe_allow_html=True)


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

# if "signed_in" not in st.session_state:
#     st.session_state["signed_in"] = False
# if "cached_token" not in st.session_state:
#     st.session_state["cached_token"] = ""
# if "code" not in st.session_state:
#     st.session_state["code"] = ""
# if "oauth" not in st.session_state:
#     st.session_state["oauth"] = None

url_params = st.experimental_get_query_params()

st.write(url_params)

st.write("Hello. Testing")

sliders = st.checkbox("Sliders")

if sliders:
    authorize_url = 'https://accounts.spotify.com/authorize'
    scope = "user-library-read"
    state = generate_random_string(16)

    # # attempt sign in with cached token
    # if st.session_state["cached_token"] != "":
    #     sp = app_sign_in()
    # # if no token, but code in url, get code, parse token, and sign in
    # elif "code" in url_params:
    #     # all params stored as lists, see doc for explanation
    #     st.session_state["code"] = url_params["code"][0]
    #     app_get_token()
    #     sp = app_sign_in()
    # # otherwise, prompt for redirect
    # else:
    #     authorize()
    #
    # if st.session_state["signed_in"]:
    #     user = sp.current_user()
    #     name = user["display_name"]
    #     username = user["id"]
    #
    #     st.markdown("Hi {n}! Let's modify a playlist or two :smiley:".format(n=name))

    # authorized = requests.get(authorize_url, {
    #     'client_id' : CLIENT_ID,
    #     'response_type' : 'code',
    #     'redirect_uri' : REDIRECT_URI,
    #     'state' : state,
    #     'scope' : scope,
    #     'show_dialog' : 'true',
    # })

    oauth = SpotifyOAuth(scope=scope,
                         state=state,
                         redirect_uri=REDIRECT_URI,
                         client_id=CLIENT_ID,
                         client_secret=CLIENT_SECRET)

    auth_url = oauth.get_authorize_url()

    link_html = " <a target=\"_self\" href=\"{url}\" >{msg}</a> ".format(
        url=auth_url,
        msg="Click me to authenticate!"
    )

    st.markdown(link_html)



    # sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    # results = sp.current_user_saved_tracks()
    # st.success("It works!")
    # for idx, item in enumerate(results['items']):
    #     track = item['track']
    #     st.write(f"{idx + 1} {track['artists'][0]['name']} - {track['name']}")