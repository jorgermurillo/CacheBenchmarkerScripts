#!/bin/bash

BENCHMARK=$1
HOST=$2
PORT=$3
INSTANCE=$4
DIRECTORY=$5
RECORDCOUNT=$6
#echo $BENCHMARK

cd ~/$DIRECTORY 
pwd
#nohup  ./bin/$BENCHMARK run redis -P ~/workloads/workloada -p redis.host=$HOST -p redis.port=$PORT  </dev/null > /tmp/redis_test/benchfile$INSTANCE 2>&1  &  
echo WHAT
echo $INSTANCE
#echo 'nohup  ./bin/$BENCHMARK run redis -P workloads/workload-replayScheduler_Yahoo -p redis.host=$HOST -p redis.port=$PORT  </dev/null > ~/tmp/redis_test/benchfile$INSTANCE 2>&1  &'
nohup  ./bin/$BENCHMARK run redis -P workloads/workload-replayScheduler_Resizing -p "redis.host=$HOST" -p "redis.port=$PORT"  -p operationcount=$RECORDCOUNT  </dev/null > ~/tmp/redis_test/benchfile$INSTANCE 2>&1  &  


