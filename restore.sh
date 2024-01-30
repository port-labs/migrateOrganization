#!/bin/bash

# Instructions: Before running this script, export AWS credentials:
# export AWS_ACCESS_KEY_ID="your-access-key-id"
# export AWS_SECRET_ACCESS_KEY="your-secret-access-key"
# export S3_BUCKET_REGION="your-s3-bucket-region"
# export BACKUP_FILE_PATH="your-backup-path-including-bucket-name" 
# export FILE_NAME="your-file-name"
# export MIGRATION_FORMAT="your-migration-format (tar or excel)"


RUN_MODE="restore"
BACKUP_FILE_PATH=${BACKUP_FILE_PATH:-"backup.tar.gz"}

IS_MIGRATE=${IS_MIGRATE:-false}
PORT_CLIENT_ID=${PORT_CLIENT_ID:-}
PORT_CLIENT_SECRET=${PORT_CLIENT_SECRET:-}
MIGRATION_FORMAT=${MIGRATION_FORMAT:-"tar"}


if [ $IS_MIGRATE != true ] ; then
    if [ $MIGRATION_FORMAT = "tar" ] ; then
        if [ -n "$AWS_ACCESS_KEY_ID" ] && [ -n "$AWS_SECRET_ACCESS_KEY" ] &&  [ -n "$S3_BUCKET_REGION" ] && [ -n "$BACKUP_FILE_PATH" ] ; then
            aws s3 cp s3://$BACKUP_FILE_PATH/$FILE_NAME . --region $S3_BUCKET_REGION
            tar -xvzf ./backup-*.tar.gz ./bk*
        else
            tar -xvzf ${BACKUP_FILE_PATH} ./bk*
        fi
    else
        if [ -n "$AWS_ACCESS_KEY_ID" ] && [ -n "$AWS_SECRET_ACCESS_KEY" ] && [ -n "$S3_BUCKET_REGION" ] && [ -n "$BACKUP_FILE_PATH" ] ; then
            aws s3 cp s3://$BACKUP_FILE_PATH/$FILE_NAME . --region $S3_BUCKET_REGION
        fi
    fi
fi

export PORT_NEW_CLIENT_ID=${PORT_NEW_CLIENT_ID}
export PORT_NEW_CLIENT_SECRET=${PORT_NEW_CLIENT_SECRET}
export RUN_MODE=$RUN_MODE
python3 main.py
 
# Optionally, you can remove the local backup file after uploading
# if [ $IS_MIGRATE != true ] ; then
#     rm -rf ./bk*
# fi