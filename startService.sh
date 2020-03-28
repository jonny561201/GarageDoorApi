#!/usr/bin/env bash


GARAGE_SERVICE_FILE=garageDoor.service


function stopService {
    sudo systemctl stop ${GARAGE_SERVICE_FILE}
}

function copyServiceFile {
    sudo chmod 644 ${GARAGE_SERVICE_FILE}
    sudo cp ${GARAGE_SERVICE_FILE} /etc/systemd/system/${GARAGE_SERVICE_FILE}
}

function configureSystemD {
    sudo systemctl daemon-reload
    sudo systemctl enable ${GARAGE_SERVICE_FILE}
}


stopService
copyServiceFile
configureSystemD