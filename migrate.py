import json
import requests
import os
import copy

API_URL = 'https://api.getport.io/v1'

global error 
error = False
global teamError
teamError = False

#The purpose of this script is to copy data between organization. It will copy Blueprints, Entities, Actions, Scorecards, Teams and Users.
#Fill in the secrets or set them as environment variables

PORT_OLD_CLIENT_ID = "" # or set to os.getenv("PORT_OLD_CLIENT_ID")
PORT_OLD_CLIENT_SECRET = "" # or set to os.getenv("PORT_OLD_CLIENT_SECRET")
PORT_NEW_CLIENT_ID = "" # or set to os.getenv("PORT_NEW_CLIENT_ID")
PORT_NEW_CLIENT_SECRET = "" # or set to os.getenv("PORT_NEW_CLIENT_SECRET")

old_credentials = { 'clientId': PORT_OLD_CLIENT_ID, 'clientSecret': PORT_OLD_CLIENT_SECRET }
old_credentials = requests.post(f'{API_URL}/auth/access_token', json=old_credentials)
old_access_token = old_credentials.json()["accessToken"]
old_headers = {
    'Authorization': f'Bearer {old_access_token}'
}

new_credentials = { 'clientId': PORT_NEW_CLIENT_ID, 'clientSecret': PORT_NEW_CLIENT_SECRET }
new_credentials = requests.post(f'{API_URL}/auth/access_token', json=new_credentials)
new_access_token = new_credentials.json()["accessToken"]
new_headers = {
    'Authorization': f'Bearer {new_access_token}'
}


def getBlueprints():
    print("Getting blueprints")
    res = requests.get(f'{API_URL}/blueprints', headers=old_headers)
    resp = res.json()["blueprints"]
    return resp

def getScorecards():
    print("Getting scorecards")
    res = requests.get(f'{API_URL}/scorecards', headers=old_headers)
    resp = res.json()["scorecards"]
    return resp

def getActions():
    print("Getting actions")
    res = requests.get(f'{API_URL}/actions', headers=old_headers)
    resp = res.json()["actions"]
    return resp

def getTeams():
    print("Getting teams")
    res = requests.get(f'{API_URL}/teams', headers=old_headers)
    resp = res.json()["teams"]
    return resp

def postBlueprints(blueprints):
    global error
    print("Posting blueprints")
    cleanBP = copy.deepcopy(blueprints)
    relationsBP = copy.deepcopy(blueprints)
    for bp in cleanBP:       # send blueprint without relations and mirror properties
        print(f"posting blueprint {bp['identifier']}")
        bp.get("relations").clear()
        bp.get("mirrorProperties").clear()
        res = requests.post(f'{API_URL}/blueprints', headers=new_headers, json=bp)
        if res.ok != True:
            print("error posting blueprint:" + json.dumps(res.json()))
            error = True
    for blueprint in relationsBP:      # send blueprint with relations
        print(f"patching blueprint {blueprint['identifier']} with relations")
        blueprint.get("mirrorProperties").clear()
        res = requests.patch(f'{API_URL}/blueprints/{blueprint["identifier"]}', headers=new_headers, json=blueprint)
        if res.ok != True:
            print("error patching blueprint:" + json.dumps(res.json()))
            error = True
    for blueprint in blueprints:       # send blueprint with everything
        print(f"patching blueprint {blueprint['identifier']} with mirror properties")
        res = requests.patch(f'{API_URL}/blueprints/{blueprint["identifier"]}', headers=new_headers, json=blueprint)
        if res.ok != True:
            print("error patching blueprint:" + json.dumps(res.json()))
            error = True

def postEntities(blueprints):
    global error
    for blueprint in blueprints:
        print(f"getting entities for blueprint {blueprint['identifier']}")
        res = requests.get(f'{API_URL}/blueprints/{blueprint["identifier"]}/entities', headers=old_headers)
        resp = res.json()["entities"]
        for entity in resp:
            if entity["icon"] is None:
                entity.pop("icon", None)
            res = requests.post(f'{API_URL}/blueprints/{blueprint["identifier"]}/entities?upsert=true&validation_only=false&create_missing_related_entities=true&merge=false', headers=new_headers, json=entity)
            if res.ok != True:
                print("error posting entity:" + json.dumps(res.json()))
                error = True

def postScorecards(scorecards):
    global error
    print("Posting scorecards")
    for scorecard in scorecards:
        print(f"posting scorecard {scorecard['identifier']}")
        scorecard.pop("id", None)
        scorecard.pop("createdAt", None)
        scorecard.pop("updatedAt", None)
        scorecard.pop("createdBy", None)
        scorecard.pop("updatedBy", None)
        blueprint = scorecard.pop("blueprint", None)
        res = requests.post(f'{API_URL}/blueprints/{blueprint}/scorecards', headers=new_headers, json=scorecard)
        if res.ok != True:
            print(f"error posting scorecard:" + json.dumps(res.json()))
            error = True


def postActions(actions):
    global teamError
    print("Posting actions")
    for action in actions:
        print(f"posting action {action['identifier']}")
        action.pop("id", None)
        blueprint = action.pop("blueprint", None)
        action.pop("createdAt", None)
        action.pop("updatedAt", None)
        action.pop("createdBy", None)
        action.pop("updatedBy", None)
        res = requests.post(f'{API_URL}/blueprints/{blueprint}/actions', headers=new_headers, json=action)
        if res.ok != True:
            print(f"error posting action: " + json.dumps(res.json()))
            teamError = True


def postTeams(teams):
    global error
    print("Posting teams")
    for team in teams:
        res = requests.post(f'{API_URL}/teams', headers=new_headers, json=team)
        if res.ok != True:
            print(f"error posting team {team['name']} :" + json.dumps(res.json()))
            error = True


def main():
    blueprints = getBlueprints()
    postBlueprints(blueprints)
    scorecards = getScorecards()
    postScorecards(scorecards)
    actions = getActions()
    postActions(actions)
    teams = getTeams()
    postTeams(teams)
    postEntities(blueprints)

    if error:
        print("Errors occured during migration, please check logs")
    elif teamError:
        print("Errors occured during teams migration, please check logs")
    else:
        print("No errors were caught during migration")
    
if __name__ == "__main__":
    main()