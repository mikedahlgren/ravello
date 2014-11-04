#!/usr/bin/python
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
	client = connectToRavello(args, passwd) 

	apps = client.get_applications({"blueprintName" : args.blueprint})

	fp = open("pwob_labs.csv", "w")

	c=1
	for single_app in apps:
#	   file_line = "Student " + str(c) + "," 
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

	for c in range(1, args.count+1):
		app_name = "pwob-" + args.location + "-" + str(c).zfill(3) 	
		new_app=client.create_application({'name': app_name, 'description': 'Platform Without BoundariesLabs for ' + args.location, 'baseBlueprintId': 52101381})
		client.set_application_expiration(new_app['id'], {'expirationFromNowSeconds' : '36000' })
		client.publish_application(new_app['id'], {'optimizationLevel': 'PERFORMANCE_OPTIMIZED'})



if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-b", "--blueprint", type=str, help="Ravello Blue Print to use")
	parser.add_argument("-u", "--user", type=str, help="Ravello User")
#	parser.add_argument("-a", "--app-name", type=str, help="Template of application name")
	parser.add_argument("-c", "--create", action="store_true", help="Create Ravello applications")
	parser.add_argument("-q", "--query", action="store_true", help="Query VM Names for existing applications")	
	parser.add_argument("-n", "--count", type=int, help="Number of Application Instances to create")
	parser.add_argument("-l", "--location", type=str, help="Name of the Location for Ravello Service Naming")
	args = parser.parse_args()

	if args.user == None:
		print "Error: Please specify a Ravello user to use"
		quit()
	
	passwd = getpass.getpass("Ravello Password: ")

	if args.query == True:
		if args.blueprint == None:
			print "Error: Please specifiy a Ravello Blueprint to use"
			quit()	
		findHostnames(args, passwd)

	if args.create == True:
		if args.count == None:
			print "Error: Need the count of applications to create"
			quit()
		if args.location == None:
			print "Error: Need to know location in order name the Ravello Services"
			quit()
		createRavelloApps(args, passwd)

