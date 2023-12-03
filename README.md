# Migrate Organization
This repository is for a script used to migrate Port's organizations.
This script will migrate your Blueprints, entities, scorecards, actions and teams.

During this walkthrough, we will use the terms "old" and "new". Old represents the organization you are migrating from, and new represents the organizaiton you are migrating to.

# How to use
In order to use, run in your terminal the following commands:

```
export PORT_OLD_CLIENT_ID=<ENTER OLD PORT CLIENT ID>
export PORT_OLD_CLIENT_SECRET= <ENTER OLD PORT CLIENT SECRET>
export PORT_NEW_CLIENT_ID=<ENTER NEW PORT CLIENT ID>
export PORT_NEW_CLIENT_SECRET=<ENTER NEW PORT CLIENT SECRET>

git clone https://github.com/port-labs/migrateOrganization.git

cd migrateOrganization

pip install -r ./requirements.txt

python migrate.py

```

List of required variables for the script (Port's organization credentials):
 - 'PORT_OLD_CLIENT_ID'
 - 'PORT_OLD_CLIENT_SECRET'
 - 'PORT_NEW_CLIENT_ID'
 - 'PORT_NEW_CLIENT_SECRET'

 In case you have encountered issues and would like to debug the code, you can delete the entire data from the new organization by running:

 ```
 python clean.py
 ```