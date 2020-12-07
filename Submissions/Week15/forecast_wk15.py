# %%
# Week 15 - Richard Marcelain
# Forecasting Code

# %%
import pandas as pd
import numpy as np
import datetime
import os
import json 
import urllib.request as req
import urllib
from sklearn.linear_model import LinearRegression


# %%
# Location and time variables
site = '09506000'
start = '1989-01-01'
end = '2020-12-5'

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
flow_data = data[['year', 'month','day', 'flow']].to_numpy()

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
last_flow = flow_weekly[['flow']].tail(2).round(1)
lastweek_flow = last_flow.values[0]


# %%
# Run AR-based function to produce remaining forecast weeks
flow_prediction = predictions(lastweek_flow,model)

# Print forecast values
print('Regression based weekly forecasts:')
print('1-Week: ',flow_prediction[1].round(1), "cfs")
print('2-Week: ',flow_prediction[2].round(1), "cfs")


# %%
print('Quantile based season forecasts:')
aug31 = flow_data[(flow_data[:,2] == 31) & (flow_data[:,1]==8), ]
print(np.quantile(aug31[:,3], q=[0]))

sep7 = flow_data[(flow_data[:,2] == 7) & (flow_data[:,1]==9), ]
print(np.quantile(sep7[:,3], q=[0]))

sep14 = flow_data[(flow_data[:,2] == 14) & (flow_data[:,1]==9), ]
print(np.quantile(sep14[:,3], q=[0]))

sep21 = flow_data[(flow_data[:,2] == 21) & (flow_data[:,1]==9), ]
print(np.quantile(sep21[:,3], q=[0]))

sep28 = flow_data[(flow_data[:,2] == 28) & (flow_data[:,1]==9), ]
print(np.quantile(sep28[:,3], q=[0]))

oct5 = flow_data[(flow_data[:,2] == 5) & (flow_data[:,1]==10), ]
print(np.quantile(oct5[:,3], q=[0]))

oct12 = flow_data[(flow_data[:,2] == 12) & (flow_data[:,1]==10), ]
print(np.quantile(oct12[:,3], q=[0]))

oct19 = flow_data[(flow_data[:,2] == 19) & (flow_data[:,1]==10), ]
print(np.quantile(oct19[:,3], q=[0]))

oct26 = flow_data[(flow_data[:,2] == 26) & (flow_data[:,1]==10), ]
print(np.quantile(oct26[:,3], q=[0]))

nov2 = flow_data[(flow_data[:,2] == 1) & (flow_data[:,1]==11), ]
print(np.quantile(nov2[:,3], q=[0]))

nov9 = flow_data[(flow_data[:,2] == 9) & (flow_data[:,1]==11), ]
print(np.quantile(nov9[:,3], q=[0]))

nov16 = flow_data[(flow_data[:,2] == 16) & (flow_data[:,1]==11), ]
print(np.quantile(nov16[:,3], q=[0]))

nov23 = flow_data[(flow_data[:,2] == 23) & (flow_data[:,1]==11), ]
print(np.quantile(nov23[:,3], q=[0]))

nov30 = flow_data[(flow_data[:,2] == 30) & (flow_data[:,1]==11), ]
print(np.quantile(nov30[:,3], q=[0]))

dec17 = flow_data[(flow_data[:,2] == 17) & (flow_data[:,1]==12), ]
print(np.quantile(dec17[:,3], q=[0]))
# %%

# %%
