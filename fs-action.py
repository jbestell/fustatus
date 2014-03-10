#!/usr/bin/env python
# Public: fs-action.py
#
# SupFubot project - API Interaction Handler
# For details see:
# https://github.com/jbestell/fustatus

import os
import time
import argparse
from datetime import datetime
import json
import requests

# Get incident json passed to script
parser = argparse.ArgumentParser()
parser.add_argument('active_incident_file', help='<path to active incident file>')
args = parser.parse_args()

# For Reverse assignment of POSIX timestamp, to human-readable time.
# In our current context, the json array has timestamps such as "1394146800" and we need
# to convert them back to something we can pass in the API call.
def hr_timestamp (string, outformat):
        "Convert a POSIX timestamp to a Human-Readable String"
        hr_date = datetime.fromtimestamp(float(int(string))).strftime(outformat)
        return hr_date;
# Text and HTML formatting functions
def boldit (string):
      string = '<strong>&nbsp;' + string + '</strong>'
      return string
def emphit (string):
      string = '<em>&nbsp;' + string + '</em>'
      return string
def imgit (url, file):
      string = '<img src=\"' + url + file + '\">'
      return string
def urlit (href, title):
      string = '<a href=\"' + href + '\">' + title + '</a>'
      return string
# Fancy sauce to cust the description to a manageable length
def cut_desc (content, length, suffix):
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length+1].split(' ')[0:-1]) + suffix
# Inelegant, but required due to format limitations in Hipchat
brk = '<br />'

# All this stuff is specific to the data body of the hipchat API call
# File names for common images used in API calls
imgs = {
             "adv"  : "advisory_20.png",
             "arup" : "arrowup_20.png",
             "dash" : "dash_20.png",
             "intr" : "interval_20.png",
             "notc" : "notice_20.png",
             "plsg" : "plusgreen_20.png",
             "rsvd" : "resolved_20.png"
            }
strs =      {
             'notc' : 'Incident Posted:&nbsp;',
             'indt':  'Incident:&nbsp;',
             'start': 'Start:&nbsp;',
             'end'  : 'End:&nbsp;',
             'pstrt': 'Posted Start:&nbsp;',
             'pend' : 'Posted End:&nbsp;',
             'desc' : 'Description:&nbsp;',
             'stat' : 'Current Status:&nbsp;'
            }
msg_color = [ "red", "green", "yellow", "gray", "purple" ]
msg_format = [ "html", "text" ]
# Requests expects a dict here, so oblige
headers = { "Content-Type" : "application/json" }

# Room ID's to notify, have to loop over this with the API request if there are multiple rooms
rooms = ['437185', '437235', '472193']

# API URL concatenation with room !!REFACTOR  this
hpcapi_url = 'https://api.hipchat.com/v2/room/' + rooms[2] + '/notification?auth_token='

# need to make this persist on the server independent of no interactive session
hpctkn = os.environ['hutkn_sbx']

# Swift container where icon images reside - tenant estellj-web in AW2
img_url = "https://region-a.geo-1.objects.hpcloudsvc.com/v1/15669176189025/hpc_img_icons/"

# ----  Down to bitness

# Open the desired file specified by the script argument
with open(args.active_incident_file, 'r') as file:
    indt = json.load(file)

# Check End time - if unset, print dashes
    if indt['time_end'] != None:
        time_end = hr_timestamp (indt['time_end'], "%A, %B %d, %Y %I:%M %p %Z")
    else:
        time_end = "---"

indt['status'] = 'MONITORING'

# This is the Incident Notification body.  Once all contexts are better defined,
# this can probably be functionalized !!REFACTOR
message = (imgit(img_url, imgs['notc']) +
           boldit(strs['indt']) + indt['title'] + brk +
           imgit(img_url, imgs['dash'])+
           boldit(strs['stat'] + indt['status']) + brk +
           boldit(strs['pstrt'] +
           emphit(hr_timestamp (indt['time_start'], "%A, %B %d, %Y %I:%M %p %Z"))) + brk +
           boldit(strs['pend'] + emphit(time_end)) + brk +
           boldit(strs['desc']) + cut_desc(indt['desc'], 150, '...&nbsp;' +
           urlit(indt['link'], 'read more'))
          )

# Construct the data body in JSON. This could probably also be a function too !!REFACTOR

json_pl =  json.dumps({ "notify" : True,
            "color" : msg_color[2],
            "message_format" : msg_format[0],
            "message" : message
          })

# Use Requests to perform the API call
#print hpcapi_url + hpctkn + '\n\n'
#print json_pl + '\n\n'

r = requests.post(hpcapi_url + hpctkn, data=json_pl, headers=headers)

# Show Response for troubleshooting. Requests is awesome and this object
# can probably be used for all sorts of cool shit!!REFACTOR
print r.text
