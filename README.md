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
 First, select the backup format by running(and leaving the desire format):
 
 ```
 export MIGRATION_FORMAT="tar"/"excel"
 ```

 In order to run a partial backup, insert the blueprints identifiers into the `specificBlueprints` array at the beginning of `main.py` file.

 The script only support filenames named `backup-(timestamp).tar.gz`. For the script to work, do not change the name of the backup file.

 If you're interested in pushing the backfile to an S3 Bucket, first run the following commands in your terminal (exporting AWS credentials):

```
export AWS_ACCESS_KEY_ID="your-access-key-id"
export AWS_SECRET_ACCESS_KEY="your-secret-access-key"
export S3_BUCKET_REGION="your-s3-bucket-region"
export S3_SAVE_PATH="your-s3-save-path-including-bucket-name"
```

 Then, run the following commands in your terminal (remember to insert Port's credentials):

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
 First, select the format you restore data from by runnig(and leaving the desired format):
 
 ```
 export MIGRATION_FORMAT="tar"/"excel"
 ```

 The script only support filenames named `backup-(timestamp).tar.gz`. For the script to work, do not change the name of the backup file.

 If you want to restore the backup file from your S3 Bucket, first run the following commands (export your AWS credentials):
 If your file is backed up on S3 bucket, the s3 bucket name in the path. Otherwise, specify the local path to it.
```
export AWS_ACCESS_KEY_ID="your-access-key-id"
export AWS_SECRET_ACCESS_KEY="your-secret-access-key"
export S3_BUCKET_REGION="your-s3-bucket-region"
export BACKUP_FILE_PATH="your-backup-path-including-bucket-name" 
export FILE_NAME="your-file-name"
```

Then, run the following commands in your terminal (remember to insert Port's credentials):

 ```
export PORT_CLIENT_ID=<ENTER PORT CLIENT ID>
export PORT_CLIENT_SECRET=<ENTER PORT CLIENT SECRET>

git clone https://github.com/port-labs/migrateOrganization.git

cd migrateOrganization

pip install -r ./requirements.txt
 ```

 Then, place your tar.gz backup file inside the directory, or edit the restore.sh file and set BACKUP_PATH to the path of the backupfile and run:
 ```
bash restore.sh
```

 The script extract the backup files, read them and send the data into Port.