import os

import requests
import spotipy
import pprint
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

"""
This program will look up Billboard's Top 100 songs from any date and create a 
private Spotify playlist of those songs.

The Billboard top songs list is at:
https://www.billboard.com/charts/hot-100/
"""

# -------------------- SCRAPE THE BILLBOARD 100 --------------------

BILLBOARD_100_URL = "https://www.billboard.com/charts/hot-100/"

# Scrape the Billboard 100
print("This program will create a private Spotify playlist of the Billboard Top 100 songs from any date.")
date = input("Type the date you want to look up in this format YYYY-MM-DD: ")
# date = "2001-06-01"
print("")

response = requests.get(BILLBOARD_100_URL + date)
billboard_html = response.text

soup = BeautifulSoup(billboard_html, "html.parser")
# print(soup.prettify())

# Old implementation prior to Billboard changing its website layout in November 2021:
# song_names_spans = soup.find_all("span", class_="chart-element__information__song text--truncate color--primary")
# song_names = [song.getText() for song in song_names_spans]

song_names_spans = soup.find_all("h3", id="title-of-a-story", class_="a-font-primary-bold-s")
# print(song_names_spans)

song_names = [song.getText().strip() for song in song_names_spans]
print("Songs: ")
print(song_names)
print("")


# -------------------- SPOTIFY AUTHENTICATION  --------------------

# Load environment variables from .env
# By default, load_dotenv doesn't override existing environment variables.
#
# https://pypi.org/project/python-dotenv/
load_dotenv(".env")
SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")

# Successfully authenticating with Spotify will generate a file "token.txt".
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
print("")
print(song_uris)


# -------------------- CREATE PRIVATE SPOTIFY PLAYLIST --------------------

playlist = sp.user_playlist_create(user=user_id, name=f"{date} - Billboard Top 100", public=False)
print(playlist)

# Add songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

print("")
print("Your Spotify playlist has been created at URL:")
print(playlist["external_urls"]["spotify"])
