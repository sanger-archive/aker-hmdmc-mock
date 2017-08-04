#!/bin/bash

PORT=3501

set -e

cd "`dirname $BASH_SOURCE`"

if [ -f ./run.pid ]
then
	echo "Problem: run.pid file already exists. If the script is not already running, delete the pid file."
	exit 1
fi

if [ ! -f ./nginx-selfsigned.pem ]
then
  openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout nginx-selfsigned.key -out nginx-selfsigned.pem
fi

nohup ./fake_hmdmc.py -c nginx-selfsigned.pem -k nginx-selfsigned.key $PORT > ./log.txt 2>&1 &

echo $! > ./run.pid
echo "OK"
