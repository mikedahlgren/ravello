ravello
=======

Python script that creates applications in Ravello.


Usage
=======

The script has to functions.   The first will create the lab environment and the second function will query the labs for the DNS names of the virtual machines.  Each of the functions will prompt for a user password after the command is run.

To create a lab environment you will need to run the script with the following command line options:
   ravello_pwob.py -u (ravello user name) -c -n (number of applcations to create) -l (Name of location the lab will be run) 

To query a ravello environment you will need to run the script with the following command line options.   This will output the DNS names in a csv file.
   ravello_pwob.py -u (ravello user name) -q -b (name of blueprint used to create lab)

