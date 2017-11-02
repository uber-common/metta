#!/bin/bash

# MITRE PHASE: DISCOVERY
# MITRE TECHNIQUE: System Service Discovery

# All the wmic commands you can handle dawg

echo "Windows Command: wmic service"
vagrant winrm -c "wmic service" #WMIC service usage,process_name:wmic.exe cmdline:"wmic service"

echo "Windows Command: tasklist /svc"
vagrant winrm -c "tasklist /svc" #tasklist /svc usage
