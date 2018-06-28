#author Chris Gates - Uber
#additions Maus - Uber
#additions author Russ Nolen - Riot Games

# adversarial simulation engine
from __future__ import print_function

import datetime
import json
import logging
import os
import subprocess
import sys
import time
from argparse import ArgumentParser
from random import randint

import requests

import yaml
from reporting.log_to_file import *
from workers.vagranttasks import *

try:
    import configparser as ConfigParser  # Python 3
except ImportError:
    import ConfigParser                  # Python 2

#slack hook URL
hook = ""

#vagrant variables that get populated below
windows = " "
osx = " "
linux = " "

#banners for metta
banner = '''
   _____          __    __
  /     \   _____/  |__/  |______
 /  \ /  \_/ __ \   __\   __\__  \
/    Y    \  ___/|  |  |  |  / __ \_
\____|__  /\___  >__|  |__| (____  /
        \/     \/                \/
'''

banner2 = '''

 __   __  _______  _______  _______  _______
|  |_|  ||       ||       ||       ||   _   |
|       ||    ___||_     _||_     _||  |_|  |
|       ||   |___   |   |    |   |  |       |
|       ||    ___|  |   |    |   |  |       |
| ||_|| ||   |___   |   |    |   |  |   _   |
|_|   |_||_______|  |___|    |___|  |__| |__|

'''

#module to post to slack if you set the webhook in config.ini
def post_to_slack(hook,json):
    try:
        r = requests.post(hook, json=json)
    except Exception as e:
        print(e)

def run_scenario(ioc_filename):
    try:
        print("### Running the Scenario ###")
        raw_iocs = yaml.load_all(open(ioc_filename,'r').read())

        timenow = datetime.datetime.utcnow()

        for raw_ioc in raw_iocs:
            scenario = raw_ioc.get('meta').get('scenario_actions')
            rule_name = raw_ioc.get('name')
            print("### {} ###".format(rule_name))

            scenario_actions = []
            #read the steps from purple_actions in yaml and load them into purple_actions
            for x in range(1,len(scenario)+1):
                scenario_actions.append(raw_ioc.get('meta').get('scenario_actions').get(x))

            for uuid_file in scenario_actions:
                run_uuid(uuid_file)

    except Exception as e:
        print(e)

def run_uuid(ioc_filename):
    try:
        print("\nRunning UUID actions inside:{}".format(ioc_filename))

        raw_iocs = yaml.load_all(open(ioc_filename,'r').read())


        for raw_ioc in raw_iocs:
            rule_name = raw_ioc.get('name')
            rule_uuid = raw_ioc.get('uuid')
            rule_os = raw_ioc.get('os')
            mitre_phase = raw_ioc.get('meta').get('mitre_attack_phase')
            mitre_tech = raw_ioc.get('meta').get('mitre_attack_technique')
            purple = raw_ioc.get('meta').get('purple_actions')

            if not purple:
                print("No Purple Actions detected you've probably messed up your scenario.yml...")
                sys.exit(0)

            purple_actions = []
            #read the steps from purple_actions in yaml and load them into purple_actions
            for x in range(1,len(purple)+1):
                purple_actions.append(raw_ioc.get('meta').get('purple_actions').get(x))

            if rule_os == "windows":
                print("OS matched Windows...sending to the windows vagrant")
                for action in purple_actions:
                    print("Running: {}".format(action))
                    timenow = datetime.datetime.utcnow()
                    date = timenow.strftime('%Y-%m-%d')
                    hourminsec = timenow.strftime('%H:%M:%S')
                    time_to_log = date+" "+hourminsec
                    try:
                        vagrant = runcmd_nodb_win.delay(action, rule_name, rule_uuid, windows)
                        data = json.dumps({'time' : time_to_log, 'rule_name' : rule_name, 'action' : action, 'mitre_attack_phase' : mitre_phase, 'mitre_attack_technique' : mitre_tech, 'host' : windows})
                        logging.info(data)
                        write_row(time_to_log, rule_name, action, mitre_phase, mitre_tech, windows)

                        #if you want to post to slack uncomment this and set the slack hook above
                        #json = {'text': "Automated Purple Team --> Simulation: {} | Action: {}  | Host: {} | Execution Time: {} UTC".format(rule_name,action,windows,datetime.datetime.utcnow())}
                        #post_to_slack(hook,json)

                        time.sleep(randint(2,30))
                    except Exception as e:
                        print(e)

            elif rule_os == "osx":
                print("OS matched OSX...sending to the OSX vagrant")
                for action in purple_actions:
                    print("Running: {}".format(action))
                    timenow = datetime.datetime.utcnow()
                    date = timenow.strftime('%Y-%m-%d')
                    hourminsec = timenow.strftime('%H:%M:%S')
                    time_to_log = date+" "+hourminsec
                    try:
                        vagrant = runcmd_nodb_osx.delay(action, rule_name, rule_uuid, osx)
                        data = json.dumps({'time' : time_to_log, 'rule_name' : rule_name, 'action' : action, 'mitre_attack_phase' : mitre_phase, 'mitre_attack_technique' : mitre_tech, 'host' : osx})
                        logging.info(data)
                        write_row(time_to_log, rule_name, action, mitre_phase, mitre_tech, osx)

                        #if you want to post to slack uncomment this and set the slack hook above
                        #json = {'text': "Automated Purple Team --> Simulation: {} | Action: {}  | Host: {} | Execution Time: {} UTC".format(rule_name,action,osx,datetime.datetime.utcnow())}
                        #post_to_slack(hook,json)

                        time.sleep(randint(2,30))
                    except Exception as e:
                        print(e)

            elif rule_os == "linux":
                print("OS matched Linux...sending to the Linux vagrant")
                for action in purple_actions:
                    print("Running: {}".format(action))
                    timenow = datetime.datetime.utcnow()
                    date = timenow.strftime('%Y-%m-%d')
                    hourminsec = timenow.strftime('%H:%M:%S')
                    time_to_log = date+" "+hourminsec
                    try:
                        vagrant = runcmd_nodb_linux.delay(action, rule_name, rule_uuid, linux)
                        data = json.dumps({'time' : time_to_log, 'rule_name' : rule_name, 'action' : action, 'mitre_attack_phase' : mitre_phase, 'mitre_attack_technique' : mitre_tech, 'host' : linux})
                        logging.info(data)
                        write_row(time_to_log, rule_name, action, mitre_phase, mitre_tech, linux)

                        #if you want to post to slack uncomment this and set the slack hook above
                        #json = {'text': "Automated Purple Team --> Simulation: {} | Action: {}  | Host: {} | Execution Time: {} UTC".format(rule_name,action,osx,datetime.datetime.utcnow())}
                        #post_to_slack(hook,json)

                        time.sleep(randint(2,30))
                    except Exception as e:
                        print(e)
            else:
                print("I received an unknown OS")
    except KeyboardInterrupt:
        print("CTRL-C received, exiting...")
    except Exception as e:
        print(e)


def parse_yaml(ioc_filename):
    '''
    Parse Metta format simulation file (eventually move everything to RC format)
    '''
    print(banner2)
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

    except Exception as e:
        print(e)


def rc_executor_append(executor_name):
    if executor_name == "command_prompt":
        prefix = "cmd.exe /c "
    elif executor_name == "powershell":
        prefix = "cmd.exe /c powershell.exe iex "
    elif executor_name == "sh":
        prefix = "/bin/sh -c "
    elif executor_name == "bash":
        prefix = "/bin/bash -c "
    elif executor_name == "manual":
        prefix = "manual"
    else:
        print("received an unknown executor_name")
    return prefix


def run_rc_atomictest(ioc_filename, TestName):
    try:
        print("\nRunning Red Canary Atomic Tests inside:{}".format(ioc_filename))

        raw_iocs = yaml.load_all(open(ioc_filename,'r').read())

        # RC pulls theirs from github master, if this is a feature ppl want request it
        # otherwise i'm gonna assume you have the folder of atomics checked out

        for raw_ioc in raw_iocs:
            display_name = raw_ioc.get('display_name')
            print("MITRE ATT&CK Technique: {}".format(display_name))

            attack_technique = raw_ioc.get('attack_technique')
            print("MITRE ATT&CK TechniqueID: {}".format(attack_technique))
            print("\n")

            # Parse the atomc_tests fields (fingers crossed)
            atomic_tests = raw_ioc.get('atomic_tests')
            #print(atomic_tests)


            test = list(filter(lambda atomic_tests: atomic_tests['name'] == TestName, atomic_tests))
            if len(test) != 0:
                print("{} - Atomic Red Team Test Found...processing...".format(TestName))
                print(test)

                if 'executor' in test:
                    print('found executor')
                else:
                    print('sad')
                    #executor_command = atomic.get('executor').get('command')
                    # print(executor_command)


            else:
                print("########## ERROR ##########\nCould not find the Atomic Red Team Test named: {} ! Check TestName value!".format(TestName))
                sys.exit
            #for atomic in atomic_tests:
            '''

                #name = atomic.get('name')
                #print(name)
                if name == TestName:
                    print("Found the specified test name: {}...continuing".format(TestName))
        
                    description = atomic.get('description')
                    print("Atomic Test Description: {}".format(description))

                    input_arguments = atomic.get('input_arguments')
                    print('###DEBUG###\n{}\n###DEBUG###'.format(input_arguments))
                
                    if input_arguments:
                    input_arguments_input_file = atomic.get('input_arguments').get('input_file')
                    input_arguments_output_file = atomic.get('input_arguments').get('output_file')
                    if input_arguments_input_file:
                        print('###DEBUG###\n{}\n###DEBUG###'.format(input_arguments_input_file))
                        input_file_desc = atomic.get('input_arguments').get('input_file').get('description')
                        input_file_type = atomic.get('input_arguments').get('input_file').get('type')
                        input_file_default = atomic.get('input_arguments').get('input_file').get('default')
                        print('###DEBUG###\n{}\n###DEBUG###'.format(input_file_default))
                    if input_arguments_output_file:
                        print('###DEBUG###\n{}\n###DEBUG###'.format(input_arguments_output_file))
                        output_file_desc = atomic.get('input_arguments').get('output_file').get('description')
                        output_file_type = atomic.get('input_arguments').get('output_file').get('type')
                        output_file_default = atomic.get('input_arguments').get('output_file').get('default')
                        print('###DEBUG###\n{}\n###DEBUG###'.format(output_file_default))
                    
                
                    executor_name = atomic.get('executor').get('name')
                    # print(executor_name)
                    executor_command = atomic.get('executor').get('command')
                    # print(executor_command)
                
                    #executor_steps = atomic.get('executor').get('steps')
                    #executor_input_arguments.input_file:


                    supported_platforms = atomic.get('supported_platforms')
                    # gonna have to for each here
                    print(supported_platforms)
                    for platform in supported_platforms:

                        if platform == "windows":
                            print("OS matched Windows...sending to the windows vagrant")
                            prefix = rc_executor_append(executor_name)
                            if prefix != "manual":
                                print(prefix + executor_command)
                            else:
                                print("Manual executor_command found - gotta do it by hand")
                    
                        elif platform == "osx":
                            print("OS matched OSX...sending to the OSX vagrant")
                            prefix = rc_executor_append(executor_name)
                            if prefix != "manual":
                                print(prefix + executor_command)
                            else:
                                print("Manual executor_command found - gotta do it by hand")

                        elif platform == "macos":
                            print("OS matched OSX...sending to the OSX vagrant")
                            prefix = rc_executor_append(executor_name)
                            if prefix != "manual":
                                print(prefix + executor_command)
                            else:
                                print("Manual executor_command found - gotta do it by hand")

                        elif platform == "linux":
                            print("OS matched Linux...sending to the Linux vagrant")
                            prefix = rc_executor_append(executor_name)
                            if prefix != "manual":
                                print(prefix + executor_command)
                            else:
                                print("Manual executor_command found - gotta do it by hand")

                        elif platform == "centos":
                            print("OS matched Linux...sending to the Centos Linux vagrant")
                            prefix = rc_executor_append(executor_name)
                            if prefix != "manual":
                                print(prefix + executor_command)
                            else:
                                print("Manual executor_command found - gotta do it by hand")

                        elif platform == "ubuntu":
                            print("OS matched Linux...sending to the Ubuntu Linux vagrant")
                            prefix = rc_executor_append(executor_name)
                            if prefix != "manual":
                                print(prefix + executor_command)
                            else:
                                print("Manual executor_command found - gotta do it by hand")

                        else:
                            print("We received an unknown OS")
                            sys.exit
                    print("\n")
                elif name != TestName:
                    next
                else:
                    print("########## ERROR ##########\nCould not find the test named: {} ! Check TestName value!".format(TestName))
                    sys.exit()
            
            for atomic in atomic_test:


            rule_os = raw_ioc.get('os')

            mitre_phase = raw_ioc.get('meta').get('mitre_attack_phase')
            mitre_tech = raw_ioc.get('meta').get('mitre_attack_technique')
            purple = raw_ioc.get('meta').get('purple_actions')

            if not purple:
                print("No Purple Actions detected you've probably messed up your scenario.yml...")
                sys.exit(0)

            purple_actions = []
            #read the steps from purple_actions in yaml and load them into purple_actions
            for x in range(1,len(purple)+1):
                purple_actions.append(raw_ioc.get('meta').get('purple_actions').get(x))

            if rule_os == "windows":
                print("OS matched Windows...sending to the windows vagrant")
                for action in purple_actions:
                    print("Running: {}".format(action))
                    timenow = datetime.datetime.utcnow()
                    date = timenow.strftime('%Y-%m-%d')
                    hourminsec = timenow.strftime('%H:%M:%S')
                    time_to_log = date+" "+hourminsec
                    try:
                        vagrant = runcmd_nodb_win.delay(action, rule_name, rule_uuid, windows)
                        data = json.dumps({'time' : time_to_log, 'rule_name' : rule_name, 'action' : action, 'mitre_attack_phase' : mitre_phase, 'mitre_attack_technique' : mitre_tech, 'host' : windows})
                        logging.info(data)
                        write_row(time_to_log, rule_name, action, mitre_phase, mitre_tech, windows)

                        #if you want to post to slack uncomment this and set the slack hook above
                        #json = {'text': "Automated Purple Team --> Simulation: {} | Action: {}  | Host: {} | Execution Time: {} UTC".format(rule_name,action,windows,datetime.datetime.utcnow())}
                        #post_to_slack(hook,json)

                        time.sleep(randint(2,30))
                    except Exception as e:
                        print(e)

            elif rule_os == "osx":
                print("OS matched OSX...sending to the OSX vagrant")
                for action in purple_actions:
                    print("Running: {}".format(action))
                    timenow = datetime.datetime.utcnow()
                    date = timenow.strftime('%Y-%m-%d')
                    hourminsec = timenow.strftime('%H:%M:%S')
                    time_to_log = date+" "+hourminsec
                    try:
                        vagrant = runcmd_nodb_osx.delay(action, rule_name, rule_uuid, osx)
                        data = json.dumps({'time' : time_to_log, 'rule_name' : rule_name, 'action' : action, 'mitre_attack_phase' : mitre_phase, 'mitre_attack_technique' : mitre_tech, 'host' : osx})
                        logging.info(data)
                        write_row(time_to_log, rule_name, action, mitre_phase, mitre_tech, osx)

                        #if you want to post to slack uncomment this and set the slack hook above
                        #json = {'text': "Automated Purple Team --> Simulation: {} | Action: {}  | Host: {} | Execution Time: {} UTC".format(rule_name,action,osx,datetime.datetime.utcnow())}
                        #post_to_slack(hook,json)

                        time.sleep(randint(2,30))
                    except Exception as e:
                        print(e)

            elif rule_os == "linux":
                print("OS matched Linux...sending to the Linux vagrant")
                for action in purple_actions:
                    print("Running: {}".format(action))
                    timenow = datetime.datetime.utcnow()
                    date = timenow.strftime('%Y-%m-%d')
                    hourminsec = timenow.strftime('%H:%M:%S')
                    time_to_log = date+" "+hourminsec
                    try:
                        vagrant = runcmd_nodb_linux.delay(action, rule_name, rule_uuid, linux)
                        data = json.dumps({'time' : time_to_log, 'rule_name' : rule_name, 'action' : action, 'mitre_attack_phase' : mitre_phase, 'mitre_attack_technique' : mitre_tech, 'host' : linux})
                        logging.info(data)
                        write_row(time_to_log, rule_name, action, mitre_phase, mitre_tech, linux)

                        #if you want to post to slack uncomment this and set the slack hook above
                        #json = {'text': "Automated Purple Team --> Simulation: {} | Action: {}  | Host: {} | Execution Time: {} UTC".format(rule_name,action,osx,datetime.datetime.utcnow())}
                        #post_to_slack(hook,json)

                        time.sleep(randint(2,30))
                    except Exception as e:
                        print(e)
            else:
                print("I received an unknown OS")
            '''
    except KeyboardInterrupt:
        print("CTRL-C received, exiting...")
    except Exception as e:
        print(e)

def parse_rc_yaml(ioc_filename, TestName):
    '''
    Parse Red Canary Atomic Testing format simulation file
    '''
    print(banner2)
    print("YAML FILE: {}".format(ioc_filename))
    try:
        atomics = yaml.load_all(open(ioc_filename,'r').read())
        start_log("Adversarial Simulation", "1.0")

        #run_rc_atomictest(ioc_filename)
        run_rc_atomictest(ioc_filename, TestName)
        
        close_log()

    except KeyboardInterrupt:
        print("CTRL-C received, exiting...")

    except Exception as e:
        print(e)

def main():
    parser = ArgumentParser(description="adversarial-simulation ")
    parser.add_argument("-f", "--simfile", action="store", default=None, required=False, dest="simfile", help="Path to simulation file you want to run")
    parser.add_argument("-rc", "--atomic", action="store", default=None, required=False, dest="atomic", help="Path to Atomic simulation file you want to run")
    parser.add_argument("-N",  action="store", default=None, required=False, dest="TestName", help="Test Name ex. 'Data Compressed - nix'")

    args = parser.parse_args()
    config = ConfigParser.RawConfigParser()

    try:
        config.read('config.ini')
    except Exception as e:
        print(e)
        sys.exit(0)

    global windows
    windows = config.get('vms','windows')

    global osx
    osx = config.get('vms', 'osx')

    global linux
    linux = config.get('vms','linux')

    global console_output
    console_log_output = config.get('console_log_output','enabled')

    # logging function to log json to a file
    logging.basicConfig(level=logging.DEBUG, format='%(message)s',filename='simulation.log', filemode='a')

    if console_log_output == 'True' or console_log_output == 'true':
        #logging function to give info to the console
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        # set a format which is simpler for console use
        formatter = logging.Formatter('%(levelname)-4s : %(message)s')
        # tell the handler to use this format
        console.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger('').addHandler(console)
    else:
        ''

    if args.simfile:
        print("Running Metta simulation file")
        parse_yaml(args.simfile)
    elif args.atomic:
        print("Running Red Canary Atomic Testing simulation file")
        if args.atomic and args.TestName is None: #and args.rport is None:
            parser.error("-rc/--atomic requires the -N (test name) argument.")
        else:
            TestName = args.TestName.strip()
            print(TestName)
            parse_rc_yaml(args.atomic, TestName)


if __name__=='__main__':
    main()
