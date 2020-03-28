#!/usr/bin/env bash


GARAGE_SERVICE_FILE=garageDoor.service


function cloneServiceFiles {
    if [[ -d "/home/pi/GarageDoorApi" ]]
    then
        echo "Directory exists."
        cd /home/pi/GarageDoorApi
        git pull
    else
        echo "Directory does not exist."
        cd /home/pi/
        git clone https://github.com/jonny561201/GarageDoorApi.git
    fi

}

function stopService {
    sudo systemctl stop ${GARAGE_SERVICE_FILE}
}

function copyServiceFile {
    sudo chmod 644 ${GARAGE_SERVICE_FILE}
    sudo yes | cp ${GARAGE_SERVICE_FILE} /etc/systemd/system/${GARAGE_SERVICE_FILE}
}

function configureSystemD {
    sudo systemctl daemon-reload
    sudo systemctl enable ${GARAGE_SERVICE_FILE}
}

function restartDevice {
    sudo reboot
}


cloneServiceFiles
stopService
copyServiceFile
configureSystemD
restartDevice