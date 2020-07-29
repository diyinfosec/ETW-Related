#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import json
import xmltodict
import glob
import os

def get_event_info():
	dir_name="Provider_Event_Meta\\*.txt"
	file_list=(glob.glob(dir_name))
	out_d={}

	for file_name in file_list:
		#- 
		with open(file_name,encoding='utf-8') as xml_file:
		    xml_dict = xmltodict.parse(xml_file.read())

		data_dict=json.loads(json.dumps(xml_dict))


		#print(type(data_dict))
		#print(data_dict)
		#{'Providers': {'Provider': {'Name': 'Application-Addon-Event-Provider', 'Metadata': {'Guid': '{A83FA99F-C356-4DED-9FD6-5A5EB8546D68}'

		try:
			provider_name=data_dict['Providers']['Provider']['Name']
			provider_guid=data_dict['Providers']['Provider']['Metadata']['Guid']
			event_list=data_dict['Providers']['Provider']['EventMetadata']['Event']
		except (TypeError, KeyError):
			event_list=None

		#-Setting the output variables:

		out_d[provider_name]={}
		out_d[provider_name]['Events']={}

		
		if event_list is None:
			continue

		if type(event_list) is dict:
			event_list=[event_list]

		for key in event_list: 
			try:
				event_message=key['Message']
			except KeyError:
				event_message=''

			out_d[provider_name]['Events'][key['Id']]=event_message

			
	return(out_d)



def get_provider_info():
	dir_name="Provider_Meta\\*.txt"
	file_list=(glob.glob(dir_name))
	out_d={}

	#print(file_list)

	for file_name in file_list:

		#- 
		with open(file_name,encoding='utf-8') as xml_file:
		    xml_dict = xmltodict.parse(xml_file.read())

		data_dict=json.loads(json.dumps(xml_dict))


		provider_name=file_name.split('\\')[-1].split('_')[0]

		#- Initializing output variables. 
		out_d[provider_name]={}
		out_d[provider_name]['MessageDlls']=[]
		out_d[provider_name]['Guid']=''

		if data_dict['Providers'] is None:	
			continue

		try:
			provider_message_dll=data_dict['Providers']['Provider']['Metadata']['MessageFilePath'].split(';')	
		except (TypeError, KeyError,AttributeError) as e:
			pass

		try:
			provider_guid=data_dict['Providers']['Provider']['Metadata']['Guid']
		except (TypeError, KeyError,AttributeError) as e:
			pass

		out_d[provider_name]['MessageDlls']=provider_message_dll
		out_d[provider_name]['Guid']=provider_guid
	return(out_d)


provider_events=get_event_info()
#print(provider_events)

provider_metas=get_provider_info()
#print(provider_metas)

dd={}
for d in (provider_metas, provider_events):
	for main_key, value_dict in d.items():
		if main_key not in dd:
			dd[main_key]={}

		#print(value_dict)
		for sub_key,value in value_dict.items():
			dd[main_key][sub_key]=value


#df=pd.DataFrame.from_dict(dd, orient='index')
#df = pd.DataFrame.from_dict(pd.json_normalize(json.loads(json.dumps(dd))))
with open('final.json','w') as f:
	f.write(json.dumps(dd))