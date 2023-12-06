#!/bin/bash
RUN_MODE="backup"
IS_MIGRATE=${IS_MIGRATE:-false}
PORT_CLIENT_ID=${PORT_CLIENT_ID:-}
PORT_CLIENT_SECRET=${PORT_CLIENT_SECRET:-}

export PORT_OLD_CLIENT_ID=${PORT_CLIENT_ID} 
export PORT_OLD_CLIENT_SECRET=${PORT_CLIENT_SECRET}
export RUN_MODE=$RUN_MODE
python3 main.py

if [ $IS_MIGRATE != true ] ; then
    tar -czf ./backup.tar.gz ./bk*
    rm -rf ./bk*
fi

