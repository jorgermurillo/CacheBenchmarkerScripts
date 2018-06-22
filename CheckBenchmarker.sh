#!/bin/bash

benchmarker=$1

pgrep -f $benchmarker | wc -l  
