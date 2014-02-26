**CONDITIONS TESTING**

**ACTIVE TEST CASES**

   
ONGOING
Product Set
START SET
 


[x] Result: **OK**
```bash
[ user # testserver-integration ~/fustatus ]./fustatus-item3 2463
2463.json written successfully
[ user # testserver-integration ~/fustatus ]cat incidents/2463.json
{'status': 'ONGOING', 'sub_status': None, 'time_start': '1393380600', 'interval': None, 'nodeId': '2463', 'time_end': None, 'link': 'https://community.hpcloud.com/status/incident/2463', 'desc': ['We are Currently Testing The Incident Notification System.']}
[ user # testserver-integration ~/fustatus ]
```
   

 
ONGOING
Product NOT Set
START SET
 


[x] Result: **OK**
```bash
[ user # testserver-integration ~/fustatus ]./fustatus-item3 2463
2463.json written successfully
[ user # testserver-integration ~/fustatus ]cat incidents/2463.json
{'status': 'ONGOING', 'sub_status': None, 'time_start': '1393380600', 'interval': None, 'nodeId': '2463', 'time_end': None, 'link': 'https://community.hpcloud.com/status/incident/2463', 'desc': ['We are Currently Testing The Incident Notification System.']}
[ user # testserver-integration ~/fustatus ]
```
   

 
MONITORING
Product Set
START SET
 


[x] Result: **OK**
```bash
[ user # testserver-integration ~/fustatus ]./fustatus-item3 2463
2463.json written successfully
[ user # testserver-integration ~/fustatus ]cat incidents/2463.json
{'status': 'MONITORING', 'sub_status': None, 'time_start': '1393380600', 'interval': None, 'nodeId': '2463', 'time_end': None, 'link': 'https://community.hpcloud.com/status/incident/2463', 'desc': ['We are Currently Testing The Incident Notification System.']}
[ user # testserver-integration ~/fustatus ]
```
   

 
MONITORING
Product NOT Set
START SET
 


[x] Result: **OK**
```bash
[ user # testserver-integration ~/fustatus ]./fustatus-item3 2463
2463.json written successfully
[ user # testserver-integration ~/fustatus ]cat incidents/2463.json
{'status': 'MONITORING', 'sub_status': None, 'time_start': '1393380600', 'interval': None, 'nodeId': '2463', 'time_end': None, 'link': 'https://community.hpcloud.com/status/incident/2463', 'desc': ['We are Currently Testing The Incident Notification System.']}
[ user # testserver-integration ~/fustatus ]

```
   


**RESOLVED  TEST CASES**

 
RESOLVED
Product Set
START SET
END SET
 


[x] Result: **OK**
```bash
[ user # testserver-integration ~/fustatus ]./fustatus-item3 2463
2463.json written successfully
[ user # testserver-integration ~/fustatus ]cat incidents/2463.json
{'status': 'RESOLVED', 'sub_status': None, 'time_start': '1393380600', 'interval': None, 'nodeId': '2463', 'time_end': '1393425000', 'link': 'https://community.hpcloud.com/status/incident/2463', 'desc': ['We are Currently Testing The Incident Notification System.']}
[ user # testserver-integration ~/fustatus ]

```
   
 
RESOLVED
Product NOT Set
START SET
END SET
 
[x] Result: **FAIL**
```bash
[ user # testserver-integration ~/fustatus ]./fustatus-item3 2463
Traceback (most recent call last):
  File "./fustatus-item3", line 112, in <module>
    item['time_end'] = timestamp(tree.xpath(match_end3)[0], "%A, %B %d, %Y %I:%M %p %Z", "%s")
IndexError: list index out of range
[ user # testserver-integration ~/fustatus ]
```
   
 
RESOLVED
Product Set
START SET
END NOT SET
 


[x] Result: **OK**
```bash 
[ user # testserver-integration ~/fustatus ]./fustatus-item3 2463
2463.json written successfully
[ user # testserver-integration ~/fustatus ]cat incidents/2463.json
{'status': 'RESOLVED', 'sub_status': None, 'time_start': '1393380600', 'interval': None, 'nodeId': '2463', 'time_end': '1393380600', 'link': 'https://community.hpcloud.com/status/incident/2463', 'desc': ['We are Currently Testing The Incident Notification System.']}
[ user # testserver-integration ~/fustatus ]
```
   
 
RESOLVED
Product NOT Set
START SET
END NOT SET
 


[x] Result: **OK**
```bash
[ user # testserver-integration ~/fustatus ]./fustatus-item3 2463
2463.json written successfully
[ user # testserver-integration ~/fustatus ]cat incidents/2463.json
{'status': 'RESOLVED', 'sub_status': None, 'time_start': '1393380600', 'interval': None, 'nodeId': '2463', 'time_end': '1393380600', 'link': 'https://community.hpcloud.com/status/incident/2463', 'desc': ['We are Currently Testing The Incident Notification System.']}
[ user # testserver-integration ~/fustatus ]
```
   



