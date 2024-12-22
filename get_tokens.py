from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv, set_key
import os

load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_url = "https://localhost:3000/callback"

session = OAuth2Session(client_id, redirect_uri=redirect_url)
auth_base_url = "https://www.strava.com/oauth/authorize"
session.scope = ["activity:read_all"]
auth_link = session.authorization_url(auth_base_url)

print(f"Click here to authorize: {auth_link[0]}")
redirect_response = input(f"Paste redirect url here: ")

token_url = "https://www.strava.com/api/v3/oauth/token"
session.fetch_token(
    token_url=token_url,
    client_id=client_id,
    client_secret=client_secret,
    authorization_response=redirect_response,
    include_client_id=True
)

set_key('.env', 'ACCESS_TOKEN', session.token['access_token'])
set_key('.env', 'REFRESH_TOKEN', session.token['refresh_token'])