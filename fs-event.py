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

# Path to the incidents directory
indt_path = '/home/hpcsint/dev/fustatus/incidents/'
indt_file = 'current'

# Possible Status values
current_status = ['ONGOING', 'MONITORING', 'RESOLVED']


''' fs-event.py [completion: 00%] uses python-crontab to generate, maintain and delete cron jobs for periodic API interactions

  -- [ACTION] API notification is sent to listening roomId(s) via fs-action.py
  -- When a node status has been ONGOING for 28 minutes
  -- Status ONGOING is verified against node file in './incidents/active' -OPENED sub-status is removed.
  -- Interval marker is updated to [1]
  -- a 'duration' timestamp (POSIX), calculated from the arbitrary start time entered by agent, is appended based on the current interval
'''

# -- monitors current 'status' of incidents in './incidents'

# Open incidents 'current'
with open(indt_path + indt_file) as f:
        nodes = f.read()
     # Reclaim list values and strip brackets - probably need to do this before here
        nodes =  nodes.replace("[", "").replace("]", "")
        nodes = nodes.strip().split(', ')
        nodes = sorted([int(l[0:4]) for l in nodes], reverse=True)


#  -- reads through all node files in incident/ and checks for status ONGOING
# When a node's status is ONGOING and 'sub_status' is None, a sub-status 
# of OPENED is assigned for the first interval. 'interval' marker is set to 0.
# Node file is then copied to './incidents/active' directory

for node in sorted(nodes):
         # Open each .json file 
        with  open(indt_path + str(node) + '.json', 'r') as file:
            indt_array = json.load(file)
      	# Determine if status is ONGOING and sub_status is None
        if  indt_array['status'] == 'ONGOING' and not indt_array['sub_status']:
            # If so, set the sub_status and the interval
            indt_array['sub_status'] = 'OPENED'
            indt_array['interval'] = 0
	    # Write the newly modified array to active/
            try:
                item = json.dumps(indt_array, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
                f = open(indt_path + 'active/' + indt_array['nodeId'] + '.json', 'w')
                f.write(item + '\n')
                f.close()
            except IOError:
                        print "Error: can\'t find file or read data"

        #else:
        #    print indt_array['desc']

#        with open(file) as f:
#                item = f.read()
#        print item



