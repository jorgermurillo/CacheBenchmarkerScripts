#!/bin/bash

PORT=$1
MEMORY=$2
IP=$3
NUMBER=$4
#cd Redis-Shards

echo ssh -i ~/Downloads/SHARDS.pem  centos@$IP 'cd redis-SHARDS ; nohup ./src/redis-server ./redis_'$PORT'.conf --protected-mode no  --port '$PORT'  --maxmemory ' $MEMORY ' </dev/null > /tmp/redis'$NUMBER'logfile 2>&1  &  '


ssh -i ~/Downloads/SHARDS.pem  centos@$IP 'cd redis-SHARDS ; nohup ./src/redis-server ./redis_'$PORT'.conf  --protected-mode no  --port '$PORT'  --maxmemory ' $MEMORY ' </dev/null > /tmp/redis'$NUMBER'logfile 2>&1  &  '

#nohup ./src/k_v_benchmark/redis-proxy > /tmp/redis-proxy-log 2>&1 &
#nohup ./src/k_v_benchmark/ZeroMQ_SHARDS2  1000   > /tmp/redis-proxy-log 2>&1 &

