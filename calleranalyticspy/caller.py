from . import ca_api_call
from . import CaApiClass

def read(phoneNumber, requestProfile = None):
   """read a caller, returning a Caller instance"""
   data = { "phoneNumber": phoneNumber }
   if requestProfile:
      data["requestProfile"] = requestProfile
   return Caller(ca_api_call('Caller', 'Read', data)) 

class Caller(CaApiClass):
   def __init__(self, *args, **kwargs):
      CaApiClass.__init__(self, 'Caller', *args, **kwargs)
   
   def get_data(self, key):
      """Get a caller data item by key
      """
      return self._data[key]
   
   def iterdata(self):
      """Iterate over key/value pairs of caller data items
      """
      return self._data.iteritems()

class CallerUpdate(CaApiClass):
   def __init__(self, phoneNumber):
      CaApiClass.__init__(self, 'Caller', phoneNumber=phoneNumber)
   
   def add_data(self, key, value):
      if self.caller:
         self.caller[key] = value
      else:
         self.caller = { key : value }
   
   def iterdata(self):
      if self.caller:
         return self.caller.iteritems()
      return []
