#!/usr/bin/env python

# prints out the US Census key
import os
# import libraries for API requests
from urllib2 import Request, urlopen, URLError

# make a request from the US Census, EXAMPLE:
key = os.environ['USCENSUS_KEY'];
request = Request('http://api.census.gov/data/bds/firms?get=metro,sic1&for=us:*&year2=2012&key='+key);

try:
	response = urlopen(request)
	data = response.read()
	print data
except URLError, e:
    print 'Got an error code:', e
