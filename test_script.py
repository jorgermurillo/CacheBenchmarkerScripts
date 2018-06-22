#!/bin/python3.6

import subprocess
import sys
import redis
from time import sleep, time

print(sys.argv)

#print(subprocess.check_output(['mvn' ,'-v']))
benchmarker = sys.argv[1]
host = sys.argv[2]
port = sys.argv[3]
numberOfInstances = int(sys.argv[4])
recordcount =  sys.argv[5]
elements_epoch = sys.argv[6]
port_int = int(port)
#memory = int(sys.argv[5])
memory = 524288000# 500 mb


#print("Starting the Redis-proxy")

#subprocess.run(['./Redis-Shards/', str(port_int)], stdout=subprocess.PIPE)

# Start the Redis instances
print("Starting up the Redis instances.")

#print(str(subprocess.check_output(['./Proxy.sh',  host, elements_epoch])))

for i in range(1,numberOfInstances+1):
	#print(subprocess.run(['nohup','./Redis-Shards/src/redis-server', '--port', str(port_int), ' </dev/null > /tmp/mylogfile 2>&1  &  ' ]))

	subproc = subprocess.run(['./Redis_init.sh', str(port_int), str(memory), str(host), str(i) ]   , stdout=subprocess.PIPE)
	s = subproc.stdout.decode('utf-8')
	print(s)
		
	print("Instance with port number %s running "%(str(port_int)) )
	'''
	sleep(6)
	#r = redis.Redis(host=host, port=port_int)
	#r.config_set("maxmemory", memory)
	'''
	port_int = port_int+1


port_int = int(port)





sleep(10)
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
	
	for i in range(1,numberOfInstances+1):
		directory = '/KV-replay%d'%(i)
		print("Instance of %s number %d with port %d running"%(directory, i, port_int))
		#print(str(subprocess.check_output(['./Redis_run.sh', benchmarker, host, str(port_int), str(i), directory, recordcount])))
		s = subprocess.check_output(['./Benchmarker_run.sh', benchmarker, host, str(port_int), str(i), directory, str(recordcount)]).decode('utf-8')
		print(s)
		print(port_int)
		port_int+=1

start = time()
		
sleep(60)



while(1):
	
	x = int(subprocess.check_output(["./CheckBenchmarker.sh", benchmarker]))
	print("Number of Processes: " + str(x))
	#print(str(x))
	
	if(x<=2): # the +2 takes into account the fact that the pgrep call in CheckBenchmarker.sh will return the "./ CheckBenchmarker.shkv-replay" process as well as the "./test_script.py"
		sleep(30)
		print("Killing")

		#subprocess.run(["./Redis_kill.sh", host])
		break
	
	sleep(10) # 300 seconds == 5 minutes

end = time()
total_time = end - start
print("Total time: " + str(total_time))

print("Done!")



