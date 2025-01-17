#!/bin/bash

NL=`echo -ne '\015'`
EXCALIBUR_CMD="./start-excalibur.sh 5002"
EXCALIBUR_LOGFILE="screen-excalibur.log"
SCREEN=$(which screen)
if [[ -n "$SCREEN" ]]; then
    SESSION=$(screen -ls | awk '/[0-9]\.Virtue/ { print $1 }')
    echo "Current Screens are [$SESSION]"
    if [[ ! -n "$SESSION" ]]; then
        screen -S Virtue -t excalibur -d -m bash
        sleep 1
        CURRENT_SESSION=$(screen -ls | awk '/[0-9]\.Virtue/ { print $1 }')
        echo "Current Session is [$CURRENT_SESSION]"
        screen -S $CURRENT_SESSION -p excalibur -X logfile $EXCALIBUR_LOGFILE
        screen -S $CURRENT_SESSION -p excalibur -X log on
        screen -S $CURRENT_SESSION -p excalibur -X stuff "$EXCALIBUR_CMD $NL"
    fi
fi
