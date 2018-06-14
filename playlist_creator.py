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

def search_artist_id(name, auth_token):
    search_endpoint = 'https://api.spotify.com/v1/search'
    r = requests.get(
        search_endpoint,
        params={'q': name, 'type': 'artist', 'limit': 1},
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    artist = r.json()['artists']['items'][0]
    return artist['id'], artist['name']

# sample queries
auth_token = get_server_token().json()['access_token']
sample_query = search_artist_id('Lady Gaga', auth_token)
print(sample_query)