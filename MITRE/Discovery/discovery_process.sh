#!/bin/bash

# MITRE PHASE: DISCOVERY
# MITRE TECHNIQUE: Process Discovery

# Process Discovery Commands

echo "Windows Command: wmic process list /format:list"
vagrant winrm -c "wmic process list /format:list" #WMIC process usage,cmdline:"process" process_name:wmic.exe

echo "Windows Command: tasklist /v"
vagrant winrm -c "tasklist /v" #tasklist execution, process_name:tasklist





