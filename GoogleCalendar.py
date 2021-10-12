import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime, timedelta
import time
# If modifying these scopes, delete the file token.pickle.

class Calendar():
    def __init__(self, CREDENTIALS_FILE):
        self.CREDENTIALS_FILE = CREDENTIALS_FILE
    def get_calendar_service(self):
       SCOPES = ['https://www.googleapis.com/auth/calendar']

       creds = None
       # The file token.pickle stores the user's access and refresh tokens, and is
       # created automatically when the authorization flow completes for the first
       # time.
       if os.path.exists('token.pickle'):
           with open('token.pickle', 'rb') as token:
               creds = pickle.load(token)
       # If there are no (valid) credentials available, let the user log in.
       if not creds or not creds.valid:
           if creds and creds.expired and creds.refresh_token:
               creds.refresh(Request())
           else:
               flow = InstalledAppFlow.from_client_secrets_file(
                   self.CREDENTIALS_FILE, SCOPES)
               creds = flow.run_local_server(port=0)

           # Save the credentials for the next run
           with open('token.pickle', 'wb') as token:
               pickle.dump(creds, token)

       service = build('calendar', 'v3', credentials=creds)
       return service




    def CreateEvent(self,Subject = "",desc = "",start = datetime(1900,1,1),end = datetime(1900,1,1),organizer = "",location = ''):
       # creates one hour event tomorrow 10 AM IST
       service = self.get_calendar_service()
       print(Subject)
       print(desc)
       print(start)
       print(end)
       print(organizer)
       print(location)
       

       event_result = service.events().insert(calendarId='primary',
           body={
               "summary": Subject,
               "description": desc,
               "location:":location,
               "start": {"dateTime": start, "timeZone": 'Asia/Ho_Chi_Minh'},
               "organizer": {"displayName": organizer},
               "end": {"dateTime": end, "timeZone": 'Asia/Ho_Chi_Minh'},"reminders": {"useDefault": False,"overrides": [ { "method": "popup","minutes": 5},{ "method": "popup","minutes": 30} ]},

  }
       ).execute()
       time.sleep(0.5)
       return event_result['id'],event_result['summary'],event_result['start']['dateTime'],event_result['end']['dateTime']
    def DeleteEvent(self,ID):
       # Delete the event
       service = self.get_calendar_service()
       try:
           service.events().delete(
               calendarId='primary',
               eventId=ID,
           ).execute()
       except googleapiclient.errors.HttpError:
           print("Failed to delete event")
       
       print("Event deleted")
       time.sleep(0.5)

