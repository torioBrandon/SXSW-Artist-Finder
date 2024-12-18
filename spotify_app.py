import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API credentials (replace with your credentials)
CLIENT_ID = "your_client_id"  # Replace with your Spotify Client ID
CLIENT_SECRET = "your_client_secret"  # Replace with your Spotify Client Secret

# Authenticate with Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET), requests_timeout=30)

# Function to extract artist names from a playlist
def get_artists_from_playlist(playlist_url):
    playlist_id = playlist_url.split("/")[-1].split("?")[0]
    artists = set()
    offset = 0
    limit = 100

    while True:
        results = sp.playlist_tracks(playlist_id, offset=offset, limit=limit)
        for item in results["items"]:
            track = item["track"]
            if track and track["artists"]:
                for artist in track["artists"]:
                    artists.add(artist["name"])

        if results["next"] is None:
            break
        offset += limit

    return artists

# Streamlit app layout
st.title("Spotify Playlist Artist Comparator 🎵")

st.write("Enter two Spotify playlist URLs to find artists that are shared in both playlists.")

# Input fields for playlist URLs
playlist_url_1 = st.text_input("Enter the first playlist URL:")
playlist_url_2 = st.text_input("Enter the second playlist URL:")

if st.button("Compare Playlists"):
    if playlist_url_1 and playlist_url_2:
        try:
            # Get artists from playlists
            artists_1 = get_artists_from_playlist(playlist_url_1)
            artists_2 = get_artists_from_playlist(playlist_url_2)

            # Find common artists
            common_artists = artists_1.intersection(artists_2)

            # Display results
            if common_artists:
                st.success(f"Found {len(common_artists)} common artists:")
                for artist in sorted(common_artists):
                    st.write(artist)
            else:
                st.warning("No common artists found.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please provide both playlist URLs.")
