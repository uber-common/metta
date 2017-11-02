#!/bin/bash

# MITRE PHASE: DISCOVERY
# MITRE TECHNIQUE: Query Registry

# Query Registry

echo "Windows Command: REG QUERY HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs"
vagrant winrm -c "REG QUERY HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs" #query a reg value from the command line
