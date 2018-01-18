#!/bin/bash
PROJECT_FOLDER=$1
PORT=3501

set -e

cd "`dirname $BASH_SOURCE`"

if [ -f ./run.pid ]
then
	echo "Problem: run.pid file already exists. If the script is not already running, delete the pid file."
	exit 1
fi

nohup $PROJECT_FOLDER/current/fake_hmdmc.py -c $PROJECT_FOLDER/shared/aker-fake-hmdmc_public.crt -k $PROJECT_FOLDER/shared/aker-fake-hmdmc_private.pem $PORT > $PROJECT_FOLDER/current/log.txt 2>&1 &

echo $! > ./run.pid
echo "OK"
