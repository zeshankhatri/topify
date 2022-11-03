import streamlit as st
import numpy as np
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from spotipy.cache_handler import MemoryCacheHandler
import random, string
import os


# Generates state value (state parameter serves security purposes)
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


# Specifies which time period to get data for
def get_term(key):
    # Radio button to select time range parameter for parsing data
    term = st.radio(
        "How far back would you like to go?",
        ('Past Month', 'Past Six Months', 'All Time'),
        horizontal=True,
        key=key
    )

    if term == 'Past Month':
        t = 'short_term'
    elif term == 'Past Six Months':
        t = 'medium_term'
    else:
        t = 'long_term'

    return t


# Specifies the amount of items to list
def get_limit(key):
    # Show max limit tracks
    show_all = st.checkbox('Show All', key=key+'1') #to avoid duplicate keys

    if show_all:
        limit = st.slider(
            "Show top:",
            min_value=5,
            max_value=50,
            value=10,
            step=1,
            key=key,
            disabled=True
        )
        limit=50
    else:
        limit = st.slider(
            "Show top:",
            min_value=5,
            max_value=50,
            value=10,
            step=1,
            key=key
        )

    return limit


def get_top_items(item, term, limit):
    if item == 'tracks':
        # Get top tracks during given term up to specified limit (max 50)
        res = st.session_state['user'].current_user_top_tracks(
            limit=limit,
            time_range=term
        )
    else:
        # Get top artists during given term up to specified limit (max 50)
        res = st.session_state['user'].current_user_top_artists(
            limit=limit,
            time_range=term
        )

    return res


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
SPOTIPY_CLIENT_ID = st.secrets['SPOTIPY_CLIENT_ID']
SPOTIPY_CLIENT_SECRET = st.secrets['SPOTIPY_CLIENT_SECRET']
REDIRECT_URI = st.secrets['REDIRECT_URI']

# Gets URL parameters following authentication
url_params = st.experimental_get_query_params()

# Specify scope
scope = "user-library-read user-top-read"

# Specify Authorization Code Flow parameters
oauth = SpotifyOAuth(scope=scope,
                     redirect_uri=REDIRECT_URI,
                     client_id=SPOTIPY_CLIENT_ID,
                     client_secret=SPOTIPY_CLIENT_SECRET)

# /authorize
auth_url = oauth.get_authorize_url()

st.title("Topify")

add_selectbox = st.sidebar.selectbox(
    "What Would You Like to Know?",
    ["Favorite Tracks and Artists", "Some Fun General Spotify Data"]
)

if add_selectbox == "Some Fun General Spotify Data":
    # See Spotify's official colors
    st.subheader("Spotify's Official Colors")
    st.info("Enter the corresponding value to view the color!")
    st.write("Green: #1D8954, White: #FFFFFF, Black: #191414")
    st.color_picker('Random Label', '#1D8954', label_visibility='collapsed')
    st.subheader("Map and Graphs")

    # Client Credentials Authorization
    auth_manager = SpotifyClientCredentials(cache_handler=MemoryCacheHandler())
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # Gets available markets country code and loads data file of capitals
    markets = sp.available_markets()
    markets = markets['markets']
    df = pd.read_csv('assets/country_capitals.csv')

    latitudes = []
    longitudes = []

    # For all merket country codes, get latitude and longitude of capital
    for i, code in enumerate(df['CountryCode']):
        if code in markets:
            latitudes.append(df['CapitalLatitude'][i])
            longitudes.append(df['CapitalLongitude'][i])

    # Map of available markets by capital
    locations = pd.DataFrame({
         'latitude': latitudes,
         'longitude': longitudes
    })

    st.write("Spotify's Available Markets:")
    st.map(locations)
    st.caption('Countries (Markets) marked according to capital.')
else:
    if "code" not in url_params:
        st.info("Click the green button to view your top artists and tracks from Spotify!")
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
        # Get user data (Authorization Code Flow)
        if 'user' not in st.session_state:
            code = url_params['code'][0]
            token = get_token(oauth, code)
            st.session_state['user'] = sign_in(token)
            st.success("Sign in successful.")

        user = st.session_state['user'].current_user()
        name = user["display_name"]
        username = user["id"]

        st.subheader("Happy to see you, {n}!".format(n=name))
        st.write("Let's see your music taste by using the options below:")

        tracks, artists, genres = st.tabs(["Your Top Tracks", "Your Top Artists", "Your Top Genres"])

        with tracks:
            term = get_term('t_term')
            limit = get_limit('t_limit')

            # Get top tracks during given term
            results = get_top_items('tracks', term, limit)

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
                }
            )
            show_tracks.index += 1

            # Displaying the dataframe
            st.dataframe(show_tracks, use_container_width=True)

        with artists:
            term = get_term('a_term')
            limit = get_limit('a_limit')

            # Get top artists during given term
            results = get_top_items('artists', term, limit)

            # Display top artists
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

        with genres:
            # Top artists data used to determine top genres
            term = get_term('g_term')

            results = get_top_items('artists', term, 50) # gets max num of entries

            # Get genres through top artists data
            count_genres = {}

            for item in results['items']:
                for genre in item['genres']:
                    genre = string.capwords(genre)
                    count_genres[genre] = count_genres.get(genre, 0) + 1

            # Sort genres based on how many top artists are part of genre
            sorted_genres = sorted(count_genres.items(), key=lambda x: x[1], reverse=True)
            count_genres = dict(sorted_genres)
            genres = list(count_genres.keys())

            # Display top genres
            limit = get_limit('g_limit')
            show_genres = pd.DataFrame(
                {
                    "Genre": genres[:limit]
                },
            )
            show_genres.index += 1

            # Displaying the dataframe
            st.dataframe(show_genres, use_container_width=True)

            genre_data = st.checkbox('Learn genre data taking process.')

            if genre_data:
                st.info('''Unlike top tracks and artists, Spotify doesn't provide top genre data. However, top artist data
                            supplies the genre(s) of each artist. Based on that, the following graph showcases which genre 
                            appeared the most in all your top artists:''')

                counts = list(count_genres.values())

                bar_chart = pd.DataFrame({
                    "Genre": genres[:limit],
                    "Instances": counts[:limit]
                })

                st.bar_chart(bar_chart, x='Genre', y="Instances")