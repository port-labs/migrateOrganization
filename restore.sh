#!/bin/bash

# Instructions: Before running this script, export AWS credentials:
# export AWS_ACCESS_KEY_ID="your-access-key-id"
# export AWS_SECRET_ACCESS_KEY="your-secret-access-key"
# export AWS_DEFAULT_REGION="your-default-region"
# export S3_BUCKET_NAME="your-s3-bucket-name"
# export S3_BUCKET_REGION="your-s3-bucket-region"
# export BACKUP_FILE_PATH="your-backup-path-including-file-name" 


RUN_MODE="restore"
BACKUP_FILE_PATH=${BACKUP_FILE_PATH:-"backup.tar.gz"}

IS_MIGRATE=${IS_MIGRATE:-false}
PORT_CLIENT_ID=${PORT_CLIENT_ID:-}
FORMAT=${MIGRATION_FORMAT:-"tar"}


if [ $IS_MIGRATE != true ] ; then
    if [ $FORMAT = "tar"] ; then
        if [ -n "$AWS_ACCESS_KEY_ID" ] && [ -n "$AWS_SECRET_ACCESS_KEY" ] && [ -n "$AWS_DEFAULT_REGION" ] && [ -n "$S3_BUCKET_NAME" ] && [ -n "$S3_BUCKET_REGION" ] && [ -n "$BACKUP_FILE_PATH" ] ; then
            aws s3 cp s3://$S3_BUCKET_NAME/$BACKUP_FILE_PATH . --region $S3_BUCKET_REGION
            tar -xvzf ./backup-*.tar.gz ./bk*
        else
            tar -xvzf ${BACKUP_FILE_PATH} ./bk*
        fi
    else
        if [ -n "$AWS_ACCESS_KEY_ID" ] && [ -n "$AWS_SECRET_ACCESS_KEY" ] && [ -n "$AWS_DEFAULT_REGION" ] && [ -n "$S3_BUCKET_NAME" ] && [ -n "$S3_BUCKET_REGION" ] && [ -n "$BACKUP_FILE_PATH" ] ; then
            aws s3 cp s3://$S3_BUCKET_NAME/$BACKUP_FILE_PATH . --region $S3_BUCKET_REGION
        fi
    fi
fi

export PORT_NEW_CLIENT_ID=${PORT_CLIENT_ID}
export PORT_NEW_CLIENT_SECRET=${PORT_CLIENT_SECRET}
export RUN_MODE=$RUN_MODE
python3 main.py

if [ $IS_MIGRATE != true ] ; then
    rm -rf ./bk*
fi