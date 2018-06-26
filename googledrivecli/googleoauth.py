"""
Create Project in Google, URL : https://console.developers.google.com/flows/enableapi?apiid=drive
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from sys import exit

from googledrivecli.driverclient import secretfilename, credentialsfilename


def GetAPIResourceObj():
	# Setup the Drive v3 API
	SCOPES = 'https://www.googleapis.com/auth/drive'
	store = file.Storage(credentialsfilename)
	creds = store.get()
	if not creds or creds.invalid:
	    flow = client.flow_from_clientsecrets(secretfilename, SCOPES)
	    creds = tools.run_flow(flow, store)
	service = build('drive', 'v3', http=creds.authorize(Http()))
	return service
