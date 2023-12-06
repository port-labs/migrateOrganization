#!/bin/bash
RUN_MODE="restore"

BACKUP_PATH=${BACKUP_PATH:-./backup.tar.gz}

IS_MIGRATE=${IS_MIGRATE:-false}
PORT_CLIENT_ID=${PORT_CLIENT_ID:-}
PORT_CLIENT_SECRET=${PORT_CLIENT_SECRET:-}

if [ $IS_MIGRATE != true ] ; then
    tar -xvzf ${BACKUP_PATH} ./bk*
fi
export PORT_NEW_CLIENT_ID=${PORT_CLIENT_ID} 
export PORT_NEW_CLIENT_SECRET=${PORT_CLIENT_SECRET}
export RUN_MODE=$RUN_MODE
python3 main.py

if [ $IS_MIGRATE != true ] ; then
    rm -rf ./bk*
fi