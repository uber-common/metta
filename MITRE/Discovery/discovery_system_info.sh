#!/bin/bash

# MITRE PHASE: DISCOVERY
# MITRE TECHNIQUE: System Information Discovery

# All the wmic commands you can handle dawg

echo "Windows Command: gpresult -r"
vagrant winrm -c "gpresult -r" #gpresult -r usage, process_name:gpresult.exe cmdline:"-r"

echo "Windows Command: gpresult -z"
vagrant winrm -c "gpresult -z" #gpresult -z usage, process_name:gpresult.exe cmdline:"-z"