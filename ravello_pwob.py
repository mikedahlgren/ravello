#!/usr/bin/python
#Forked from Ryan Hennessy
#Modified by Mike Dahlgren
from ravello_sdk import *
import argparse
import getpass

def connectToRavello(args, passwd):
        client = RavelloClient()
        client.connect()
        try:
                client.login(args.user, passwd)
        except:
                print "Invalid Password"
                quit()
	return client


def findHostnames(args, passwd):
	print "Query"
	print "Blueprint : " , args.blueprint

	client = connectToRavello(args, passwd) 

	apps = client.get_applications({'baseBlueprintId' : args.blueprint})

	fp = open("itwob_labs.csv", "w")

	c=1
	for single_app in apps:
           print 'Found : ', single_app['name']
	   file_line = single_app['name'] + "," 
	   single_app = client.get_application(single_app['id'])
	   for vm in single_app['deployment']['vms']:
	      try: 
		 name = vm['externalFqdn']
		 file_line = file_line + name + ","
	      except:
		pass 
	   fp.write(file_line + "\n")
	   c+=1

	fp.close()


def createRavelloApps(args, passwd):
	client = connectToRavello(args, passwd)

	print "Create"
	print "Blueprint : " , args.blueprint
	print "Location  : " , args.location
	print "Auto Stop : " , args.time
	print "Count     : " , args.count
	print "Start     : " , args.start
	print ""

	for c in range(args.start, args.start + args.count):
		app_name = "CloudForms-Workshop-" + args.location + "-" + str(c).zfill(3) 	
		print "Creating  : ", app_name
		new_app=client.create_application({'name': app_name, 'description': 'CloudForm Workshop for ' + args.location , 'baseBlueprintId': args.blueprint})
		client.set_application_expiration(new_app['id'], {'expirationFromNowSeconds' : args.time })
		client.publish_application(new_app['id'], {'optimizationLevel': 'PERFORMANCE_OPTIMIZED'})
		print "Published : ", new_app['name']
		print ""


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-c", "--create", action="store_true", help="Create Ravello applications")
	parser.add_argument("-q", "--query", action="store_true", help="Query VM Names for existing applications")	
	parser.add_argument("-n", "--count", type=int, help="Number of application instances to create")
	parser.add_argument("-s", "--start", type=int, help="Start iterating app numbers from this number")
	parser.add_argument("-l", "--location", type=str, help="Short unique name (location) for application naming")
	parser.add_argument("-b", "--blueprint", type=int, help="Blueprint ID for create or query")
	parser.add_argument("-u", "--user", type=str, help="Your Ravello username")
	parser.add_argument("-t", "--time", type=int, help="How many hours before application auto-stop")
	args = parser.parse_args()

	if args.user == None:
		print "ERROR: --user not specified"
		quit()

	if args.blueprint == None:
		print "ERROR: --blueprint not specified"
		quit()	

	passwd = getpass.getpass("Ravello Password: ")

	if args.query == True:
		findHostnames(args, passwd)
		quit()

	if args.create == True:
		if args.count == None:
			print "ERROR: --count not specified"
			quit()

		if args.location == None:
			print "ERROR: --location not specified"
			quit()

		if args.start == None:
			print "WARN: --start not specified, assuming --start 1"
			args.start = 1;

		if args.time == None:
			print "WARN: --time not specified, assuming --time 4"
			args.time = 60 * 60 * 4
		else:
			args.time = 60 * 60 * args.time

		createRavelloApps(args, passwd)
		quit()
