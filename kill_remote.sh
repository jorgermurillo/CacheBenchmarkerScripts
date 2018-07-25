#!/bin/bash

#This script is for killing a process using its name in another machine


TARGET=$1
HOST=$2

echo "Killing \"$TARGET"\"" remotely"
ssh -i ~/Downloads/SHARDS.pem centos@$HOST  'kill $(pgrep -f '$TARGET') '


