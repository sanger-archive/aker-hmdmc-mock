#!/bin/bash

set -e

cd "`dirname $0`"

if [ ! -f ./run.pid ]
then
	echo "Problem: No pid file found."
	exit 1
fi

kill `cat ./run.pid`
rm ./run.pid
echo "OK"
