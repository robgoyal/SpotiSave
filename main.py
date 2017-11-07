import requests
import base64

client_id = ""
client_secret = ""

auth_string = 'Basic ' + base64.b64encode(bytes(client_id + ':' + client_secret, 'utf-8')).decode('ascii')

# Setup access token information
header = {'Authorization': auth_string}
payload = {'grant_type': 'client_credentials'}
url = 'https://accounts.spotify.com/api/token'

# Request access token
r = requests.post(url, data = payload, headers = header)

auth_token = r.json()['access_token']