**FuStatus Logical Outline - Incident and Maintenance Notifications**

**fs-pulse.py  [completion: 100%]**

 - Scrapes status page every minute
 -   'incident' Nodes on page are counted and stored in a flat file as a list item
 
**fs-item.py   [completion: 100%]**
 -  spiders each node URL gathered by fs-pulse.py every 2 minutes and scrapes for the following information, storing it in a dictionary format:
 	```
{
'status': 'MONITORING', 
'sub_status': None, 
'time_start': '<timestamp>', 
'interval': None, 
'nodeId': '2466', 
'time_end': '<timestamp>', 
'link': 'https://community.hpcloud.com/status/incident/2466', 
'desc': 'We are currently testing status notifications. THERE IS NO ACTIVE INCIDENT.   Please disregard this message.'
}
```
 - saves these entries, or 'nodes' as .json files in a directory called './incidents',  one per unique nodeId
 
**fs-event.py  [completion: 00%]**
uses python-crontab to generate, maintain and delete cron jobs for periodic API  interactions

 - monitors current 'status' of incidents in './incidents'
 - indexes node files and checks for new files once every minute.
 - determines there is a new '/incident' node (file) and reads it for status ONGOING
 - When new node status is ONGOING
      - node file is copied to './incidents/active' directory
      - a sub-status of OPENED is assigned for the first interval (i.e., ONGOING:OPENED)
 - interval marker is set to [0]
 - [ACTION] API notification is sent to listening roomId(s) via fs-action.py 
 - When a node status has been ONGOING for 28 minutes
- Status ONGOING is verified against node file in './incidents/active'
	-OPENED sub-status is removed.
	- Interval marker is updated to [1]
 - a 'duration' timestamp (POSIX), calculated from the arbitrary start time entered by agent, is appended based on the current interval

**fs-action.py**
Houses all [HipChat] API interaction methods.

- [ACTION] API notifications sent to listening roomId(s)
```
    <strong>NOTICE</strong> New Status Message Posted: 
    <a href="_link_">_title_</a>
    <strong>Status:</strong> OPENED" }' \
    https://api.hipchat.com/v2/room/437235/notification? \
    auth_token=$HUBOT_TEST_TOKEN 
```


	
