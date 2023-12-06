# Migrate Organization
This repository is for a script used to migrate Port's organizations.
This script will migrate your Blueprints, entities, scorecards, actions and teams.

This script can also be used to backup and restore your Port data.

# How to migrate
In order to use, run in your terminal the following commands:

```
export PORT_OLD_CLIENT_ID=<ENTER OLD PORT CLIENT ID>
export PORT_OLD_CLIENT_SECRET= <ENTER OLD PORT CLIENT SECRET>
export PORT_NEW_CLIENT_ID=<ENTER NEW PORT CLIENT ID>
export PORT_NEW_CLIENT_SECRET=<ENTER NEW PORT CLIENT SECRET>

git clone https://github.com/port-labs/migrateOrganization.git

cd migrateOrganization

pip install -r ./requirements.txt

bash migrate.sh

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

 # How to Backup
 In order to backup your data, run the following commands in your terminal (remember to insert Port's credentials):

 ```
export PORT_CLIENT_ID=<ENTER PORT CLIENT ID>
export PORT_CLIENT_SECRET= <ENTER PORT CLIENT SECRET>

git clone https://github.com/port-labs/migrateOrganization.git

cd migrateOrganization

pip install -r ./requirements.txt

bash backup.sh
 ```

 This will create a tar.gz file in the directory, which will contain the data from your Port's organization

 # How to restore
 In order to restore data from a backup file, run the following commands in your terminal  (remember to insert the Port's credentials):

 ```
export PORT_CLIENT_ID=<ENTER PORT CLIENT ID>
export PORT_CLIENT_SECRET= <ENTER PORT CLIENT SECRET>

git clone https://github.com/port-labs/migrateOrganization.git

cd migrateOrganization

pip install -r ./requirements.txt
 ```

 Then, place your tar.gz backup file inside the directory, or edit the restore.sh file and set BACKUP_PATH to the path of the backupfile and run:
 ```
bash restore.sh
```

 The script extract the backup files, read them and send the data into Port.