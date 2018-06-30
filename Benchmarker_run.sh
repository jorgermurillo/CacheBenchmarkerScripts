#!/bin/bash

BENCHMARK=$1
HOST=$2
PORT=$3
INSTANCE=$4
DIRECTORY=$5
RECORDCOUNT=$6
START=$7
#echo $BENCHMARK

cd ~/$DIRECTORY 
pwd

echo $INSTANCE
nohup  ./bin/$BENCHMARK run redis -P workloads/workload-replayScheduler_Resizing -p "redis.host=$HOST" -p "redis.port=$PORT" -p startdatetime="$START" -p operationcount=$RECORDCOUNT  </dev/null > ~/tmp/redis_test/benchfile$INSTANCE 2>&1  &  


