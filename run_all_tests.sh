#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
WHITE='\033[0m'

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

function runUnitTests {
    echo -e "${YELLOW}---------------Running Unit Tests---------------${WHITE}"
    python3 -m pytest -s ${CURRENT_DIR}/test/unit
    UNIT_TEST=$?
    if [[ ${UNIT_TEST} -ne 0 ]]; then
        echo -e "${RED}ERROR: Unit Tests Failed!!!${WHITE}"
        exit 1
    fi
    echo -e "${GREEN}---------------Unit Tests Passed---------------${WHITE}"
}

function startPostgresDocker {
    echo -e "${YELLOW}---------------Starting Postgres Docker---------------${WHITE}"
    pushd ${CURRENT_DIR}
    docker-compose up -d
    popd
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
    python3 -m pytest -s ${CURRENT_DIR}/test/integration
    INTEGRATION_EXIT=$?
    if [[ ${INTEGRATION_EXIT} -ne 0 ]]; then
        echo -e "${RED}ERROR: Integration Tests Failed!!!${WHITE}"
        exit 1
    fi
    echo -e "${GREEN}---------------Integration Tests Passed---------------${WHITE}"
}

function teardownDocker {
    echo -e "${YELLOW}---------------Cleaning up Container---------------${WHITE}"
    pushd ${CURRENT_DIR}
    docker-compose down
    popd
}

runUnitTests
startPostgresDocker
waitForContainerToBeHealthy
runIntegrationTests
teardownDocker