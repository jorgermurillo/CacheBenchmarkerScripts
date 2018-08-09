#!/bin/python3.6
import configparser
import subprocess
import sys
import redis
from datetime import datetime, timedelta
from time import sleep, time
import signal

def SIGINThandler(signum, frame):
	print("Catching SIGINT!")
	
	print("Killing")
	subprocess.run(["./kill_local.sh", "kv-replay"])
	subprocess.run(["./kill_remote.sh", "redis", host])
	if Resizer_bool:
		subprocess.run(["./kill_remote.sh", "redis-proxy", host])
		
		subprocess.run(["./kill_remote.sh", "ZeroMQ_SHARDS", host])
		
		

	print("BYE BYE!!!")
	sys.exit()

def SIGTSTPhandler(signum, frame):
	print("Catching SIGTSTP!")
				
	print("BYE BYE!!!")
	sys.exit()


signal.signal(signal.SIGINT, SIGINThandler)
signal.signal(signal.SIGTSTP, SIGTSTPhandler)

print(sys.argv)

configfile = sys.argv[1]

Resizer_bool = False
config = configparser.ConfigParser()
config.read(configfile)

host = config["TARGET"]["host"]
port = config["TARGET"]["port"]
port_int = int(port)
Resizer_bool = config["ZEROMQ"].getboolean("active")
print(Resizer_bool)
print(host)
print(port)
benchmarker = "kv-replay"
print("Starting up the Redis instances.")

#WORKLOAD
workload_file = config["WORKLOAD"]["workload_file"]

#The number of seconds to wait before checking if the benchmarker has stopped
kill_check_time = int(sys.argv[2])

#Time in minutes to wait before starting. Format: "2016-01-01 00:00:00:000"
wait_time = int(sys.argv[3])

# Checking if there is an equal number of redis instances to benchmarkers
numberOfRedis = len(config["INSTANCES"])
numberOfBenchmarkers = len(config["BENCHMARKERS"])


if numberOfRedis != numberOfBenchmarkers:
	print("The number of Redis instances (%d) does not match the number of benchmarker instances (%d)!"%(numberOfRedis, numberOfBenchmarkers))
	exit() 

total_memory = 0

i = 1
for key in config["INSTANCES"]:
	#print(subprocess.run(['nohup','./Redis-Shards/src/redis-server', '--port', str(port_int), ' </dev/null > /tmp/mylogfile 2>&1  &  ' ]))
	memory = config["INSTANCES"][key]
	#memory_tmp is used to extract the number of bytes (memory is given as XXmb)
	memory_tmp = memory.split("m")[0]
	total_memory += int(memory_tmp)

	subproc = subprocess.run(['./Redis_init.sh', str(port_int), memory, str(host), str(i) ]   , stdout=subprocess.PIPE)
	s = subproc.stdout.decode('utf-8')
	#print(s)
		
	print("Instance with port number %s running. Maxmemory = %s"%(str(port_int), memory ))
	
	port_int = port_int+1
	i+=1

port_int = int(port)


if config["ZEROMQ"]["active"]=='yes':
	# convert memory to bytes
	total_memory = total_memory * 1024 * 1024 
	setsize = int(config["ZEROMQ"]["setsize"])
	epoch_length = int(config["ZEROMQ"]["epoch_length"])
	r_value = float(config["ZEROMQ"]["r_value"])
	s = subprocess.check_output(['./Proxy.sh', host,  str(epoch_length), str(r_value),str(setsize),str(total_memory)]).decode('utf-8') 
	print(s)


sleep(1)
print("Starting the benchmarker instances: %s"%(benchmarker))
if benchmarker=='ycsb':

	for i in range(1,numberOfInstances+1):
		directory = '/YCSB%d'%(i)
		print(directory)
		s = subprocess.check_output(['./Benchmarker_run.sh', benchmarker, host, str(port_int), str(i), directory, recordcount]).decode('utf-8') 
		print(s)
		print(port_int)
		port_int+=1
		
elif benchmarker=='kv-replay':
	i = 1
	for key in config["BENCHMARKERS"]:
		recordcount = config["BENCHMARKERS"][key]
		directory = '/KV-replay%d'%(i)
		print("Instance of %s with port %d running. Record count = %s"%(directory, port_int, recordcount))
		wait_time_delta = timedelta(minutes=wait_time)
		start_time = "'"+str(datetime.now() + wait_time_delta)+"'"
		s = subprocess.check_output(['./Benchmarker_run.sh', benchmarker, host, str(port_int), str(i), directory, str(recordcount), start_time, workload_file]).decode('utf-8')
		print(s)
		
		port_int+=1
		i+=1
start = time()	


sleep(60)



while(1):
	
	x = int(subprocess.check_output(["./CheckBenchmarker.sh", benchmarker]))
	print("Number of Processes: " + str(x))
	
	if(x<=2): 
		sleep(5)
		print("Killing")

		subprocess.run(["./kill_remote.sh", "redis", host])
		if Resizer_bool:
			subprocess.run(["./kill_remote.sh", "redis-proxy", host])
			subprocess.run(["./kill_remote.sh", "ZeroMQ_SHARDS", host])

		break
	
	sleep(kill_check_time) # 300 seconds == 5 minutes

end = time()
total_time = end - start
print("Total time: " + str(total_time))

print("Done!")



