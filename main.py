from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_url = "https://localhost:3000/callback"

print(client_id, client_secret, redirect_url)

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
session = OAuth2Session(client_id, redirect_uri=redirect_url)

auth_base_url = "https://www.strava.com/oauth/authorize"
session.scope = ["profile:read_all"]
auth_link = session.authorization_url(auth_base_url)

print(auth_link[0])

redirect_response = input(f"Paste redirect url here: ")

token_url = "https://www.strava.com/api/v3/oauth/token"
session.fetch_token(
    token_url=token_url,
    client_id=client_id,
    client_secret=client_secret,
    authorization_response=redirect_response,
    include_client_id=True
)

response = session.get("https://www.strava.com/api/v3/athlete")

print(f"Status code: {response.status_code}")
print(f"Reason: {response.reason}")
print(f"Time: {response.elapsed}")
print(f"Response: {response.text}")