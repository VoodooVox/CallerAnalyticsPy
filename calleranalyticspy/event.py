from . import ca_api_call
from . import CaApiClass

def read_events(dataBucket, eventType, start, end, pageSize=None, lastEvent=None):
   """Find events for current user"""
   data = {
      "dataBucket" : dataBucket,
      "eventType" : eventType,
      "period" : {
            "start" : start,
            "end" : end
      }
   }
   
   if pageSize:
      data["pageSize"] = pageSize
   
   if lastEvent:
      data["lastEvent"] = lastEvent
    
   return EventResponse(ca_api_call('Event', 'Read', data))

class EventResponse(object):
   def __init__(self, response):
      if "lastEvent" in response:
         self.lastEvent = response["lastEvent"]
      else:
         self.lastEvent = None
      
      self.events = []
      for event in response["events"]:
         self.events.append(Event(event))
      
class Event(CaApiClass):
   def __init__(self, *args, **kwargs):
      CaApiClass.__init__(self, 'Event', *args, **kwargs)
      
