#author Chris Gates - Uber

# adversarial-simulation-automation
import datetime
import subprocess
import time
import yaml
import os
import logging
import pprint
import sys
import requests

from random import randint

#slack hook URL
hook = 'https://hooks.slack.com/services/XXXXXX'

windows = "windows-cb"
osx = "osx-cb"

#logging = True

from workers.vagranttasks import *
from reporting.log_to_file import *

#not using this..but u can
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
					)
logger = logging.getLogger(__name__)

def post_to_slack(hook,json):
	try:
		r = requests.post(hook, json=json)
	except Exception as e:
		print e

def run_scenario(ioc_filename):
	try:
		print("### Running the Scenario ###")
		#print ioc_filename
		raw_iocs = yaml.load_all(open(ioc_filename,'r').read())


		timenow = datetime.datetime.utcnow()

		for raw_ioc in raw_iocs:
			scenario = raw_ioc.get('meta').get('scenario_actions')
			rule_name = raw_ioc.get('name')
			print "### {} ###".format(rule_name)

			scenario_actions = []
			#read the steps from purple_actions in yaml and load them into purple_actions
			for x in range(1,len(scenario)+1):
				scenario_actions.append(raw_ioc.get('meta').get('scenario_actions').get(x))

			for uuid_file in scenario_actions:
				run_uuid(uuid_file)

	except Exception as e:
		print e

def run_uuid(ioc_filename):
	try:
		print"\nRunning UUID actions inside:{}".format(ioc_filename)

		raw_iocs = yaml.load_all(open(ioc_filename,'r').read())


		for raw_ioc in raw_iocs:
			rule_name = raw_ioc.get('name')
			rule_uuid = raw_ioc.get('uuid')
			rule_os = raw_ioc.get('os')
			mitre_phase = raw_ioc.get('meta').get('mitre_attack_phase')
			mitre_tech = raw_ioc.get('meta').get('mitre_attack_technique')
			purple = raw_ioc.get('meta').get('purple_actions')

			if not purple:
				print "No Purple Actions detected you've probably messed up your scenario.yml..."
				sys.exit(0)

			purple_actions = []
			#read the steps from purple_actions in yaml and load them into purple_actions
			for x in range(1,len(purple)+1):
				purple_actions.append(raw_ioc.get('meta').get('purple_actions').get(x))

			if rule_os == "windows":
				print "OS matched windows...sending to the windows vagrant"
				for action in purple_actions:
					print("Running: {}".format(action))
					timenow = datetime.datetime.utcnow()
					date = timenow.strftime('%Y-%m-%d')
					hourminsec = timenow.strftime('%H:%M:%S')
					time_to_log = date+" "+hourminsec
					try:
						vagrant = runcmd_nodb_win.delay(action, rule_name, rule_uuid, windows)
						#logstring = action +','+ rule_name +','+ windows
						write_row(time_to_log, rule_name, action, mitre_phase, mitre_tech, windows)
						#if you want to post to slack uncomment this and set the slack hook above
						#json = {'text': "Automated Purple Team --> Simulation: {} | Action: {}  | Host: {} | Execution Time: {} UTC".format(rule_name,action,windows,datetime.datetime.utcnow())}
						#post_to_slack(hook,json)
						time.sleep(randint(2,30))
					
					except Exception as e:
						print(e)

			elif rule_os == "osx":
				print "OS matched OSX...sending to the OSX vagrant"
				for action in purple_actions:
					print("Running: {}".format(action))
					timenow = datetime.datetime.utcnow()
					date = timenow.strftime('%Y-%m-%d')
					hourminsec = timenow.strftime('%H:%M:%S')
					time_to_log = date+" "+hourminsec
					try:
						vagrant = runcmd_nodb_osx.delay(action, rule_name, rule_uuid, osx)
						write_row(time_to_log, rule_name, action, mitre_phase, mitre_tech, osx)
						#if you want to post to slack uncomment this and set the slack hook above
						#json = {'text': "Automated Purple Team --> Simulation: {} | Action: {}  | Host: {} | Execution Time: {} UTC".format(rule_name,action,osx,datetime.datetime.utcnow())}
						#post_to_slack(hook,json)
						time.sleep(randint(2,30))
						
					except Exception as e:
						print(e)
			else:
				print "I received an unknown OS"
	except KeyboardInterrupt:
		print("CTRL-C received, exiting...")

	except Exception, e:
		print e


def parse_yaml(ioc_filename):
	print("YAML FILE: {}".format(ioc_filename))
	try:
		raw_iocs = yaml.load_all(open(ioc_filename,'r').read())
		start_log("Adversarial Simulation", "1.0")

		for raw_ioc in raw_iocs:
			
			scenario = raw_ioc.get('meta').get('scenario')
			purple = raw_ioc.get('meta').get('purple_actions')
			#if we cant find the scenario tag, default to run_uuid
			if not scenario:
				run_uuid(ioc_filename)
			#if the scenario field is found and if it's true run the run_scenario function
			if scenario == True:
				run_scenario(ioc_filename)
		close_log()

	except KeyboardInterrupt:
		print("CTRL-C received, exiting...")

	except Exception, e:
		print e

if len(sys.argv) < 2:
    print("You must specify a filename")
    sys.exit(0)
else:
    parse_yaml(sys.argv[1])
