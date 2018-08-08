#!/bin/bash


NUMBER=$1
IP=$2
DOWNLOAD_PATH=$3


echo ssh -i ~/Downloads/SHARDS.pem  centos@$IP 'tar -vczf ZeroMQ_Results.tar.gz  ~/redis-SHARDS/ZeroMQ_Results ~/tmp/ZeroMQ_SHARDSlogfile'

echo scp -i ~/Downloads/SHARDS.pem  centos@$IP:/home/centos/ZeroMQ_Results.tar.gz $DOWNLOAD_PATH



for (( I=1; I<=$NUMBER; I++ ))
do  
	tail -n 3500 ~/tmp/redis_test/benchfile$I  >  $DOWNLOAD_PATH/benchresults$I
	cp ~/tmp/redis_test/benchfile$I  $DOWNLOAD_PATH
done