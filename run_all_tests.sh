#!/bin/bash

function runUnitTests {
    echo "---------------Running Unit Tests---------------"
    pytest -s $(pwd)/test/unit
}

function runIntegrationTests {
    echo "---------------Running Integration Tests---------------"
    docker-compose up -d
    pytest -s $(pwd)/test/integration
}

function teardownDocker {
    echo "---------------Cleaning up Container---------------"
    docker-compose down
}

runUnitTests
runIntegrationTests