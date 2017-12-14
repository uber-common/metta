from celery import Celery
from config import BaseConfig
import subprocess
import shlex
import json
import time
import datetime
import os
import sys
import datetime

config = BaseConfig()
sim_vagrant = Celery('tasks', backend=config.redisbackend, broker=config.redisbroker)


@sim_vagrant.task
def alive_vagrant():
    return "pong"

@sim_vagrant.task
def runcmd_win(vagrant_cmd, rule_name, rule_uuid, hostname):
	try:
		print "##### DEBUG -- We made it to the vagrant function  -- DEBUG ###### "
		print "'Running: {} with Rule GUID: {} against vagrant {}".format(vagrant_cmd, rule_uuid, hostname)
		cmd = 'vagrant winrm {} -c "{}"'.format(hostname, vagrant_cmd)
		args = shlex.split(cmd)
		print args
		dovagrant = subprocess.Popen(args)
		print dovagrant
		print "Inserting info into the DB"
		execution_time = datetime.datetime.utcnow()
		db.insert_row(rule_name, rule_uuid, hostname, execution_time)
	except Exception as e:
		print(e)

@sim_vagrant.task
def runcmd_osx(vagrant_cmd, rule_name, rule_uuid, hostname):
	try:
		print "##### DEBUG -- We made it to the vagrant function  -- DEBUG ###### "
		print "'Running: {} with Rule GUID: {} against vagrant {}".format(vagrant_cmd, rule_uuid, hostname)
		cmd = 'vagrant ssh {} -c "{}"'.format(hostname, vagrant_cmd)
		args = shlex.split(cmd)
		print args
		dovagrant = subprocess.Popen(args)
		print dovagrant
		print "Inserting info into the DB"
		execution_time = datetime.datetime.utcnow()
		db.insert_row(rule_name, rule_uuid, hostname, execution_time)
	except Exception as e:
		print(e)

@sim_vagrant.task
def runcmd_linux(vagrant_cmd, rule_name, rule_uuid, hostname):
	try:
		print "##### DEBUG -- We made it to the vagrant function  -- DEBUG ###### "
		print "'Running: {} with Rule GUID: {} against vagrant {}".format(vagrant_cmd, rule_uuid, hostname)
		cmd = 'vagrant ssh {} -c "{}"'.format(hostname, vagrant_cmd)
		args = shlex.split(cmd)
		print args
		dovagrant = subprocess.Popen(args)
		print dovagrant
		print "Inserting info into the DB"
		execution_time = datetime.datetime.utcnow()
		db.insert_row(rule_name, rule_uuid, hostname, execution_time)
	except Exception as e:
		print(e)

@sim_vagrant.task
def runcmd_nodb_win(vagrant_cmd, rule_name, rule_uuid, hostname):
	try:
		#print "changing locations"
		#os.chdir(vagrantlocation)
		print "##### DEBUG -- We made it to the vagrant function  -- DEBUG ###### "
		print "'Running: {} with Rule GUID: {} against vagrant {}".format(vagrant_cmd, rule_uuid, hostname)
		#cmd = "vagrant winrm "+hostname+" -c " +"\"" + vagrant_cmd +"\""
		cmd = 'vagrant winrm {} -c "{}"'.format(hostname, vagrant_cmd)
		args = shlex.split(cmd)
		print args
		dovagrant = subprocess.Popen(args)
		print dovagrant
	except Exception as e:
		print(e)

@sim_vagrant.task
def runcmd_nodb_osx(vagrant_cmd, rule_name, rule_uuid, hostname):
	try:
		print "##### DEBUG -- We made it to the vagrant function  -- DEBUG ###### "
		print "'Running: {} with Rule GUID: {} against vagrant {}".format(vagrant_cmd, rule_uuid, hostname)
		cmd = 'vagrant ssh {} -c "{}"'.format(hostname, vagrant_cmd)
		args = shlex.split(cmd)
		print args
		dovagrant = subprocess.Popen(args)
		print dovagrant
	except Exception as e:
		print(e)

@sim_vagrant.task
def runcmd_nodb_linux(vagrant_cmd, rule_name, rule_uuid, hostname):
	try:
		print "##### DEBUG -- We made it to the vagrant function  -- DEBUG ###### "
		print "'Running: {} with Rule GUID: {} against vagrant {}".format(vagrant_cmd, rule_uuid, hostname)
		cmd = 'vagrant ssh {} -c "{}"'.format(hostname, vagrant_cmd)
		args = shlex.split(cmd)
		print args
		dovagrant = subprocess.Popen(args)
		print dovagrant
	except Exception as e:
		print(e)
