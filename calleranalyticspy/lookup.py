from . import ca_api_call
from . import CaApiClass

def lookup(phoneNumber, requestProfile = None):
   """Lookup a caller, returning a Lookup instance"""
   data = { "phoneNumber": phoneNumber }
   if requestProfile:
      data["requestProfile"] = requestProfile
   return Lookup(ca_api_call('Lookup', 'Read', data)) 

class Lookup(CaApiClass):
   def __init__(self, *args, **kwargs):
      CaApiClass.__init__(self, 'Lookup', *args, **kwargs)
   
   def get_data(self):
      return self._data
   
   def iterdata(self):
      return self._data.iteritems()
