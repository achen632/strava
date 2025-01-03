from requests_oauthlib import OAuth2Session
import requests
from dotenv import load_dotenv, set_key
import os

# Retrieve auth tokens from Strava after user authorization
def get_tokens():
    # Load environment variables
    load_dotenv()
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    redirect_url = "https://localhost:3000/callback"

    # Create session and get authorization link
    session = OAuth2Session(client_id, redirect_uri=redirect_url)
    auth_base_url = "https://www.strava.com/oauth/authorize"
    session.scope = ["activity:read_all"]
    auth_link = session.authorization_url(auth_base_url)

    # Get user authorization
    print(f"Click here to authorize: {auth_link[0]}")
    redirect_response = input(f"Paste redirect url here: ")

    # Get tokens
    token_url = "https://www.strava.com/api/v3/oauth/token"
    session.fetch_token(
        token_url=token_url,
        client_id=client_id,
        client_secret=client_secret,
        authorization_response=redirect_response,
        include_client_id=True
    )

    # Save tokens to .env file
    set_key('.env', 'ACCESS_TOKEN', session.token['access_token'])
    set_key('.env', 'REFRESH_TOKEN', session.token['refresh_token'])

# Refresh tokens
def refresh_tokens():
    # Load environment variables
    load_dotenv()
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    refresh_token = os.getenv('REFRESH_TOKEN')

    # POST request
    token_url = "https://www.strava.com/api/v3/oauth/token"
    response = requests.post(
        token_url,
        data={
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
    )

    if response.status_code == 200:
        tokens = response.json()
        new_refresh_token = tokens['refresh_token']
        if new_refresh_token == refresh_token:
            return # No need to update
        new_access_token = tokens['access_token']

        # Update the .env file
        set_key('.env', 'ACCESS_TOKEN', new_access_token)
        set_key('.env', 'REFRESH_TOKEN', new_refresh_token)

        print("Refreshed tokens")
    else:
        print("Failed to refresh tokens:", response.status_code, response.text)

# Return JSON of user's activities
def get_activities(num_activities=10):
    # Load environment variables
    refresh_tokens()
    load_dotenv()
    access_token = os.getenv('ACCESS_TOKEN')

    # GET request
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'page': 1, 'per_page': num_activities}
    response = requests.get(url, headers=headers, params=params)

    return response.json()