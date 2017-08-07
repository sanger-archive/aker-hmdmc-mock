#!/bin/bash

PORT=3501

set -e

cd "`dirname $BASH_SOURCE`"

if [ -f ./run.pid ]
then
	echo "Problem: run.pid file already exists. If the script is not already running, delete the pid file."
	exit 1
fi

nohup ./fake_hmdmc.py -c ../shared/nginx-selfsigned.pem -k ../shared/nginx-selfsigned.key $PORT > ./log.txt 2>&1 &

echo $! > ./run.pid
echo "OK"
