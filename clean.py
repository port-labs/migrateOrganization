import requests
import json

API_URL = 'https://api.getport.io/v1'

NEW_CLIENT_ID = "" # or set to os.getenv("NEW_CLIENT_ID")
NEW_CLIENT_SECRET = "" # or set to os.getenv("NEW_CLIENT_SECRET")

new_credentials = { 'clientId': NEW_CLIENT_ID, 'clientSecret': NEW_CLIENT_SECRET }
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