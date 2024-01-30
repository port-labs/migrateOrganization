import json
import requests
import os
import copy
import pandas as pd
import math
import openpyxl
 
API_URL = 'https://api.getport.io/v1'

global error 
error = False
global teamError
teamError = False
FORMAT = os.getenv("MIGRATION_FORMAT", "tar") #Format = tar or excel

#Selective format = In case you are interested in only backing up specific blueprints, specify them here by adding their identifiers to the array. If the array is empty, all blueprints will be backed up.
# Example format: 
# specificBlueprints = ["blueprint1", "blueprint2"]

specificBlueprints = []

SPECIFIC = False
if specificBlueprints:
    SPECIFIC = True

#The purpose of this script is to copy data between organization. It will copy Blueprints, Entities, Actions, Scorecards, Teams and Users.
#Fill in the secrets or set them as environment variables

PORT_OLD_CLIENT_ID = os.getenv("PORT_OLD_CLIENT_ID", "")
PORT_OLD_CLIENT_SECRET = os.getenv("PORT_OLD_CLIENT_SECRET", "")
PORT_NEW_CLIENT_ID = os.getenv("PORT_NEW_CLIENT_ID", "")
PORT_NEW_CLIENT_SECRET = os.getenv("PORT_NEW_CLIENT_SECRET", "")
RUN_MODE = os.getenv("RUN_MODE", "backup")

if PORT_OLD_CLIENT_ID != "" or PORT_OLD_CLIENT_SECRET != "":
    old_credentials = { 'clientId': PORT_OLD_CLIENT_ID, 'clientSecret': PORT_OLD_CLIENT_SECRET }
    old_credentials = requests.post(f'{API_URL}/auth/access_token', json=old_credentials)
    old_access_token = old_credentials.json()["accessToken"]
    old_headers = {
        'Authorization': f'Bearer {old_access_token}'
    }

if PORT_NEW_CLIENT_ID != "" or PORT_NEW_CLIENT_SECRET != "":
    new_credentials = { 'clientId': PORT_NEW_CLIENT_ID, 'clientSecret': PORT_NEW_CLIENT_SECRET }
    new_credentials = requests.post(f'{API_URL}/auth/access_token', json=new_credentials)
    new_access_token = new_credentials.json()["accessToken"]
    new_headers = {
        'Authorization': f'Bearer {new_access_token}'
    }

def getSpecificBlueprints(blueprints):
    returnBlueprints = []
    for blueprint in blueprints:
        print(f"Getting blueprint {blueprint}")
        res = requests.get(f'{API_URL}/blueprints/{blueprint}', headers=old_headers)
        resp = res.json()["blueprint"]
        returnBlueprints.append(resp)
    return returnBlueprints

def getBlueprints():
    print("Getting blueprints")
    res = requests.get(f'{API_URL}/blueprints', headers=old_headers)
    resp = res.json()["blueprints"]
    return resp

def getSpecificScorecards(blueprints):
    returnScorecards = []
    for blueprint in blueprints:
        print(f"Getting scorecards for blueprint {blueprint}")
        res = requests.get(f'{API_URL}/blueprints/{blueprint}/scorecards', headers=old_headers)
        resp = res.json()["scorecards"]
        returnScorecards += resp
    return returnScorecards

def getScorecards():
    print("Getting scorecards")
    res = requests.get(f'{API_URL}/scorecards', headers=old_headers)
    resp = res.json()["scorecards"]
    return resp

def getSpecificActions(blueprints):
    returnActions = []
    for blueprint in blueprints:
        print(f"Getting actions for blueprint {blueprint}")
        res = requests.get(f'{API_URL}/blueprints/{blueprint}/actions', headers=old_headers)
        resp = res.json()["actions"]
        returnActions += resp
    return returnActions

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

def getEntites(blueprint):
    print(f"Getting entities for {blueprint}")
    res = requests.get(f'{API_URL}/blueprints/{blueprint}/entities', headers=old_headers)
    resp = res.json()["entities"]
    return resp

def postBlueprints(blueprints):
    global error
    print("Posting blueprints")
    cleanBP = copy.deepcopy(blueprints)
    relationsBP = copy.deepcopy(blueprints)
    for bp in cleanBP:       # send blueprint without relations and mirror properties
        print(f"posting blueprint {bp['identifier']} without relations, mirrors and aggregations")
        if bp.get("teamInheritance") is not None:
            bp.pop("teamInheritance", None)
        bp["aggregationProperties"] = {}
        bp["relations"] = {}
        bp["mirrorProperties"] = {}
        res = requests.post(f'{API_URL}/blueprints', headers=new_headers, json=bp)
        if res.ok != True:
            print("error posting blueprint:" + json.dumps(res.json()))
            error = True
    for blueprint in relationsBP:      # send blueprint with relations
        print(f"patching blueprint {blueprint['identifier']} with relations")
        if blueprint.get("teamInheritance") is not None: 
            blueprint.pop("teamInheritance", None)
        blueprint["aggregationProperties"] = {} 
        blueprint["mirrorProperties"] = {}
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

def postExcelEntities(entities, blueprints):
    for item in entities.values():
        for entity in item:
            bp_object = next((bp for bp in blueprints if bp["identifier"] == entity["blueprint"]), None)
            if bp_object.get("teamInheritance") is not None:
                entity.pop("team", None)
            if entity.get("icon") is None:
                entity.pop("icon", None)
            print(f"posting entity {entity['identifier']}")
            res = requests.post(f'{API_URL}/blueprints/{entity["blueprint"]}/entities?upsert=true&validation_only=false&create_missing_related_entities=true&merge=true', headers=new_headers, json=entity)
            if res.ok != True:
                print("error posting entity:" + json.dumps(res.json()))
                error = True

def postEntities(entities, blueprints):
    global error
    for blueprint in entities:
        removeTeam = False
        print(f"posting entities for blueprint {blueprint}")
        bp_object = next((bp for bp in blueprints if bp["identifier"] == blueprint), None)
        if bp_object.get("teamInheritance") is not None:
            removeTeam = True
        for entity in entities[blueprint]:
            if entity["icon"] is None:
                entity.pop("icon", None)
            if removeTeam:
                entity.pop("team", None)
            res = requests.post(f'{API_URL}/blueprints/{blueprint}/entities?upsert=true&validation_only=false&create_missing_related_entities=true&merge=true', headers=new_headers, json=entity)
            if res.ok != True:
                print("error posting entity:" + json.dumps(res.json()))
                error = True

def postScorecards(scorecards):
    global error
    print("Posting scorecards")
    for scorecard in scorecards:
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
        if pd.isna(action.get("description", "")): # check if description is NaN
            action["description"] = "" # set description to empty string
        if pd.isna(action.get("icon", "Microservice")): # check if icon is NaN
            action["icon"] = "" # set icon to empty string
        action.pop("createdAt", None)
        action.pop("updatedAt", None)
        action.pop("createdBy", None)
        action.pop("updatedBy", None)
        res = requests.post(f'{API_URL}/blueprints/{blueprint}/actions', headers=new_headers, json=action)
        if res.ok != True:
            print(f"error posting action: " + json.dumps(res.json()))
            teamError = True

def parser(data):
    for item in data:
        for key in item:
            if type(item[key]) == str:
                try:
                    item[key] = json.loads(item[key])
                except:
                    pass
            elif math.isnan(item[key]):
                item[key] = None
            else:
                pass
    return data

def postTeams(teams):
    global error
    print("Posting teams")
    for team in teams:
        if pd.isna(team.get("description", "")): # check if description is NaN
            team["description"] = "" # set description to empty string
        res = requests.post(f'{API_URL}/teams', headers=new_headers, json=team)
        if res.ok != True:
            print(f"error posting team {team['name']} :" + json.dumps(res.json()))
            error = True

def main(): 
    if RUN_MODE == "backup" or RUN_MODE == "migrate":
        if SPECIFIC: #check if we are backing up specific blueprints
            blueprints = getSpecificBlueprints(specificBlueprints)
            scorecards = getSpecificScorecards(specificBlueprints)
            actions = getSpecificActions(specificBlueprints)
        else: 
            blueprints = getBlueprints()
            scorecards = getScorecards()
            actions = getActions()
        teams = getTeams()
        entities = {}
        for blueprint in blueprints:
            bp_id = blueprint["identifier"]
            entities[bp_id] = getEntites(bp_id)
        if RUN_MODE == "backup":
            if FORMAT == "tar": 
                with open('bk-blueprints.json', 'w') as outfile:
                    json.dump(blueprints, outfile)
                with open('bk-scorecards.json', 'w') as outfile:
                    json.dump(scorecards, outfile)
                with open('bk-actions.json', 'w') as outfile:
                    json.dump(actions, outfile)
                with open('bk-teams.json', 'w') as outfile:
                    json.dump(teams, outfile)
                with open('bk-entities.json', 'w') as outfile:
                  json.dump(entities, outfile)
            else:
                df_blueprints = pd.DataFrame(blueprints).map(lambda x: json.dumps(x) if isinstance(x, dict) or isinstance(x,list) else x)
                df_scorecards = pd.DataFrame(scorecards).map(lambda x: json.dumps(x) if isinstance(x, dict) or isinstance(x,list) else x)
                df_actions = pd.DataFrame(actions).map(lambda x: json.dumps(x) if isinstance(x, dict) or isinstance(x,list) else x)
                df_teams = pd.DataFrame(teams).map(lambda x: json.dumps(x) if isinstance(x, dict) or isinstance(x,list) else x)
                with pd.ExcelWriter('bk-data.xlsx') as writer:
                    df_blueprints.to_excel(writer, sheet_name='Blueprints', index=False)
                    df_scorecards.to_excel(writer, sheet_name='Scorecards', index=False)
                    df_actions.to_excel(writer, sheet_name='Actions', index=False)
                    df_teams.to_excel(writer, sheet_name='Teams', index=False)
                    for blueprint, entity_list in entities.items():
                        for entity in entity_list:
                            for key in entity["properties"]:
                                 entity[f"prop_{key}"] = entity["properties"][key]
                            for key in entity["relations"]:
                                entity[f"rel_{key}"] = entity["relations"][key]
                            entity.pop("properties", None)
                            entity.pop("scorecardsStats", None)
                            entity.pop("relations", None)
                        df = pd.DataFrame(entity_list).map(lambda x: json.dumps(x) if isinstance(x, dict) or isinstance(x,list) else x)
                        df.to_excel(writer, sheet_name=blueprint, index=False)

    if RUN_MODE == "migrate" or RUN_MODE == "restore":
        if RUN_MODE == "restore":
            if FORMAT == "tar": 
                with open('bk-blueprints.json') as json_file:
                    blueprints = json.load(json_file)
                with open('bk-scorecards.json') as json_file:
                    scorecards = json.load(json_file)
                with open('bk-actions.json') as json_file:
                    actions = json.load(json_file)
                with open('bk-teams.json') as json_file:
                    teams = json.load(json_file)
                with open('bk-entities.json') as json_file:
                    entities = json.load(json_file)
            else: 
                blueprints = parser(pd.read_excel(os.getenv("FILE_NAME"), sheet_name='Blueprints').to_dict(orient='records'))
                scorecards = parser((pd.read_excel(os.getenv("FILE_NAME"), sheet_name='Scorecards').to_dict(orient='records')))
                actions = parser((pd.read_excel(os.getenv("FILE_NAME"), sheet_name='Actions').to_dict(orient='records')))
                teams = parser((pd.read_excel(os.getenv("FILE_NAME"), sheet_name='Teams').to_dict(orient='records')))
                entities = {}
                sheet_names = pd.ExcelFile(os.getenv("FILE_NAME")).sheet_names
                for sheet in sheet_names:
                    if sheet not in ['Blueprints', 'Scorecards', 'Actions', 'Teams']:  # Skip non-entity sheets
                        df = parser(pd.read_excel(os.getenv("FILE_NAME"), sheet_name=sheet).to_dict(orient='records'))
                        for entity in df:
                            entity["properties"] = {}
                            entity["relations"] = {}
                            initial_entity = dict(entity)
                            for key, value in initial_entity.items():
                                if value is None:
                                    entity.pop(key)
                                elif key.startswith("prop_"):
                                    entity["properties"][key[5:]] = value
                                    entity.pop(key)
                                elif key.startswith("rel_"):
                                    entity["relations"][key[4:]] = value
                                    entity.pop(key)
                        entities[sheet] = df
        postBlueprints(blueprints)
        postScorecards(scorecards)
        postActions(actions)
        postTeams(teams)
        if FORMAT == "tar":
            postEntities(entities, blueprints)
        else:
            postExcelEntities(entities, blueprints)
    if error:
        print("Errors occured during migration, please check logs")
    elif teamError:
        print("Errors occured during teams migration, please check logs")
    else:
        print("No errors were caught during migration")
    
if __name__ == "__main__":
    main()
