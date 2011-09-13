#!/usr/bin/env python

import sys

import calleranalyticspy as ca
import calleranalyticspy.lookup as calookup

if len(sys.argv) != 3:
	print "usage: %s API_KEY PHONE_NUMBER" % ( sys.argv[0] )
	sys.exit()

apiKey = sys.argv[1]
phoneNumber = sys.argv[2]

ca.ca_api_init(apiKey)

print "==========================="
print " Looking up %s" % ( phoneNumber )
print "==========================="

lookup = calookup.lookup( phoneNumber )

for (k,v) in lookup.iterdata():
	if k == "members":
		print "members : "
		i = 1
		for member in v:
			print "   member %i" % ( i )
			i += 1
			for (mk,mv) in member.iteritems():
				print "      %s : %s" % ( mk, str(mv) )
	else:
		print "%s : %s" % ( k, str(v) )

