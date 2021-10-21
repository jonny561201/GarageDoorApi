#!/usr/bin/env bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
WHITE='\033[0m'

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

function runUnitTests {
  echo -e "${YELLOW}----------Running Unit Tests----------${WHITE}"
  if [[ "$OSTYPE" == "msys" ]]; then
    runWindowsUnitTests
  else
    runLinuxUnitTests
  fi
  echo -e "${GREEN}----------Unit Tests Passed----------${WHITE}"
}

function runLinuxUnitTests {
  python3 -m pytest -s ${CURRENT_DIR}/test/unit
  UNIT_TEST=$?
  if [[ ${UNIT_TEST} -ne 0 ]]; then
      echo -e "${RED}ERROR: Unit Tests Failed!!!${WHITE}"
      exit 1
  fi
}

function runWindowsUnitTests {
  python -m pytest -s ${CURRENT_DIR}/test/unit
  UNIT_TEST=$?
  if [[ ${UNIT_TEST} -ne 0 ]]; then
      echo -e "${RED}ERROR: Unit Tests Failed!!!${WHITE}"
      exit 1
  fi
}

function runIntegrationTests {
  echo -e "${YELLOW}---------------Running Integration Tests---------------${WHITE}"
  if [[ "$OSTYPE" == "msys" ]]; then
    runWindowsIntegrationTests
  else
    runLinuxIntegrationTests
  fi
}

function runLinuxIntegrationTests {
    if [ -d "${CURRENT_DIR}/test/integration" ]; then
      python3 -m pytest -s ${CURRENT_DIR}/test/integration
      INTEGRATION_EXIT=$?
      if [[ ${INTEGRATION_EXIT} -ne 0 ]]; then
          echo -e "${RED}ERROR: Integration Tests Failed!!!${WHITE}"
          exit 1
      fi
      echo -e "${GREEN}---------------Integration Tests Passed---------------${WHITE}"
  fi
}

function runWindowsIntegrationTests {
  if [ -d "${CURRENT_DIR}/test/integration" ]; then
    python -m pytest -s ${CURRENT_DIR}/test/integration
    INTEGRATION_EXIT=$?
    if [[ ${INTEGRATION_EXIT} -ne 0 ]]; then
        echo -e "${RED}ERROR: Integration Tests Failed!!!${WHITE}"
        exit 1
    fi
    echo -e "${GREEN}---------------Integration Tests Passed---------------${WHITE}"
  fi
}

function activateVirtualEnv {
  echo -e "${YELLOW}---------------Activating Virtual Environment---------------${WHITE}"
  if [[ "$OSTYPE" == "msys" ]]; then
    source ${CURRENT_DIR}/venv/Scripts/activate
  else
    source ${CURRENT_DIR}/venv/bin/activate
  fi
}

function deactivateVirtualEnv {
  echo -e "${YELLOW}---------------Deactivating Virtual Environment---------------${WHITE}"
  deactivate
}


activateVirtualEnv
runUnitTests
runIntegrationTests
deactivateVirtualEnv