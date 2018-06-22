#!/bin/python3.6
import configparser
import subprocess
import sys
import redis
from time import sleep, time

print(sys.argv)

configfile = sys.argv[1]

'''
benchmarker = sys.argv[1]
host = sys.argv[2]
port = sys.argv[3]
numberOfInstances = int(sys.argv[4])
recordcount =  sys.argv[5]
elements_epoch = sys.argv[6]
port_int = int(port)
#memory = int(sys.argv[5])
memory = 524288000# 500 mb
'''



config = configparser.ConfigParser()
config.read(configfile)

host = config["TARGET"]["host"]
port = config["TARGET"]["port"]
port_int = int(port)
print(host)
print(port)

benchmarker = sys.argv[2]
print("Starting up the Redis instances.")

#The number of seconds to wait before checking if the benchmarker has stopped
kill_check_time = int(sys.argv[2])

# Checking if there is an equal number of redis instances to benchmarkers

numberOfRedis = len(config["INSTANCES"])
numberOfBenchmarkers = len(config["BENCHMARKERS"])


if numberOfRedis != numberOfBenchmarkers:
	print("The number of Redis instances (%d) does not match the number of benchmarker instances (%d)!"%(numberOfRedis, numberOfBenchmarkers))
	exit() 

i = 1
for key in config["INSTANCES"]:
	#print(subprocess.run(['nohup','./Redis-Shards/src/redis-server', '--port', str(port_int), ' </dev/null > /tmp/mylogfile 2>&1  &  ' ]))
	memory = config["INSTANCES"][key]
	#print(memory)


	subproc = subprocess.run(['./Redis_init.sh', str(port_int), memory, str(host), str(i) ]   , stdout=subprocess.PIPE)
	s = subproc.stdout.decode('utf-8')
	#print(s)
		
	print("Instance with port number %s running. Maxmemory = %s"%(str(port_int), memory ))
	
	port_int = port_int+1
	i+=1

port_int = int(port)





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
		#print(str(subprocess.check_output(['./Redis_run.sh', benchmarker, host, str(port_int), str(i), directory, recordcount])))
		s = subprocess.check_output(['./Benchmarker_run.sh', benchmarker, host, str(port_int), str(i), directory, str(recordcount)]).decode('utf-8')
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

		subprocess.run(["./Redis_kill.sh", host])
		break
	
	sleep(kill_check_time) # 300 seconds == 5 minutes

end = time()
total_time = end - start
print("Total time: " + str(total_time))

print("Done!")



