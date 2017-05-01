#!/usr/bin/env python

# used to get the US Census key
import os
# import libraries for API requests
try:
    # For Python 3.0 and later
    from urllib.request import urlopen, Request, URLError
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import Request, urlopen, URLError
# VERY CONVENIENT LIBRARY FOR TRANSLATING US STATE METADATA!
import us
# import libraries for printing prettily
import pprint
# for converting data
import pandas as pd
import numpy as np
# for regex expressions
import re
##################################################################
# Implementation:
#################

# REMEMBER TO ADD YOUR CENSUS KEY TO THE SYSTEM VARIABLES!!!!!
key = os.environ['USCENSUS_KEY']; 

# make a request from the US Census:
def census_request(url):
    request = Request(url+'&key='+key);
    try:
        response = urlopen(request);
        data     = response.read();
        df       = pd.read_json(data); 
        return df;
    except (URLError, e):
        print('Got an error code:', e);
        raise;


# format the education dataset:
def education():
    # get the (Bachelor's Degree or higher) Education Rate from 2010-2014 
    # for each state, or:
    # EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Percent bachelor's
    # degree or higher
    
    # 2010 and 2011 are in CSV files:
    df = pd.DataFrame();
    for (path, year) in [('Datasets/ACS_10_5YR_S1501/ACS_10_5YR_S1501_with_ann.csv',
                          '2010'),
                         ('Datasets/ACS_11_5YR_S1501/ACS_11_5YR_S1501_with_ann.csv',
                          '2011')]:
        next_year = pd.read_csv(path, header=None, names=["state", year], 
                                usecols=[1, 3], skiprows=2, dtype={'state':str});
        next_year = next_year.set_index('state');
        df = pd.concat([df, next_year], axis=1); 
    
    # 2012-2014 are from the Census API:
    for i in [2012, 2013, 2014]:
        acs_education_URL = 'https://api.census.gov/data/'+str(i)+ \
                            '/acs5/profile?get=DP02_0067PE&for=state:*';
        next_year = census_request(acs_education_URL);
        next_year = next_year.rename(columns = {0:str(i), 1:'state'});
        next_year.drop(0, inplace=True);
        next_year = next_year.set_index('state');
        df = pd.concat([df, next_year], axis=1); 
    df = df.rename_axis('state').rename_axis('time', axis=1);
    df.drop('72', inplace=True); # get rid of state 72
   # df.index = df.index.map(lambda x: 'edu'+x);
    df = df.transpose().stack().to_frame();    
    df = df.rename(columns={0:'edu'});
    return df;


# format the job creation dataset
def job_creation():
    # get the Job Creation Rate from 2010-2014 for each state:
    bds_URL = 'https://api.census.gov/data/bds/firms?get=' + \
              'job_creation_rate_births,sic1&for=state:*&time=from+2010+to+2014';
    df = census_request(bds_URL);
    df = df.rename(columns=df.iloc[0]);
    df.drop(0, inplace=True);
    df.drop('sic1', axis=1, inplace=True);
    df = df.pivot(index='state', columns='time', values='job_creation_rate_births');
    df = df.rename_axis('state').rename_axis('time', axis=1);
   # df.index = df.index.map(lambda x: 'job'+x);
    df = df.transpose().stack().to_frame();    
    df = df.rename(columns={0:'job'});
    return df;

# format the university funds dataset
def university_funds():
    df = pd.read_excel('Datasets/University_States.xlsx', 
                            sheetname='HERD2015_DST_62', header=3, skip_footer=8,
                            parse_cols='A,F:J');
    US_df = df.index[0]; # get the total for United States

    df.drop(0, inplace=True); # remove the United States
  
    # Convert State names to fips codes:
    name2code = us.states.mapping('name', 'fips');
    df['State'] = df['State'].apply(lambda x: name2code[x]);
    df = df.set_index('State');
    df = df.rename_axis('state').rename_axis('time', axis=1);
   # df.index = df.index.map(lambda x: 'uni'+x);
    df = df.transpose().stack().to_frame();    
    df = df.rename(columns={0:'uni'});
    df.uni = df.uni.astype(float);
    return df;

# format the minimum wage dataset
def min_wage():
    df = pd.read_table('Datasets/min_wage.txt', sep='\t', header=2,
                       usecols=[0, 2, 3, 4, 5, 6, 7]); 

    # Convert State names to fips codes:
    name2code = us.states.mapping('name', 'fips');
    df['States'] = df['States'].apply(lambda x: name2code[x]);
    df = df.set_index('States');
    df = df.rename_axis('state').rename_axis('time', axis=1);
    # Change values from currency to floats:
    df = df[df.columns[1:]].replace('[\$,]', '', regex=True).astype(float);
    df.drop('72', inplace=True); # remove Puerto Rico
  

   # df.index = df.index.map(lambda x: 'minw'+x);
    df = df.transpose().stack().to_frame();    
    df = df.rename(columns={0:'minw'});
    return df;    

# format the electricity cost dataset
def electricity_costs():
    df = pd.read_csv('Datasets/Average_retail_price_of_electricity.csv',
                          header=None, names=["state", "2010","2011","2012",
                                              "2013","2014"],
                          index_col = 0, usecols=[0, 3, 4, 5, 6, 7],
                          skiprows=6);
    # Change values from :
    df.index = df.index.map(lambda x: re.sub('\s:\s(commercial|industrial)','', x));
    US_df = df.index[0:1]; # get the total for United States
    # Convert State names to fips codes:
    name2code = us.states.mapping('name', 'fips');
    df = df.ix[2:] # remove the United States
    df.index = df.index.map(lambda x: name2code[x]);
    df = df.rename_axis('state').rename_axis('time', axis=1);

    df.sort_index(axis=0, inplace=True);
    df_c = df.iloc[::2, :];
    df_i = df.iloc[1::2, :];

    # rename states:
   # df_c.index = df_c.index.map(lambda x: 'ec'+x);
   # df_i.index = df_i.index.map(lambda x: 'ei'+x);
    df_c = df_c.transpose().stack().to_frame();    
    df_c = df_c.rename(columns={0:'ecom'});
    df_i = df_i.transpose().stack().to_frame();    
    df_i = df_i.rename(columns={0:'eind'});
    return (df_c, df_i);

# format the unemployment dataset
def unemployment():
    df = pd.read_excel('Datasets/annual_unemployment.xlsx', 
                            header=None, skiprows=np.arange(0,7,1),
                            skip_footer=2, names=["state", "2014","2013","2012",
                                                    "2011","2010"], 
                            parse_cols='A,T,Q,N,K,H');

    US_df = df.index[0]; # get the total for United States
    df.drop(0, inplace=True); # remove the United States
  
    # Convert State names to fips codes:
    name2code = us.states.mapping('name', 'fips');
    #print(name2code);
    df['state'] = df['state'].apply(lambda x: name2code[x]);
    df = df.set_index('state');
    df = df.rename_axis('state').rename_axis('time', axis=1);
    #df.index = df.index.map(lambda x: 'unemp'+x);
    df = df.transpose().stack().to_frame();    
    df = df.rename(columns={0:'unemp'});
    return df;

# Build datasets:
def main():
    Jobs    = job_creation();
    Edu     = education();
    Uni     = university_funds();
    Uni     = Uni.set_index(Jobs.index);
    MinWage = min_wage();
    GDP     = pd.read_excel('Datasets/gdplev.xls', header=None, 
                            skiprows=np.arange(0,89,1),
                            skip_footer=195, names=['time', 'GDP'], 
                            parse_cols='A:B');
    GDP     = GDP.set_index('time');
    GDP     = GDP.loc[np.repeat(GDP.index.values, 51)];
    GDP     = GDP.set_index(Jobs.index);
    (Elec_Commercial, Elec_Industrial) = electricity_costs();
    Unemp   = unemployment();

    # combine all datasets:
    Datasets = pd.concat([Jobs, Edu, Uni, MinWage, GDP, Elec_Industrial, 
                        Elec_Commercial, Unemp], axis=1);
    Datasets.reset_index(level=0, inplace=True);
    Datasets.reset_index(level=0, inplace=True);
    
    Datasets.to_csv('dataset.csv');
   # print(Exogens[['job', 'edu']]);
    # with pd.option_context('display.max_rows', None, 'display.max_columns', 10):
    #     print(Unemp.info());
    #     print(Jobs.info());
    #     print(Edu.info());
    #     print(Uni.info());
    #     print(MinWage.info());
    #     print(GDP.info());
    #     print(Elec_Industrial.info());
    #     print(Elec_Commercial.info());
    #     print(Datasets.info());
    #     print(Datasets.columns.values);
        
if __name__ == "__main__":
    main();