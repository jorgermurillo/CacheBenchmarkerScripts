#!/bin/bash

IP=$1
EPOCH=$2
R_VALUE=$3
SETSIZE=$4
TOTALMEMORY=$5


ssh -i ~/Downloads/SHARDS.pem  centos@$IP 'cd redis-SHARDS ; nohup ./src/k_v_benchmark/ZeroMQ_SHARDS ' $EPOCH ' ' $R_VALUE ' '$SETSIZE' '$TOTALMEMORY' >~/tmp/ZeroMQ_SHARDSlogfile 2>&1   &  '
ssh -i ~/Downloads/SHARDS.pem  centos@$IP 'cd redis-SHARDS ;  nohup ./src/k_v_benchmark/redis-proxy   >~/tmp/redis-proxylogfile  2>&1  &  '
#nohup ./src/k_v_benchmark/redis-proxy > /tmp/redis-proxy-log 2>&1 &
#nohup ./src/k_v_benchmark/ZeroMQ_SHARDS2  1000   > /tmp/redis-proxy-log 2>&1 &


