#!/bin/bash

# MITRE PHASE: DISCOVERY
# MITRE TECHNIQUE: System Owner/User Discovery

# System Owner/User Discovery commands (various)

echo "Windows Command: set"
vagrant winrm -c "cmd.exe /c set" #set usage

echo "Windows Command: tasklist /v"
vagrant winrm -c "tasklist /v" #tasklist execution, process_name:tasklist /v will give username

echo "Windows Command: net user"
vagrant winrm -c "net user automation" #net user
