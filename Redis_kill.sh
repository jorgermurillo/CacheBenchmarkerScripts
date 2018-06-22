#!/bin/bash

HOST=$1
echo "Killing the Redis Process"
#kill $(ps -aux | grep redis-server | cut -d " " -f 6) #</dev/null > /tmp/mylogfile 2>&1  &  
ssh -i ~/Downloads/SHARDS.pem centos@$HOST  'kill $(pgrep -f redis-server) '