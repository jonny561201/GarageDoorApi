#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
WHITE='\033[0m'

function runUnitTests {
    echo -e "${YELLOW}---------------Running Unit Tests---------------${WHITE}"
    pytest -s $(pwd)/test/unit
}

function startPostgresDocker {
    echo -e "${YELLOW}---------------Running Integration Tests---------------${WHITE}"
    docker-compose up -d
}

function waitForContainerToBeHealthy {
    until [[ $(docker inspect postgres-test -f='{{.State.Health.Status}}') = "healthy" ]]; do
        echo "...waiting for healthy..."
        sleep 1
    done
    echo -e "${GREEN}Container is healthy!${WHITE}"
}

function runIntegrationTests {
    echo -e "${YELLOW}---------------Running Integration Tests---------------${WHITE}"
    pytest -s $(pwd)/test/integration
}

function teardownDocker {
    echo -e "${YELLOW}---------------Cleaning up Container---------------${WHITE}"
    docker-compose down
}

runUnitTests
startPostgresDocker
waitForContainerToBeHealthy
runIntegrationTests
teardownDocker