#!/bin/bash

# Instructions: Before running this script, export AWS credentials:
# export AWS_ACCESS_KEY_ID="your-access-key-id"
# export AWS_SECRET_ACCESS_KEY="your-secret-access-key"
# export AWS_DEFAULT_REGION="your-default-region"

RUN_MODE="backup"
IS_MIGRATE=${IS_MIGRATE:-false}
PORT_CLIENT_ID=${PORT_CLIENT_ID:-}

# S3 bucket name and region (modify accordingly)
S3_BUCKET_NAME="your-s3-bucket-name"
S3_BUCKET_REGION="your-s3-bucket-region"

export PORT_OLD_CLIENT_ID=${PORT_CLIENT_ID}
export PORT_OLD_CLIENT_SECRET=${PORT_CLIENT_SECRET}
export RUN_MODE=$RUN_MODE
python3 main.py

if [ $IS_MIGRATE != true ] ; then
    tar -czf ./backup.tar.gz ./bk*
    rm -rf ./bk*

    # Upload the backup to S3 if it's a backup
    aws s3 cp ./backup.tar.gz s3://$S3_BUCKET_NAME/ --region $S3_BUCKET_REGION

    # Optionally, you can remove the local backup file after uploading
    rm -f ./backup.tar.gz
fi
