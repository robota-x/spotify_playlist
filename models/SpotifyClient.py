import requests
from base64 import b64encode


class SpotifyClient:
    AUTH_ENDPOINT = 'https://accounts.spotify.com/api/token'
    SEARCH_ENDPOINT = 'https://api.spotify.com/v1/search'
    TOP_TRACKS_ENDPOINT = 'https://api.spotify.com/v1/artists/{id}/top-tracks'

    def __init__(self, file_name='credentials.txt'):
        self.client_id, self.secret = self._read_credentials(file_name)
        self._update_server_token()

    def _read_credentials(self, file_name):
        with open(file_name, 'r') as f:
            return f.read().splitlines()[:2]

    def _api_request(self, endpoint, method='get', headers=None, data=None, params=None):
        r = getattr(requests, method)(
            endpoint,
            params=params,
            data=data,
            headers=headers or {'Authorization': f'Bearer {self.auth_token}'}
        )
        r.raise_for_status()
        return r.json()

    def _update_server_token(self):
        auth_string = b64encode(
            f'{self.client_id}:{self.secret}'.encode('utf-8')).decode()

        self.auth_token = self._api_request(
            self.AUTH_ENDPOINT,
            data={'grant_type': 'client_credentials'},
            headers={'Authorization': f'Basic {auth_string}'},
            method='post'
        )['access_token']


    def get_artist_by_name(self, name, strict=True):
        res = requests.get(
            self.SEARCH_ENDPOINT,
            params={'q': name, 'type': 'artist', 'limit': 1},
            headers={'Authorization': f'Bearer {self.auth_token}'}
        ).json()

        if len(res):
            artist = res['artists']['items'][0]
            return name.lower() == artist['name'].lower() and artist['id'] if strict else artist['id']

    def get_top_songs_by_artist_id(self, artist_id, country='GB'):
        res = requests.get(
            self.TOP_TRACKS_ENDPOINT.format(id=artist_id),
            params={'country': country},
            headers={'Authorization': f'Bearer {self.auth_token}'}
        ).json()

        track_blob = res['tracks']
        return [{'id': track['id'], 'name': track['name']} for track in track_blob]


# # sample queries
# client = SpotifyClient()

# artist_id = client.get_artist_by_name('Lady gaga')
# top_songs = client.get_top_songs_by_artist_id(artist_id)

# print(top_songs)
