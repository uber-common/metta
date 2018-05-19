import datetime
import json
import logging
import os
import shlex
import subprocess
import sys
import time

from celery import Celery
from config import BaseConfig

config = BaseConfig()
sim_vagrant = Celery('tasks', backend=config.redisbackend, broker=config.redisbroker)

# redis seems to be pickig up the logger stuff on its own
# logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')


@sim_vagrant.task
def alive_vagrant():
    return "pong"


@sim_vagrant.task
def runcmd_nodb_win(vagrant_cmd, rule_name, rule_uuid, hostname):
    try:
        logging.info('#####  We made it to the vagrant function  ###### ')
        logging.info("'Running: {} with Rule GUID: {} against vagrant {}".format(vagrant_cmd, rule_uuid, hostname))
        cmd = 'vagrant winrm {} -c "{}"'.format(hostname, vagrant_cmd)
        args = shlex.split(cmd)
        logging.info("Arguments passed to vagrant are: {}".format(args))
        dovagrant = subprocess.Popen(args)
    except Exception as e:
        print(e)
        logging.warning(e)


@sim_vagrant.task
def runcmd_nodb_osx(vagrant_cmd, rule_name, rule_uuid, hostname):
    try:
        logging.info('#####  We made it to the vagrant function  ###### ')
        logging.info("'Running: {} with Rule GUID: {} against vagrant {}".format(vagrant_cmd, rule_uuid, hostname))
        cmd = 'vagrant ssh {} -c "{}"'.format(hostname, vagrant_cmd)
        args = shlex.split(cmd)
        logging.info("Arguments passed to vagrant are: {}".format(args))
        dovagrant = subprocess.Popen(args)
    except Exception as e:
        print(e)
        logging.warning(e)


@sim_vagrant.task
def runcmd_nodb_linux(vagrant_cmd, rule_name, rule_uuid, hostname):
    try:
        logging.info('#####  We made it to the vagrant function  ###### ')
        logging.info("'Running: {} with Rule GUID: {} against vagrant {}".format(vagrant_cmd, rule_uuid, hostname))
        cmd = 'vagrant ssh {} -c "{}"'.format(hostname, vagrant_cmd)
        args = shlex.split(cmd)
        logging.info("Arguments passed to vagrant are: {}".format(args))
        dovagrant = subprocess.Popen(args)
    except Exception as e:
        print(e)
        logging.warning(e)


@sim_vagrant.task
def runcmd_nodb_kali(vagrant_cmd, rule_name, rule_uuid, hostname):
    try:
        logging.info('#####  We made it to the vagrant function  ###### ')
        logging.info("'Running: {} with Rule GUID: {} against vagrant {}".format(vagrant_cmd, rule_uuid, hostname))
        cmd = 'vagrant ssh {} -c "{}"'.format(hostname, vagrant_cmd)
        args = shlex.split(cmd)
        logging.info("Arguments passed to vagrant are: {}".format(args))
        dovagrant = subprocess.Popen(args)
    except Exception as e:
        print(e)
        logging.warning(e)
