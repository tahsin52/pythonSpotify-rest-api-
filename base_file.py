import json
import requests
import secrets
from pprint import pprint
import sys

class lastFmSpotify():
    def __init__(self):
        self.token = secrets.spotify_token()
        self.api_key = secrets.last_fm_api_key()
        self.user_id = secrets.spotify_user_id()
        self.headers = {"Content-Type": "application/json",
                        "Authorization": f"Bearer {self.token}"}
        self.playlist_id = ""
        self.song_info = {}
        self.uris = []

#https://www.last.fm/api/show/chart.getTopTracks

#https://developer.spotify.com/console/get-search-item/

    def fetch_songs_from_lastFm(self):
        params = {"limit": 20, "api_key": self.api_key}
        url = f"http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&format=json"
        response = requests.get(url, params=params)
        if response.status_code != 200:
            self.exceptionalExceptions(response.status_code, response.text())
        res = response.json()
        print("Top Songs are: ")
        for item in res['tracks']['track']:
            song = item['name'].title()
            artist = item['artist']['name'].title()
            print(f"{song} by {artist}")
            self.song_info[song] = artist
        print("Getting Song URI\n")
        self.get_uri_from_spotify()
        print("Creating a playlist!")
        self.create_spotify_playlist()
        print("Adding Songs!\n")
        self.add_songs_to_playlist()
        print("Songs are as follows: \n")
        self.list_songs_in_playlist()

    def get_uri_from_spotify(self):

        for song_name, artist in self.song_info.items():
            url = f"https://api.spotify.com/v1/search?query=track%3A{song_name}+artist%3A{artist}&type=track&offset=0&limit=10"
            response = requests.get(url, headers=self.headers)

            res = response.json()
            output_uri = res['tracks']['items']
            uri = output_uri[0]['uri']
            self.uris.append(uri)

    def create_spotify_playlist(self):
        data = {
            "name": "Last Fm songs !",
            "description": "Songs from the topcharts of Last FM created via an API",
            "public": True
        }
        data = json.dumps(data)
        url = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"
        response = requests.post(url, data=data, headers=self.headers)
        print(response.status_code)
        if response.status_code == 201:
            res = response.json()
            self.playlist_id = res['id']
        else:
            self.exceptionalExceptions(response.status_code, response.text())

    def add_songs_to_playlist(self):
        uri_list = json.dumps(self.uris)
        url = f"https://api.spotify.com/v1/playlists/{self.playlist_id}/tracks"
        response = requests.post(url, data=uri_list, headers=self.headers)
        if response.status_code == 201:
            print("Songs Added Successfully.")
        else:
            self.exceptionalExceptions(response.status_code, response.text())

    def list_songs_in_playlist(self):
        self.playlist_id = "" # Go playlist and right click -> Share->Copy Playlist Link and pasted
        url = f"https://api.spotify.com/v1/playlists/{self.playlist_id}/tracks"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            self.exceptionalExceptions(response.status_code, response.text())
        else:
            res = response.json()
            for item in res['items']:
                print(item['track']['name'])


    def exceptionalExceptions(self, status_code, err):
        print("Exception Occured with status code", status_code)
        print("Error", err)


