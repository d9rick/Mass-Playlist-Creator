import spotipy
from dotenv import load_dotenv
import time
import os

# get auth
from spotipy.oauth2 import SpotifyOAuth

# set up scopes
scopes = "user-library-read,playlist-modify-private,playlist-modify-public"

# set up credentials
load_dotenv('.env')
clientID = os.environ.get("ClientID")
clientSECRET = os.environ.get("clientSECRET")
redirectURI = os.environ.get("redirectURI")
numSongs = os.environ.get("numSongs")
newPlaylistID = os.environ.get("newPlaylistID")

# create OAUTH connection
spotify = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(client_id = clientID, client_secret = clientSECRET, scope = scopes, redirect_uri = redirectURI))

# stores album ids
albums = []

# get albums in increments of 50
for n in range(0, (int(numSongs)//50)+1):
    start = n*50
    albumCount = 0

    # get liked songs playlist
    likedSongs = spotify.current_user_saved_tracks(limit=50, offset=start)

    # get list of albums from tracks
    for i, track in enumerate(likedSongs['items']):

        # check if album is already grabbed
        if track['track']['album']['id'] in albums:
            print("Found duplicate album: " + track['track']['album']['name'] + '\n')
            continue

        # output current work
        print(str(i + n*50) + " " + track['track']['album']['name'] + " by " + track['track']['artists'][0]['name'])
        print('\t' + "ID: " + track['track']['album']['id'] + '\n')

        # add album to list
        albums.append(track['track']['album']['id'])
        print()
        albumCount += 1

    # get songs from each album and add to the new playlist
    for albumID in albums[-albumCount:]:
        # printing
        print(spotify.album(album_id=albumID)['name'] + ":")

        # get songs
        tracks = []
        for track in spotify.album_tracks(album_id=albumID)['items']:
            print('\t' + track['name'])
            tracks.append(track['id'])
        print()

        # add songs
        spotify.playlist_add_items(playlist_id=newPlaylistID, items=tracks)
        albumCount += 1
    
    # must sleep due to rate limits
    time.sleep(30)