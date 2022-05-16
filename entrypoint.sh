#!/bin/bash

USER=$1
USER_ID=$2

echo -n "Creating user $USER... "
egrep "^$USER" /etc/passwd >/dev/null
if [ $? -eq 0 ]; then
    echo "$USER already exists."
    exit 0
else
    useradd --create-home --shell /bin/bash $USER --uid $USER_ID
    if [ $? -eq 0 ]; then
        echo "done."
    else
        echo "failed."
        exit 1
    fi
fi

runuser -u $USER -- python3 /scripts/main.py "${@:3}"