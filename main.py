from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import pprint
from dotenv import load_dotenv

# -------------------- SCRAPE THE BILLBOARD 100 --------------------

BILLBOARD_100_URL = "https://www.billboard.com/charts/hot-100/"

# Scrape the Billboard 100
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
# date = "2001-06-01"

response = requests.get(BILLBOARD_100_URL + date)
billboard_html = response.text

soup = BeautifulSoup(billboard_html, "html.parser")
# print(soup.prettify())

song_names_spans = soup.find_all("span", class_="chart-element__information__song text--truncate color--primary")
# print(song_names_spans)
song_names = [song.getText() for song in song_names_spans]
print(song_names)


# -------------------- SPOTIFY AUTHENTICATION  --------------------

# Load environment variables from .env
# By default, load_dotenv doesn't override existing environment variables.
#
# https://pypi.org/project/python-dotenv/
load_dotenv(".env")
SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
# print(user_id)


# -------------------- SEARCH SPOTIFY FOR SONGS BY TITLE --------------------

song_uris = []
year = date.split("-")[0]

for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(result)

    # Sometimes a song is not available in Spotify.
    # Use exception handling to skip over those songs.
    try:
        uri = result["tracks"]["items"][0]["uri"]
        # print(uri)
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify.  Skipped.")
print(song_uris)


# -------------------- CREATE SPOTIFY PLAYLIST --------------------

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard Top 100", public=False)
print(playlist)

# Add songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)