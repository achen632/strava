import requests
from dotenv import load_dotenv
import os

load_dotenv()
access_token = os.getenv('ACCESS_TOKEN')

url = "https://www.strava.com/api/v3/athlete/activities"
headers = {'Authorization': f'Bearer {access_token}'}
params = {'page': 1, 'per_page': 10}

response = requests.get(url, headers=headers, params=params)

for i, x in enumerate(response.json()):
    print(i+1, x['name'])