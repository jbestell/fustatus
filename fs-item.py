#!/usr/bin/env python
# Public: fs-item.py
#
# SupFubot project - Item Event Status Processor
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
name = "hpcloud-incident-status-processor"

# Path to the incidents directory
indt_path = '/home/hpcsint/dev/fustatus/incidents/'

# Possible Status values
current_status = ['ONGOING', 'MONITORING', 'RESOLVED']

# Get incidents passed to script
parser = argparse.ArgumentParser()
#parser.add_argument('incident', help='4-digit number of incident to parse and store')
parser.add_argument('incident_file', help='<path to file with incidents to scrape>')
args = parser.parse_args()

# Fancy reassignment of string to POSIX timestamp. In our current context:
# "Monday, February 24, 2014 11:30 AM UTC" strptime([var],"%A, %B %d, %Y %I:%M %p %Z") -->  strftime("%s",[var])
def timestamp (str, informat, outformat):
        "Convert a string date to a POSIX timestamp"
        global time
        str = time.strptime(str, informat)
        str = strftime(outformat,str)
        return str;

# Argument specifies file passed in, which is a comma-separated string of 'node' ID's
nodeList_s  = args.incident_file

# Grab the file written by fs-pulse.py and reads it in as a list for processing
with open(nodeList_s) as f:
        nodeList_s = f.read()
nodeList_l =  nodeList_s.replace("[", "").replace("]", "").strip().split(', ')

# Type can be Incident or Maintenance but really almost always incident
# !!CONSIDER REMOVING
type = "incident"

# Iterate through nodIed's and build a Dictionary for each, writing to individual files
for nodeId_s in nodeList_l:
        
        # The working permalink to the incident report
        start_url = "https://community.hpcloud.com/status/" + type + "/" + nodeId_s

        # Use LXML to grab the document and save it as an object
        entry  = requests.get("https://community.hpcloud.com/status/" + type + "/" + nodeId_s)
        tree = html.fromstring(entry.text)

        # These are all the required XPATH matches in one spot  
        # nodeId is the div ID for each
        node_match   = '//*[@id="node-' + nodeId_s
        match_title = '//*[@id="page-title"]/text()'
        match_desc   = node_match + '"]/div/div[last()]/div/div/descendant::*/text()'
        # 'status' is always the last element in the group of children, so use XPATH thusly
        match_status = node_match + '"]/div/div[1]/div[last()]/div[last()]/div/text()'
        # Multiple possibilities for the location of 'Start Time' and 'End Time' based 
        # on which details are specified in the incident form
        match_start1 = node_match + '"]/div/div[1]/div[2]/div/div/div[1]/span/text()'
        match_start2 = node_match + '"]/div/div[1]/div[1]/div/div/div[1]/span/text()'
        match_start3 = node_match + '"]/div/div[1]/div[2]/div/div/div[1]/span/text()'
        match_end1   = node_match + '"]/div/div[1]/div[2]/div/div/div[2]/span/text()'
        match_end2   = node_match + '"]/div/div[1]/div[1]/div/div/div[2]/span/text()'
        match_end3   = node_match + '"]/div/div[1]/div[2]/div/div/div[2]/span/text()'
        
        # The Dictionary object 
        nodeProps_d = {}
        nodeProps_d['nodeId'] = nodeId_s
        nodeProps_d['link'] = start_url
        nodeProps_d['title'] = tree.xpath(str(match_title))[0]
        #Set these to 'None' for now, as they are to be modified later in the cycle
        nodeProps_d['sub_status'] = None
        nodeProps_d['interval'] = None
        # Get the description - join if multiple descendant paragraphs.
        nodeProps_d['desc'] = tree.xpath(str(match_desc))
        nodeProps_d['desc'] = " ".join(nodeProps_d['desc'])

        nodeProps_d['status'] = tree.xpath(str(match_status))[0].upper()


        # This is the tricky bit - there can be as many as four //div/ child matches for <div class="filed-label">
        # and it varies based on whether:
        # -> the affected product is set
        # -> the end time is toggled
        # End time is a little easier to deal with as it only occurs at the end of an incident, or a post-mortem
        # 'confession' post or after-incident advisory. In all cases we need to match and capture all of these
        # items whether or not they exist.

        # A Status of RESOLVED is the best indicator that the End Field might be populated, so use it for conditionals.
        if nodeProps_d['status'] in (current_status[2]):
            try:
                #Matches if Product is Set
                nodeProps_d['time_start'] = timestamp(tree.xpath(match_start1)[0], "%A, %B %d, %Y %I:%M %p %Z", "%s")

            except IndexError:

                nodeProps_d['time_start'] = timestamp(tree.xpath(match_start2)[0], "%A, %B %d, %Y %I:%M %p %Z", "%s")

            try:

                # Matches if Product AND End Date is Shown  /div/div[1]/div[2]/div/div/div[2]/span/text()')[0]
                nodeProps_d['time_end'] = timestamp(tree.xpath(match_end1)[0], "%A, %B %d, %Y %I:%M %p %Z", "%s")

            except IndexError:
                try:
                    # Matches if only Start and End Date is Shown /div/div[1]/div[1]/div/div/div[2]/span
                    nodeProps_d['time_end'] = timestamp(tree.xpath(match_end2)[0], "%A, %B %d, %Y %I:%M %p %Z", "%s")

                except IndexError:
                    # Resolved, but No Product or End Date - Set it to Start Date (legacy)
                    nodeProps_d['time_end'] = nodeProps_d['time_start']

                else:
                    # All Three: Product, Start and End are set /div/div[1]/div[2]/div/div/div[2]/span
                    nodeProps_d['time_end'] = timestamp(tree.xpath(match_end3)[0], "%A, %B %d, %Y %I:%M %p %Z", "%s")
                 
            else:
                # Pass for all other conditions (ultimate)
                #nodeProps_d['time_end'] = None
                pass

        # If the status is ONGOING or MONITORING
        elif nodeProps_d['status'] in (current_status[0], current_status[1]):

            try:
                # ONG / MON - Matches Start if Product IS set.
                nodeProps_d['time_start'] = timestamp(tree.xpath(match_start1)[0], "%A, %B %d, %Y %I:%M %p %Z", "%s")

            except IndexError:

                # ONG / MON - Matches Start if Product IS NOT set.
                nodeProps_d['time_start'] = timestamp(tree.xpath(match_start2)[0], "%A, %B %d, %Y %I:%M %p %Z", "%s")

            #no END Date, so...
                nodeProps_d['time_end'] = None

        else:
            # For all other scenarios, just null them both out.
            nodeProps_d['time_start'] = None
            nodeProps_d['time_end'] = None


        try:
            item_array = json.dumps(nodeProps_d, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
            f = open(indt_path + nodeId_s + '.json', 'w')
            f.write(item_array + '\n')
            f.close()
        except IOError:
            print "Error: can\'t find file or read data"
        else:
            print nodeId_s + ".json written successfully"
# for debugging
#print nodes

