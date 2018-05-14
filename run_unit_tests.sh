#!/usr/bin/env bash

export PYTHONPATH=$PYTHONPATH:$(pwd)/svc:$(pwd)/test/unit
echo $PYTHONPATH

pytest -s $(pwd)/test/unit
