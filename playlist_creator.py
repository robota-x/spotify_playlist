import requests
from base64 import b64encode


class SpotifyClient:
    AUTH_ENDPOINT = 'https://accounts.spotify.com/api/token'
    SEARCH_ENDPOINT = 'https://api.spotify.com/v1/search'
    TOP_TRACKS_ENDPOINT = 'https://api.spotify.com/v1/artists/{id}/top-tracks'

    def __init__(self, file_name='credentials.txt'):
        self.client_id, self.secret = self.read_credentials(file_name)

    def read_credentials(self, file_name):
        with open(file_name, 'r') as f:
            return f.read().splitlines()[:2]

    def update_server_token(self):
        auth_string = b64encode(
            f'{self.client_id}:{self.secret}'.encode('utf-8')).decode()
        self.auth_token = requests.post(
            self.AUTH_ENDPOINT,
            data={'grant_type': 'client_credentials'},
            headers={'Authorization': f'Basic {auth_string}'}
        ).json()['access_token']

    def get_artist_by_name(self, name):
        r = requests.get(
            self.SEARCH_ENDPOINT,
            params={'q': name, 'type': 'artist', 'limit': 1},
            headers={'Authorization': f'Bearer {self.auth_token}'}
        )
        artist = r.json()['artists']['items'][0]
        return artist['id'], artist['name']

    def get_top_songs_by_artist_id(self, artist_id, country='GB'):
        r = requests.get(
            self.TOP_TRACKS_ENDPOINT.format(id=artist_id),
            params={'country': country},
            headers={'Authorization': f'Bearer {self.auth_token}'}
        )
        track_blob = r.json()['tracks']
        return [{'id': track['id'], 'name': track['name']} for track in track_blob]


# sample queries
client = SpotifyClient()

client.update_server_token()

artist_id = client.get_artist_by_name('Lady Gaga')[0]
top_songs = client.get_top_songs_by_artist_id(artist_id)

print(top_songs)
