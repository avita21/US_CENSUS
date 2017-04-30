#!/usr/bin/env python

# used to get the US Census key
import os
# import libraries for API requests
from urllib2 import Request, urlopen, URLError

# REMEMBER TO ADD YOUR CENSUS KEY TO THE SYSTEM VARIABLES
key = os.environ['USCENSUS_KEY']; 

# make a request from the US Census:
def census_request(url):
	request = Request(url+key);
	try:
		response = urlopen(request);
		data = response.read();
		print data
		return data;
	except URLError, e:
	    print 'Got an error code:', e

def main():
	# get the Job Creation Rate from 2010-2014 for each state:
	bds_URL = 'https://api.census.gov/data/bds/firms?get=job_creation_rate_births,sic1&for=state:*&time=from+2010+to+2014&key=';
	#bds_jobcreation = census_request(bds_URL);

	# get the Education Rate from 2010-2014 for each state:
	acs_education_URL = 'https://api.census.gov/data/2010/acs5?get=B23006_022E&for=state:*&key=';
	acs_education = census_request(acs_education_URL);
if __name__ == "__main__":
    main();
