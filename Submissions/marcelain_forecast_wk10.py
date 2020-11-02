# %%
# Week 10 - Richard Marcelain
# Forecasting Code

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os
import json 
import urllib.request as req
import urllib
from sklearn.linear_model import LinearRegression


# %%
# Mesonet Example - 
#Here are some helpful links for getting started
#https: // developers.synopticdata.com/about/station-variables/
#https: // developers.synopticdata.com/mesonet/explorer/

# First Create the URL for the rest API
# Insert your token here
mytoken = 'bdea3b3d824a45109755be235e6c4c44'

# This is the base url that will be the start our final url
base_url = "http://api.mesowest.net/v2/stations/timeseries"

# Specific arguments for the data that we want
# Location retrieved from: https://mesowest.utah.edu/cgi-bin/droman/mesomap.cgi?state=AZ&rawsflag=3
args = {
    'start': '199701010000',
    'end': '202010240000',
    'obtimezone': 'UTC',
    'vars': 'air_temp',
    'stids': 'KSEZ',
    'units': 'temp|F,precip|mm',
    'token': mytoken} 

# Takes your arguments and paste them together
# into a string for the api
# (Note you could also do this by hand, but this is better)
apiString = urllib.parse.urlencode(args)
print(apiString)

# add the API string to the base_url
fullUrl = base_url + '?' + apiString
print(fullUrl)

# Now we are ready to request the data
# this just gives us the API response... not very useful yet
response = req.urlopen(fullUrl)

# What we need to do now is read this data
# The complete format of this 
responseDict = json.loads(response.read())

# This creates a dictionary for you 
# The complete format of this dictonary is descibed here: 
# https://developers.synopticdata.com/mesonet/v2/getting-started/
#Keys shows you the main elements of your dictionary
responseDict.keys()
# You can inspect sub elements by looking up any of the keys in the dictionary
responseDict['UNITS']
#Each key in the dictionary can link to differnt data structures
#For example 'UNITS is another dictionary'
type(responseDict['UNITS'])
responseDict['UNITS'].keys()
responseDict['UNITS']['position']

#where as STATION is a list 
type(responseDict['STATION'])
# If we grab the first element of the list that is a dictionary
type(responseDict['STATION'][0])
# And these are its keys
responseDict['STATION'][0].keys()

# Long story short we can get to the data we want like this: 
dateTime = responseDict['STATION'][0]['OBSERVATIONS']['date_time']
airT = responseDict['STATION'][0]['OBSERVATIONS']['air_temp_set_1']

# Now we can combine this into a pandas dataframe
data = pd.DataFrame({'Temperature': airT}, index=pd.to_datetime(dateTime))

# Now convert this to daily data using resample
temp_daily = data.resample('D').mean()

# Convert to weekly data
temp_weekly = data.resample("W").mean()


# %%
# Retrieve Streamflow data up to last Saturday

# Location and time variables
site = '09506000'
start = '1989-01-01'
end = '2020-10-24'

# URL modified with variables
url = "https://waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb&site_no=" + \
      site + "&referred_module=sw&period=&begin_date=" + start + \
      "&end_date=" + end
data = pd.read_table(url, skiprows=30,
                     names=['agency_cd', 'site_no',
                            'datetime', 'flow', 'code'],
                     parse_dates=['datetime'])

# Expand data to different time dimensions including weekly (most important)
data['year'] = pd.DatetimeIndex(data['datetime']).year
data['month'] = pd.DatetimeIndex(data['datetime']).month
data['day'] = pd.DatetimeIndex(data['datetime']).day
data['dayofweek'] = pd.DatetimeIndex(data['datetime']).dayofweek

# Convert to weekly data
flow_weekly = data.resample("W", on='datetime').mean()


# %% 
# Function to predict weekly flow values using AR model results and previous flow data
def predictions(lastweek_flow,model):
    ''''
    This function will be call on at the end of AR model section of code.

    The previous week's flow along with intercept and coefficient
    values obtained from AR model are used to precict two weeks of streamflow.

    The adjustment takes the average October flow over the last two decades and subtracts
    the 2019 October average flow.  This is to adjust the prediction by the anomalous 
    low flow year values which the datasite is experiencing.

    '''
    adjustment = (np.mean(flow_weekly[(flow_weekly['year']>2000) & (flow_weekly['month']==10)]) - np.mean(flow_weekly[(flow_weekly['year']==2019) & (flow_weekly['month']==10)]))
    prediction = np.zeros(16)
    prediction[0] = (model.intercept_ + model.coef_ * lastweek_flow) - adjustment['flow']
    for i in range (1,16):
        prediction[i] = (model.intercept_ + model.coef_ * prediction[i-1]) - adjustment['flow']
    return prediction


# %%
# Building an autoregressive model (steps 1-4)
# Step 1: Setup the arrays to build model using lagged weekly (1 & 2) times
flow_weekly['flow_tm1'] = flow_weekly['flow'].shift(1)
flow_weekly['flow_tm2'] = flow_weekly['flow'].shift(2)

# Step 2: Robust modern dataset to train the AR model starting and ending at low flow values to influence results
train = flow_weekly[1400:1600][['flow', 'flow_tm1', 'flow_tm2']]
test = flow_weekly[1600:][['flow', 'flow_tm1', 'flow_tm2']]

# Step 3: Fit a linear regression model 
model = LinearRegression()
x=train['flow_tm1'].values.reshape(-1,1)  
y=train['flow'].values
model.fit(x,y)

# Step 4: Add variable for latest weekly flow data which will be used in function
october2020_flow = flow_weekly[['flow']].tail(2).round(1)
lastweek_flow = october2020_flow.values[0]


# %%
# Run AR-based function to produce remaining forecast weeks
flow_prediction = predictions(lastweek_flow,model)

# Print forecast values
print('Regression based forecasts:')
print('Week 10: ',flow_prediction[1].round(1), "cfs")
print('Week 11: ',flow_prediction[2].round(1), "cfs")
print('Week 12: ',flow_prediction[3].round(1), "cfs")
print('Week 13: ',flow_prediction[4].round(1), "cfs")
print('Week 14: ',flow_prediction[5].round(1), "cfs")
print('Week 15: ',flow_prediction[6].round(1), "cfs")
print('Week 16: ',flow_prediction[7].round(1), "cfs")

# %%
