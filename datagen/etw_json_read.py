import jmespath
import json

with open('final.json','r') as f:
	json_d=json.loads(f.read())
	events=json_d['Microsoft-Windows-EFS']['Events']['1']
	print(events)

	#print(json_str)