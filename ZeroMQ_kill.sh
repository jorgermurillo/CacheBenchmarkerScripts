#!/bin/bash

HOST=$1
echo "Killing the redis-proxy Process"
ssh -i ~/Downloads/SHARDS.pem centos@$HOST  'kill $(pgrep -f redis-proxy) '

echo "Killing the ZeroMQ_SHARDS Process"
ssh -i ~/Downloads/SHARDS.pem centos@$HOST  'kill $(pgrep -f ZeroMQ_SHARDS) '
