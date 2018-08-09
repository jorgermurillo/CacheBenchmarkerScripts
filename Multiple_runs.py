#!/bin/python3.6
import sys
import configparser
import os
import subprocess
from random import randint
from datetime import datetime, timedelta

def create_dir(top_dir, sub_dir, runs):
	if not os.path.isdir(top_dir):
		#Create the top level directory
		subprocess.run(["mkdir", top_dir])
		
		#Subdirectory list
		list_sub = []
		#Obtain the name of the subdirectories by spliting the name of each subdirectory and retrieving the last eleemnt of the split list
		for e in sub_dir:
			tmp = e.split("/")
			name = tmp[len(tmp)-1]
			print(name)
			#Concatenate the path of the top level directory with "/" and the name of each subdirectory
			subdirectory = top_dir + "/" + name	
			print(subdirectory)
			
			#Create the subdirectory
			subprocess.run(["mkdir",subdirectory])

			#Create subdirectories for each run
			for i in range(runs):
				#Create the name of each subdirectory
				run_subdir = subdirectory + "/run_" + "%05d"%(i+1)
				print(run_subdir)
				subprocess.run(["mkdir", run_subdir])

			# Add the created subdirectory to the list
			list_sub.append(subdirectory)
		return list_sub
	else:
		print("The given top level directory already exists!!")
		sys.exit()


'''
	argv[1] = Configuration file to run

'''

#	MAIN SCRIPT STARTS HERE

configfile = sys.argv[1]

config = configparser.ConfigParser()
config.read(configfile)

directory_path = config["GENERAL"]["path"]
experiment_runs = int( config["GENERAL"]["runs"])
check_interval = config["GENERAL"]["check_time_interval"]
start_wait = int(config["GENERAL"]["start_wait"])


config_files_paths = []

for e in config["EXPERIMENTS"].values():
	config_files_paths.append(e)

print(config_files_paths)


subdirectories = create_dir(directory_path, config_files_paths, experiment_runs)

print(subdirectories)

#Create the counters for each run

counters = {}
i=0
for e in config_files_paths:
	tmp = {}
	tmp["results_subdirectory"] = subdirectories[i]
	i+=1
	tmp["counter"] = 0 
	counters[e] = tmp
print("Counters:")
print(counters)

total_runs = len(config_files_paths) * experiment_runs
current_runs = 0
print("Starting tests...\n\n")
while(current_runs < total_runs):
	# Pick a possible experiment to run
	experiment_index = randint(0, len(config_files_paths)-1)
	# Check if any more of that experiment should run
	exp = config_files_paths[experiment_index]
	if(counters[exp]["counter"]<experiment_runs):
		# Run experiment
		#print(exp)
		#print(check_interval)
		#print(datetime.now())
		#print(start_time)
		print("Runnning experiment number %d: %s"%(current_runs+1, exp))
		subproc = subprocess.run(['./test_script.py', exp,  check_interval, str(start_wait) ]   , stdout=subprocess.PIPE)
		s = subproc.stdout.decode('utf-8')
		# Increase current runs counter by one after succesfully running the experiment	
		current_runs+=1
		# Increasse the counter in 
		tmp_count = counters[exp]["counter"]
		tmp_count+=1
		counters[exp]["counter"] = tmp_count

		#print(s)

		#Save the output to a file called test_script.out
		subdirectory = counters[exp]["results_subdirectory"] + "/run_%05d/"%(tmp_count)
		filename = "%s%s"%(subdirectory,"test_script.out")
		outputfile = open(filename,"w")
		outputfile.write(s)
		outputfile.close()

		#Reading the config file of the actual experiment to see how many redis instances were run
		config2 = configparser.ConfigParser()
		config2.read(exp)
		instances = len( config2["INSTANCES"] )
		IP = config2["TARGET"]["host"]
		ZEROMQ = config2["ZEROMQ"]["active"]

		if ZEROMQ=="yes":
			# Run script that downloads and copies the appropiate info to the respective subdirectory
			subproc = subprocess.run(['./Move_files.sh', str(instances),  IP, subdirectory ,"ZEROMQ"]   , stdout=subprocess.PIPE)
			s = subproc.stdout.decode('utf-8')
		else:
			# Run script that downloads and copies the appropiate info to the respective subdirectory
			subproc = subprocess.run(['./Move_files.sh', str(instances),  IP, subdirectory ,"NORMAL"]   , stdout=subprocess.PIPE)
			s = subproc.stdout.decode('utf-8')
		print("Done with experiment number %d"%(current_runs))
		print("\n\n")

print("DONE!!")