from celery import Celery
import subprocess
import json
import time
import datetime
import os
import sys
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
#from database import db

sim_vagrant = Celery('tasks', backend='redis://localhost/0', broker='redis://localhost/1')

# change for current vagrant location
vagrantlocation = "/Users/xxxxx/vagrant_rules_automation/"

@sim_vagrant.task
def alive_vagrant():
    return "pong"

@sim_vagrant.task
def runcmd_win(vagrant_cmd, rule_name, rule_uuid, hostname):
	try:
		print "changing locations"
		os.chdir(vagrantlocation)
		print "##### DEBUG -- We made it to the vagrant function  -- DEBUG ###### "
		print "'Running: {} with Rule GUID: {} against vagrant {}".format(vagrant_cmd, rule_uuid, hostname)
		cmd = "vagrant winrm "+hostname+" -c " +"\"" + vagrant_cmd +"\""
		dovagrant = subprocess.call(cmd, shell=True)
		print dovagrant
		print "Inserting info into the DB"
		execution_time = datetime.datetime.utcnow()
		db.insert_row(rule_name, rule_uuid, hostname, execution_time)
	except Exception as e:
		print(e)

@sim_vagrant.task
def runcmd_osx(vagrant_cmd, rule_name, rule_uuid, hostname):
	try:
		print "changing locations"
		os.chdir(vagrantlocation)
		print "##### DEBUG -- We made it to the vagrant function  -- DEBUG ###### "
		print "'Running: {} with Rule GUID: {} against vagrant {}".format(vagrant_cmd, rule_uuid, hostname)
		cmd = "vagrant ssh "+hostname+" -c " +"\"" + vagrant_cmd +"\""
		dovagrant = subprocess.call(cmd, shell=True)
		print dovagrant
		print "Inserting info into the DB"
		execution_time = datetime.datetime.utcnow()
		db.insert_row(rule_name, rule_uuid, hostname, execution_time)
	except Exception as e:
		print(e)

@sim_vagrant.task
def runcmd_linux(vagrant_cmd, rule_name, rule_uuid, hostname):
	try:
		print "changing locations"
		os.chdir(vagrantlocation)
		print "##### DEBUG -- We made it to the vagrant function  -- DEBUG ###### "
		print "'Running: {} with Rule GUID: {} against vagrant {}".format(vagrant_cmd, rule_uuid, hostname)
		cmd = "vagrant ssh "+hostname+" -c " +"\"" + vagrant_cmd +"\""
		dovagrant = subprocess.call(cmd, shell=True)
		print dovagrant
		print "Inserting info into the DB"
		execution_time = datetime.datetime.utcnow()
		db.insert_row(rule_name, rule_uuid, hostname, execution_time)
	except Exception as e:
		print(e)

@sim_vagrant.task
def runcmd_nodb_win(vagrant_cmd, rule_name, rule_uuid, hostname):
	try:
		print "changing locations"
		os.chdir(vagrantlocation)
		print "##### DEBUG -- We made it to the vagrant function  -- DEBUG ###### "
		print "'Running: {} with Rule GUID: {} against vagrant {}".format(vagrant_cmd, rule_uuid, hostname)
		cmd = "vagrant winrm "+hostname+" -c " +"\"" + vagrant_cmd +"\""
		dovagrant = subprocess.call(cmd, shell=True)
		print dovagrant
	except Exception as e:
		print(e)

@sim_vagrant.task
def runcmd_nodb_osx(vagrant_cmd, rule_name, rule_uuid, hostname):
	try:
		print "changing locations"
		os.chdir(vagrantlocation)
		print "##### DEBUG -- We made it to the vagrant function  -- DEBUG ###### "
		print "'Running: {} with Rule GUID: {} against vagrant {}".format(vagrant_cmd, rule_uuid, hostname)
		cmd = "vagrant ssh "+hostname+" -c " +"\"" + vagrant_cmd +"\""
		dovagrant = subprocess.call(cmd, shell=True)
		print dovagrant
	except Exception as e:
		print(e)

@sim_vagrant.task
def runcmd_nodb_linux(vagrant_cmd, rule_name, rule_uuid, hostname):
	try:
		print "changing locations"
		os.chdir(vagrantlocation)
		print "##### DEBUG -- We made it to the vagrant function  -- DEBUG ###### "
		print "'Running: {} with Rule GUID: {} against vagrant {}".format(vagrant_cmd, rule_uuid, hostname)
		cmd = "vagrant ssh "+hostname+" -c " +"\"" + vagrant_cmd +"\""
		dovagrant = subprocess.call(cmd, shell=True)
		print dovagrant
	except Exception as e:
		print(e)
