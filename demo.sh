#!/bin/bash

set -e

# copy it somewhere else

REVS=(step01 step02 step03 step04 step05 step06 step07)
if [[ $1 == "start" ]]; then
    git clean -xfd || sudo git clean -xfd
    docker-compose down
    docker-compose up -d
    rev=${REVS[0]}
    git checkout $rev
    echo 0 > /tmp/demo
elif [[ $1 == "next" ]]; then
    idx=$(($(cat /tmp/demo)+1))
    echo $idx > /tmp/demo
    rev=${REVS[$idx]}
    git checkout $rev
    docker-compose restart
else
    exit 1
fi
