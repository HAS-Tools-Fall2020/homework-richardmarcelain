# %%
# Week 12 - Richard Marcelain
# 1. NetCDF Code
# 2. Forecasting Code

# %%
import pandas as pd
import matplotlib.pyplot as plt
import xarray as xr
import rioxarray
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import seaborn as sns
import geopandas as gpd
import fiona
import shapely
from netCDF4 import Dataset
import numpy as np
import datetime
import os
import json 
import urllib.request as req
import urllib
from sklearn.linear_model import LinearRegression


# %%
# NetCDF Code
# Net CDF file historical time series
data_path = os.path.join('../data','prate.2020.nc')
# Read in the dataset as an x-array
dataset = xr.open_dataset(data_path)
# look at it
dataset

data_path2 = os.path.join('../data','prate.2019.nc')
# Read in the dataset as an x-array
dataset2 = xr.open_dataset(data_path2)


# %% We can inspect the metadata of the file like this:
metadata = dataset.attrs
metadata

# %%And we can grab out any part of it like this:
metadata['dataset_title']
metadata['history']

# %% we can also look at other  attributes like this
dataset.values
dataset.dims
dataset.coords

# %% Focusing on just the precip values
precip = dataset['prate']
precip

precip2 = dataset2['prate']

# %% Now to grab out data first lets look at spatail coordinates:
dataset['prate']['lat'].values.shape
dataset['prate']['lon'].values.shape

# %% Now looking at the time
dataset["prate"]["time"].values.shape


# %% Grab slide:  Tucson, AZ
tucson = dataset["prate"][:,91,159]
tucson.shape

tucson2 = dataset2["prate"][:,91,159]

# %% use x-array to plot timeseries
tucson.plot.line()


# %% Make a nicer timeseries plot
f, ax = plt.subplots(figsize=(12, 6))
tucson[215:318].plot.line(hue='lat',
                    marker="o",
                    ax=ax,
                    color="black",
                    markerfacecolor="red")                    
ax.set(title="2020 Tucson Precipitation - NARR")

f.set_size_inches(8,4)
f.savefig(f'plot1_hw12.png', bbox_inches = 'tight')

# %% Make a nicer timeseries plot
f, ax = plt.subplots(figsize=(12, 6))
tucson2[215:301].plot.line(hue='lat',
                    marker="o",
                    ax=ax,
                    color="black",
                    markerfacecolor="blue")                    
ax.set(title="2019 Tucson Precipitation - NARR")

f.set_size_inches(8,4)
f.savefig(f'plot2_hw12.png', bbox_inches = 'tight')


# %%
# 2. Forecasting Code
# Retrieve Streamflow data up to last Saturday

# Location and time variables
site = '09506000'
start = '1989-01-01'
#end = '2020-10-24'
end = '2020-11-14'

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
print('Week 12: ',flow_prediction[1].round(1), "cfs")
print('Week 13: ',flow_prediction[2].round(1), "cfs")
print('Week 14: ',flow_prediction[3].round(1), "cfs")
print('Week 15: ',flow_prediction[4].round(1), "cfs")
print('Week 16: ',flow_prediction[5].round(1), "cfs")

# %%
