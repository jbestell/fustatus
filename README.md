FuStatus Logical Outline - Incident and Maintenance Notifications

fustatus-scrape.py (incident_method)  [completion: 10%]

 -- Scrapes status page every 5 minutes 
 -- main page (i.e., /status ) is the focus, older nodes are not relevant to this process
 -- Nodes on page are counted and stored in a JSON array (dict)

fustatus-item.py   [completion: 80%]
 --  spiders each node URL from fustatus-scrape.py and scrapes for the following fields
	{
	'nodeid': '<node_id>',
	'desc': '<description_text>',
	'link': '<incident_post_url>',
	'status': 'ONGOING',
	'sub_status': None,
	'interval': None,
	'time_start': '1391706000',
	'time_end': '1391722500',
	'title': '<incident_title>’'
	}
 -- saves these entries, or 'nodes' as JSON files in a directory './incidents',  one per nodeId


fustatus-mon.py  [completion: 00%]

 -- monitors current status of incidents
 -- indexes node files and checks for new files once every minute.
 -- determines there is a new '/incident' node (file) and reads it for status ONGOING
 -- When new node status is ONGOING
 -- a sub-status of OPENED is assigned for the first interval (i.e., ONGOING:OPENED)
 -- interval marker is set to [0]
 -- file is copied to './incidents/active' directory
 -- a START timestamp (POSIX), calculated from the arbitrary start time entered by agent, is recorded
 -- [ACTION] API notification is sent to listening roomId(s)
 -- When a node status has been ONGOING for [28]1 minutes 	
 	-- Status ONGOING is verified against node file in './incidents/active'
	   OPENED sub-status is removed.  
 	-- Interval marker is updated to [1]
 	-- [ACTION] API notification is sent to listening roomId(s)
	 	<strong>NOTICE</strong> New Status Message Posted: 
		<a href="_link_">_title_</a>
		<strong>Status:</strong> OPENED" }' \
		https://api.hipchat.com/v2/room/437235/notification? \
		auth_token=$HUBOT_TEST_TOKEN 

fustatus-event.py  [completion: 00%]
 -- event handler and API interactions

	
Outline of what needs to happen for Maintenance Notifications 

-> fustatus-scrape.py (maintenance_method)
	Scrapes status page every 5 minutes
   	Nodes on page are counted and stored in a JSON dictionary
-> humaintenance.py 




