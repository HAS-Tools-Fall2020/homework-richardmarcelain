# Week 8
# Author: Richard Marcelain

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import datetime


# %% 
# Function to predict weekly flow values using AR model results and previous flow data
# LC - Nice documentation
def predictions(lastweek_flow,model):
    ''''
    This function will be call on at the end of AR model section of code.

    The previous week's flow (from streamflow8.txt) along with intercept and coefficient
    values obtained from AR model are used to precict two weeks of streamflow.

    The adjustment takes the average October flow over the last two decades and subtracts
    the 2019 October average flow.  This is to adjust the prediction by the anomalous 
    low flow year values which the datasite is experiencing.

    '''
    adjustment = (np.mean(flow_weekly[(flow_weekly['year']>2000) & (flow_weekly['month']==10)]) - np.mean(flow_weekly[(flow_weekly['year']==2019) & (flow_weekly['month']==10)]))*1.5
    prediction = np.zeros(2)
    prediction[0] = (model.intercept_ + model.coef_ * lastweek_flow) - adjustment['flow']
    prediction[1] = (model.intercept_ + model.coef_ * prediction[0]) - adjustment['flow']
    return prediction

# %% 
# Retrieve stored streamflow data for week 8
filename = 'streamflow_week8.txt'  
filepath = os.path.join('../../data', filename)  
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
# Building an autoregressive model (steps 1-4)

# Step 1: Setup the arrays to build model using lagged weekly (1 & 2) times
flow_weekly['flow_tm1'] = flow_weekly['flow'].shift(1)
flow_weekly['flow_tm2'] = flow_weekly['flow'].shift(2)

# Step 2: Robust modern dataset to train the AR model starting and ending at low flow values to influence results
# LC- You could set the numbers for these ranges as variables and link them to dates. 
train = flow_weekly[1400:1600][['flow', 'flow_tm1', 'flow_tm2']]
test = flow_weekly[1600:][['flow', 'flow_tm1', 'flow_tm2']]

# Step 3: Fit a linear regression model
# LC - model fitting would  also be a good step to add  into the function. 
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

# Step 4: Predict the model response for a given flow value
q_pred = model.intercept_ + model.coef_ * train['flow_tm1']


# %%
# Line plot comparison of predicted and observed flows
fig, ax = plt.subplots()
ax.plot(train['flow'], color='green', linewidth=2, label='observed', alpha=.5)
ax.plot(train.index, q_pred, color='red', linestyle='--', 
        label='simulated')
ax.set(title="Flow Time Series with Simulated Results", xlabel="Date", ylabel="Weekly Avg Flow [cfs]",
        yscale='log')
ax.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1)
fig.set_size_inches(6,4)
fig.savefig("Plot_1.png")


# %%
# Prediction from AR model using function to predict weeks 1 and 2
flow_prediction = predictions(lastweek_flow,model)

print('Regression based forecasts:')
print('Week 1: ',flow_prediction[0].round(1), "cfs")
print('Week 2: ',flow_prediction[1].round(1), "cfs")


# %% 
# Final forecasts are same as model results

print('Final Forecasts:')
print('Week 1: ',flow_prediction[0].round(1), "cfs")
print('Week 2: ',flow_prediction[1].round(1), "cfs")


# %%