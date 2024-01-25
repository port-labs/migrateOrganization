import requests
import json
import os

API_URL = 'https://api.getport.io/v1'

PORT_NEW_CLIENT_ID = os.getenv("PORT_NEW_CLIENT_ID")
PORT_NEW_CLIENT_SECRET = os.getenv("PORT_NEW_CLIENT_SECRET")

new_credentials = { 'clientId': PORT_NEW_CLIENT_ID, 'clientSecret': PORT_NEW_CLIENT_SECRET }
new_credentials = requests.post(f'{API_URL}/auth/access_token', json=new_credentials)
new_access_token = new_credentials.json()["accessToken"]
headers = {
    'Authorization': f'Bearer {new_access_token}'
}



print("Getting blueprints")
res = requests.get(f'{API_URL}/blueprints', headers=headers)
resp = res.json()["blueprints"]

for blueprint in resp:
    print(f"deleting entities of blueprint {blueprint['identifier']}")
    res = requests.delete(f'{API_URL}/blueprints/{blueprint["identifier"]}/all-entities', headers=headers)
    if res.ok != True:
        print("error while deleting entities: "+ json.dumps(res.json()))
    print(f"deleting blueprint {blueprint['identifier']}")
    res = requests.delete(f'{API_URL}/blueprints/{blueprint["identifier"]}', headers=headers)
    if res.ok != True:
        print("error while deleting blueprint: "+ json.dumps(res.json()))

print("Getting teams")
res = requests.get(f'{API_URL}/teams', headers=headers)
resp = res.json()["teams"]
for team in resp:
    print(f"deleting team {team['name']}")
    res = requests.delete(f'{API_URL}/teams/{team["name"]}', headers=headers)
    if res.ok != True:
        print("error while deleting team: "+ json.dumps(res.json()))