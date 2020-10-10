# Week 7 Codes
# Author: Richard Marcelain

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import datetime


# %%
# Function to predict weekly flow values using AR model results and previous flow data
def predictions(lastweek_flow):
    ''''
    This function will be call on at the end of AR model section of code.

    The previous week's flow (from streamflow7.txt) along with intercept and coefficient
    values obtained from AR model are used to precict two weeks of streamflow.

    '''
    prediction = np.zeros(2)
    prediction[0] = model.intercept_ + model.coef_ * lastweek_flow
    prediction[1] = model.intercept_ + model.coef_ * prediction[0]
    return prediction

# %%
# Retrieve stored streamflow data for week 7
filename = 'streamflow_week7.txt'   # Most recent flow data file namme
filepath = os.path.join('../data', filename)  # Path to flow data file
print(os.getcwd())
print(filepath)


# %%
# Read the data into a pandas dataframe
data=pd.read_table(filepath, sep = '\t', skiprows=30,
        names=['agency_cd', 'site_no', 'datetime', 'flow', 'code'],
        parse_dates=['datetime']
        )

# Expand the dates to year month day
data['year'] = pd.DatetimeIndex(data['datetime']).year
data['month'] = pd.DatetimeIndex(data['datetime']).month
data['day'] = pd.DatetimeIndex(data['datetime']).dayofweek
data['dayofweek'] = pd.DatetimeIndex(data['datetime']).dayofweek

# Aggregate daily flow values to weekly flow values
flow_weekly = data.resample("W", on='datetime').mean()

# Find last week's flow value (you'll need for AR model)
october2020_flow = flow_weekly[['flow']].tail(2).round(1)
lastweek_flow = october2020_flow.values[0]
print("Last week's flow: ", lastweek_flow, "cfs")


# %%
# Building an autoregressive model 

# Step 1: setup the arrays you will build your model on
# This is an autoregressive model so we will be building
# it based on the lagged timeseries
flow_weekly['flow_tm1'] = flow_weekly['flow'].shift(1)
flow_weekly['flow_tm2'] = flow_weekly['flow'].shift(2)

# Step 2 - pick what portion of the time series you want to use as training data
# Select a robust section of total dataset to train the AR model
train = flow_weekly[900:1500][['flow', 'flow_tm1', 'flow_tm2']]
test = flow_weekly[1500:][['flow', 'flow_tm1', 'flow_tm2']]

# Step 3: Fit a linear regression model using sklearn 
model = LinearRegression()
x=train['flow_tm1'].values.reshape(-1,1)  
y=train['flow'].values
model.fit(x,y)

# Look at the results (r^2 values)
r_sq = model.score(x, y)
print('AR model statistics:')
print('coefficient of determination:', np.round(r_sq,2))

# Print the intercept and the slope 
print('intercept:', np.round(model.intercept_, 2))
print('slope:', np.round(model.coef_, 2))


# %% 
# Forecasting for weeks 1 and 2
# I use the last year's weekly flows since they are stastically closest to this year's
# flow when lagging the data by two weeks
oct2019 = flow_weekly[(flow_weekly['year']==2019) & (flow_weekly['month']==9)]
flow_forecast = oct2019['flow_tm2'].tail(2).round(1)

print('Forecasts using own method:')
print('Week 1 forecast: ',flow_forecast[0].round(1), "cfs")
print('Week 2 forecast: ',flow_forecast[1].round(1), "cfs")


# %%
# Prediction from AR model 
# Use function to predict weeks 1 and 2
flow_prediction = predictions(lastweek_flow)

print('Preditions using AR model:')
print('Week 1 forecast (AR): ',flow_prediction[0].round(1), "cfs")
print('Week 2 forecast (AR): ',flow_prediction[1].round(1), "cfs")


# %%
