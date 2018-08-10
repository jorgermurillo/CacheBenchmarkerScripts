#!/bin/bash


NUMBER=$1
IP=$2
DOWNLOAD_PATH=$3
TYPE=$4

if [ $TYPE = "ZEROMQ" ]
then
	echo "ZEROMQ"
	ssh -i ~/Downloads/SHARDS.pem  centos@$IP 'tar -vczf ZeroMQ_Results.tar.gz  ~/redis-SHARDS/ZeroMQ_Results ~/tmp/ZeroMQ_SHARDSlogfile'
	scp -i ~/Downloads/SHARDS.pem  centos@$IP:/home/centos/ZeroMQ_Results.tar.gz $DOWNLOAD_PATH
fi




for (( I=1; I<=$NUMBER; I++ ))
do  
	tail -n 3500 ~/tmp/redis_test/benchfile$I  >  $DOWNLOAD_PATH/benchresults$I
	cp ~/tmp/redis_test/benchresults$I  $DOWNLOAD_PATH
done