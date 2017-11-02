#!/bin/bash

# MITRE PHASE: DISCOVERY
# MITRE TECHNIQUE: System Time Discovery

# System Time Discovery (various)

echo "Windows Command: w32tm /tz"
vagrant winrm -c "w32tm /tz" #w32tm /tz
