
import json
import urllib
import urllib2

__all__ = ["event", "lookup", "caller"]

CA_API_HOST="http://api.calleranalytics.com/"

_API_KEY = None

def ca_api_init(key):
   """Initialize the Caller Analytics API
   
   key: Your API key
   """
   global _API_KEY
   _API_KEY = key

def ca_api_call(className, methodName, data={}, key=None):
   """Call the Caller Analytics API
   
   Arguments:
      key -- The API key for your application
      className -- The API Class name
      methodName -- The API Method name
      data -- a dictionary of data to pass as JSON to API
   
   Returns response (from "response" key of returned JSON) on ACK, or
   throw CaApiException on NACK.
   """
   
   url = "%s%s.%s.do" % ( CA_API_HOST, className, methodName )
   
   if key == None:
      key = _API_KEY
   
   params = { 'json' : json.dumps(data), 'key' : key }
   
   params_enc = urllib.urlencode( params )
   
   req = urllib2.Request( url, params_enc )
   
   r = urllib2.urlopen( req )
   
   resp = json.load(r)
   
   response = None
   if "response" in resp:
      response = resp["response"]
   
   if "result" in resp and resp["result"] == "ack":
      return response
   
   raise CaApiException(className, methodName, response)

class CaApiException(Exception):
   def __init__(self, className, methodName, response):
      self.className = className
      self.methodName = methodName
      self.response = response
      
      self.errorKey = "UNKNOWN"
      if "errorKey" in response:
         self.errorKey = response["errorKey"]
      
      self.errorMessage = "Unknown Error"
      if "message" in response:
         self.errorMessage = response["message"]
      
      self.userMessage = self.errorMessage
      
      if self.errorKey == "PARAMETER_ERROR":
         details = response["details"]
         if details["errorKey"] == "IN_USE":
            self.userMessage = details["parameter"] + " is already in use"
         elif details["errorKey"] == "NOT_VALID":
            self.userMessage = details["parameter"] + " is not valid"
         else:
            self.userMessage = details["message"] + " [" + details["parameter"] + "]"
      elif self.errorKey == "REQUIRED_PARAMETER_MISSING":
         details = response["details"]
         self.userMessage = details["parameter"] + " is required"
      
      Exception.__init__(self, "Api Error in %s.%s.do: %s [%s]" % ( className, methodName, self.errorMessage, self.errorKey ))

class CaApiClass(object):
   """Base class for API objects. Stores data in self._data and allows
   access to data through fields through tricks with __getattr__ and __setattr__"""
   def __init__(self, className, *args, **kwargs):
      self.className = className
      
      if args and len(args) == 1:
         #print "setting _data to args " + str(args[0])
         self._data = args[0]
      else:
         #print "setting _data to kwargs: " + str(kwargs)
         self._data = kwargs
      
   def __getattr__(self, name):
      if name in self._data:
         #print "getting '%s' = '%s'" % ( name, self._data[name] )
         return self._data[name]
      #print "getting '%s' = null" % ( name )
      return None
   
   def __setattr__(self, name, value):
      if name == "_data" or name == "className":
         object.__setattr__(self, name, value)
      else:
         #print "setting '%s' to '%s'" % ( name, value )
         self._data[name] = value
   
   def create(self, key=None):
      return ca_api_call(self.className, 'Create', self._data, key)
   
   def update(self, key=None):
      return ca_api_call(self.className, 'Update', self._data, key)
