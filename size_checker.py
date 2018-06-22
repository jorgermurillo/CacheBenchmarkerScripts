#!/bin/python3.6

import subprocess
import sys
import signal
import redis
from time import sleep



class redis_connection:
	
	port = 0
	file = None
	Redis = None

	def __init__(self, port, filename, Redis):

		self.port = port
		self.file = open(filename,'w')
		self.Redis = Redis

'''
List of arguments:
	host = IP where Redis instances are located
	first_port = the number of the first of the port That the Redis instances are listening to
	number_of_instances = how many instances of Redis are running in the experiment
	time_step =  how many seconds should the program sleep between the 'DBSIZE' queries	

'''

host = sys.argv[1]
first_port = int(sys.argv[2])
number_of_instances = int(sys.argv[3])
time_step = int(sys.argv[4])

redis_instances = {}

for port in range(first_port, first_port + number_of_instances):
	#redis_instances[port] =  redis.Redis(host=host, port=port) 
	fileName = "RedisDBSIZE_port%d.dat"%(port)

	redis_instances[port] = redis_connection(port, fileName, redis.Redis(host=host, port=port) )
	#redis_instances[port] = redis_connection(port,fileName , None)


keys = list(redis_instances.keys())
keys.sort()

'''
for e in keys:
	print(redis_instances[e].port)
	print(redis_instances[e].file)
'''
print(keys)

def handler(signum, frame):
	print("Catching SIGINT!")
	for e in keys:
		print(redis_instances[e].port)
		redis_instances[e].file.close()
	print("BYE BYE!!!")
	sys.exit()

signal.signal(signal.SIGINT, handler)

while(1):
	sleep(time_step)
	try:

		for e in keys:
			#print(redis_instances[e].port)
			DBSIZE = redis_instances[e].Redis.dbsize()
			redis_instances[e].file.write( "%d \n"%(DBSIZE) )
	except:
		print("Oopsie doopsie! :(")
		sys.exit()

