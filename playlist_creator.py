import requests
from base64 import b64encode


def read_credentials(file_name='credentials.txt'):
    with open(file_name, 'r') as f:
        return f.read().splitlines()[:2]


def get_server_token():
    auth_endpoint = 'https://accounts.spotify.com/api/token'
    client_id, secret = read_credentials()
    auth_token = b64encode(f'{client_id}:{secret}'.encode('utf-8')).decode()
    return requests.post(
        auth_endpoint,
        data={'grant_type': 'client_credentials'},
        headers={'Authorization': f'Basic {auth_token}'}
    )


def get_artist_by_id(name, auth_token):
    search_endpoint = 'https://api.spotify.com/v1/search'
    r = requests.get(
        search_endpoint,
        params={'q': name, 'type': 'artist', 'limit': 1},
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    artist = r.json()['artists']['items'][0]
    return artist['id'], artist['name']


def get_top_songs_by_id(artist_id, auth_token, country='GB'):
    search_endpoint = 'https://api.spotify.com/v1/artists/{id}/top-tracks'
    r = requests.get(
        search_endpoint.format(id=artist_id),
        params={'country': country},
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    track_blob = r.json()['tracks']
    return [(track['id'], track['name']) for track in track_blob]


# sample queries
auth_token = get_server_token().json()['access_token']
artist_id = get_artist_by_id('Lady Gaga', auth_token)[0]
top_songs = [song[1] for song in get_top_songs_by_id(artist_id, auth_token)]

print(top_songs)
