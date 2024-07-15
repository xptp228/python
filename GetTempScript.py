#!/usr/bin/env python3
# This script is used to pass the host's temperature values ​​to Homeassistant, running on a Proxmox VM.
import os
import logging
import subprocess
from requests import post

# defining host
https = False
host = ""
port = ""
token = ""

# Get temperature from system
temp=subprocess.check_output("cat /sys/class/thermal/thermal_zone2/temp", shell=True)

# Parse temperature value from string
temp = [int(i) for i in temp.split() if i.isdigit()][0]

# verifing if host is up and running
host_up = os.system(f"ping -c 5 {host} > /dev/null 2>&1") == 0

# Constructing the url
if https == True:
  url = "https://" + host + ":" + port + "/api/states/input_number.cpu_temp"
else:
  url = "http://" + host + ":" + port + "/api/sates/input_number.cpu_temp" 

# constructing the autorization string with token
headers = {
  "Authorization": "Bearer " + token,
  "content-type": "application/json"
}

# Formating the data
data = '{"state": %s}' % temp

# Defining the post being delivered to hass VM, if it is available
if host_up == True:
  response = post(url, headers=headers, data=data, verify=True)
#else:
  # logging, still under construction
