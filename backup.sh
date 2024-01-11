#!/bin/bash

# Instructions: Before running this script, export AWS credentials:
# export AWS_ACCESS_KEY_ID="your-access-key-id"
# export AWS_SECRET_ACCESS_KEY="your-secret-access-key"
# export S3_BUCKET_REGION="your-s3-bucket-region"
# export S3_SAVE_PATH="your-s3-save-path-including-bucket-name"
# export MIGRATION_FORMAT="your-migration-format (tar or excel)"

RUN_MODE="backup"
IS_MIGRATE=${IS_MIGRATE:-false}
PORT_CLIENT_ID=${PORT_CLIENT_ID:-}


FORMAT=${MIGRATION_FORMAT:-"tar"}
export PORT_OLD_CLIENT_ID=${PORT_CLIENT_ID} 
export PORT_OLD_CLIENT_SECRET=${PORT_CLIENT_SECRET}
export RUN_MODE=$RUN_MODE
python3 main.py

format_time=$(date +%Y-%m-%dT%H-%M-%S)
if [ $IS_MIGRATE == false ] ; then
    if [ $FORMAT == "excel" ] ; then
        if [ -n "$AWS_ACCESS_KEY_ID" ] && [ -n "$AWS_SECRET_ACCESS_KEY" ] && [ -n "$S3_BUCKET_REGION" ] && [ -n "$S3_SAVE_PATH" ]; then
        # Upload the backup to S3 if it's a backup
        aws s3 cp ./bk-data.xlsx s3://$S3_SAVE_PATH/backup-${format_time}.xlsx  --region $S3_BUCKET_REGION
        echo "Backup uploaded to S3, path: s3://$S3_SAVE_PATH/backup-${format_time}.xlsx"
        fi
    else
    tar -czf ./backup-${format_time}.tar.gz ./bk*
    rm -rf ./bk*
    if [ -n "$AWS_ACCESS_KEY_ID" ] && [ -n "$AWS_SECRET_ACCESS_KEY" ] && [ -n "$S3_BUCKET_REGION" ] && [ -n "$S3_SAVE_PATH" ]; then
        # Upload the backup to S3 if it's a backup
        aws s3 cp ./backup.tar.gz s3://$S3_SAVE_PATH/backup-${format_time}.tar.gz  --region $S3_BUCKET_REGION
        echo "Backup uploaded to S3, path: s3://$S3_SAVE_PATH/backup-${format_time}.tar.gz"
    fi
    # Optionally, you can remove the local backup file after uploading
    # rm -f ./backup-*.tar.gz
    fi
fi
