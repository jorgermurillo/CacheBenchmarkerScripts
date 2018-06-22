#!/bin/bash

TARGET=$1
echo "Killing \""$TARGET"\""
#kill $(ps -aux | grep redis-server | cut -d " " -f 6) #</dev/null > /tmp/mylogfile 2>&1  &  
kill $(pgrep -f $TARGET) 