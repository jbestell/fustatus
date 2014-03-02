#!/usr/bin/env python
# Public: fs-event.py
#
# SupFubot project - Event Controller 
# For details see:
# https://github.com/jbestell/fustatus

import time
import argparse
from time import strftime
from time import mktime
from datetime import datetime
import json
from lxml import html
import lxml.html
import requests

#Name this script
name = "hpcloud-incident-event-handler"

''' fs-event.py [completion: 00%] uses python-crontab to generate, maintain and delete cron jobs for periodic API interactions

	-- monitors current 'status' of incidents in './incidents'
	-- indexes node files and checks for new files once every minute.
	-- determines there is a new '/incident' node (file) and reads it for status ONGOING
	-- When new node status is ONGOING
	-- node file is copied to './incidents/active' directory
	-- a sub-status of OPENED is assigned for the first interval (i.e., ONGOING:OPENED)
	-- interval marker is set to [0]
	-- [ACTION] API notification is sent to listening roomId(s) via fs-action.py
	-- When a node status has been ONGOING for 28 minutes
	-- Status ONGOING is verified against node file in './incidents/active' -OPENED sub-status is removed.
	-- Interval marker is updated to [1]
	-- a 'duration' timestamp (POSIX), calculated from the arbitrary start time entered by agent, is appended based on the current interval
'''

#file = open('/home/hpcsint/fustatus/incidents/currentmaster.list')

# grabs the file written by fustatus-scrape and reads it in as a list for processing
with open('/home/hpcsint/fustatus/incidents/currentmaster.list') as f:
        nodes = f.read()
#nodes =  nodes.replace("[", "").replace("]", "").strip().split(', ')
nodes = ['2464', '2441']

for node in nodes:
	with open('/home/hpcsint/fustatus/incidents/' + node + '.json') as f:
	        items = f.read()
items = items.split(",", 200)

#print node[1]
print items[1]








