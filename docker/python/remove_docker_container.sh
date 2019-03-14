#! /bin/sh
docker ps -aq |xargs docker stop
docker ps -aq | xargs docker rm
