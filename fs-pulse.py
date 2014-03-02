#!/usr/bin/env python
# Public: fs-pulse.py
#
# SupFubot project - Interval Status Scraper
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
name = "hpcloud-incident-status-scraper"

# Type can be Incident or Maintenance but really almost always incident
type = "incident"

# Use LXML to grab the document and save it as an object
entry  = requests.get("https://community.hpcloud.com/status")
tree = html.fromstring(entry.text)

# Grabs all of the incident links and splits out the url portion, we just need the nodeId's as integers
# aww yiss list comprehensions (freddie)
links = [i.split('/')[3] for i in tree.xpath("//a[contains(@href, 'incident')]/@href")]
links = [ int(x) for x in links ]


# Writes to file to be grabbed by fustatus-item
f = open('/home/hpcsint/fustatus/incidents/currentmaster.list','w')
f.write(str(links) + '\n')
f.close()

#with open("incidents/currentmaster.list") as f:
#        nodes = f.read()
#print nodes.replace("[", "").replace("]", "").strip().split(',')

nodes = "/home/hpcsint/fustatus/incidents/currentmaster.list"

with open(nodes) as f:
        nodes = f.read()
nodes =  nodes.replace("[", "").replace("]", "").strip().split(',')

#print nodes
