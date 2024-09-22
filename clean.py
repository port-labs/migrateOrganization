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

systemBlueprints = ["_user", "_team"]

print("Deleting actions")
res = requests.get(f'{API_URL}/actions?version=v2', headers=headers)
actions = res.json()["actions"]
for action in actions:
    print(f"deleting action {action['identifier']}")
    res = requests.delete(f'{API_URL}/actions/{action["identifier"]}', headers=headers)
    if res.ok != True:
        print("error while deleting action: "+ json.dumps(res.json()))

print("Deleting pages")
res = requests.get(f'{API_URL}/pages', headers=headers)
pages = res.json()["pages"]
for page in pages:
    print(f"deleting page {page['identifier']}")
    res = requests.delete(f'{API_URL}/pages/{page["identifier"]}', headers=headers)
    if res.ok != True:
        print("error while deleting page: "+ json.dumps(res.json()))

print("Getting blueprints")
res = requests.get(f'{API_URL}/blueprints', headers=headers)
blueprints = res.json()["blueprints"]
failed_blueprints = []

for blueprint in blueprints:
    if blueprint["identifier"] not in systemBlueprints:
        print(f"Deleting entities of blueprint {blueprint['identifier']}")
        res = requests.delete(f'{API_URL}/blueprints/{blueprint["identifier"]}/all-entities', headers=headers)
        if not res.ok:
            print(f"Error while deleting entities: {json.dumps(res.json())}")
            failed_blueprints.append(blueprint["identifier"])
            continue

        print(f"Deleting blueprint {blueprint['identifier']}")
        res = requests.delete(f'{API_URL}/blueprints/{blueprint["identifier"]}', headers=headers)
        if not res.ok:
            print(f"Error while deleting blueprint: {json.dumps(res.json())}")
            failed_blueprints.append(blueprint["identifier"])

    return failed_blueprints

for attempt in range(5):
    if not failed_blueprints:
        break

    print(f"Retrying deletion... Attempt {attempt + 1}")
    remaining_failed = []

    for identifier in failed_blueprints:
        print(f"Retrying deletion of blueprint {identifier}")
        res = requests.delete(f'{API_URL}/blueprints/{identifier}/all-entities', headers=headers)
        if not res.ok:
            print(f"Error while deleting entities: {json.dumps(res.json())}")
            remaining_failed.append(identifier)
            continue

        res = requests.delete(f'{API_URL}/blueprints/{identifier}', headers=headers)
        if not res.ok:
            print(f"Error while deleting blueprint: {json.dumps(res.json())}")
            remaining_failed.append(identifier)

    failed_blueprints = remaining_failed
    if failed_blueprints:
        print(f"Some deletions still failed. Retrying in 5 seconds...")
        time.sleep(5)

if failed_blueprints:
    print(f"Failed to delete the following blueprints after {retries} attempts: {failed_blueprints}")
else:
    print("All blueprints deleted successfully.")


print("Getting teams")
res = requests.get(f'{API_URL}/teams', headers=headers)
resp = res.json()["teams"]
for team in resp:
    print(f"deleting team {team['name']}")
    res = requests.delete(f'{API_URL}/teams/{team["name"]}', headers=headers)
    if res.ok != True:
        print("error while deleting team: "+ json.dumps(res.json()))