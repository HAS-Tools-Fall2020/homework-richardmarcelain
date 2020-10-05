# Starter code for week 6 illustrating how to build an AR model 
# and plot it

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import datetime
#note you may need to do pip install for sklearn

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
filename = 'streamflow_week6.txt'
filepath = os.path.join('C:/Users/Richard/Desktop/class/Course_Materials/homework-richardmarcelain/data/', filename)
print(os.getcwd())
print(filepath)


# %%
#Read the data into a pandas dataframe
data=pd.read_table(filepath, sep = '\t', skiprows=30,
        names=['agency_cd', 'site_no', 'datetime', 'flow', 'code'],
        parse_dates=['datetime']
        )

# Expand the dates to year month day
data['year'] = pd.DatetimeIndex(data['datetime']).year
data['month'] = pd.DatetimeIndex(data['datetime']).month
data['day'] = pd.DatetimeIndex(data['datetime']).dayofweek
data['dayofweek'] = pd.DatetimeIndex(data['datetime']).dayofweek

# Aggregate flow values to weekly 
flow_weekly = data.resample("W", on='datetime').mean()

# %%
# Building an autoregressive model 
# You can learn more about the approach I'm following by walking 
# Through this tutorial
# https://realpython.com/linear-regression-in-python/

# Step 1: setup the arrays you will build your model on
# This is an autoregressive model so we will be building
# it based on the lagged timeseries

flow_weekly['flow_tm1'] = flow_weekly['flow'].shift(1)
flow_weekly['flow_tm2'] = flow_weekly['flow'].shift(2)

# Step 2 - pick what portion of the time series you want to use as training data
# here I'm grabbing the first 800 weeks 
# Note1 - dropping the first two weeks since they wont have lagged data
# to go with them  
train = flow_weekly[100:1100][['flow', 'flow_tm1', 'flow_tm2']]
test = flow_weekly[1100:][['flow', 'flow_tm1', 'flow_tm2']]

# Step 3: Fit a linear regression model using sklearn 
model = LinearRegression()
x=train['flow_tm1'].values.reshape(-1,1) #See the tutorial to understand the reshape step here 
y=train['flow'].values
model.fit(x,y)

#Look at the results
# r^2 values
r_sq = model.score(x, y)
print('coefficient of determination:', np.round(r_sq,2))

#print the intercept and the slope 
print('intercept:', np.round(model.intercept_, 2))
print('slope:', np.round(model.coef_, 2))

# Step 4 Make a prediction with your model 
# Predict the model response for a  given flow value
q_pred_train = model.predict(train['flow_tm1'].values.reshape(-1,1))
q_pred_test = model.predict(test['flow_tm1'].values.reshape(-1,1))

#altrenatievely you can calcualte this yourself like this: 
q_pred = model.intercept_ + model.coef_ * train['flow_tm1']

# you could also predict the q for just a single value like this
last_week_flow = 500
prediction = model.intercept_ + model.coef_ * last_week_flow


# %%
# Another example but this time using two time lags as inputs to the model 
model2 = LinearRegression()
x2=train[['flow_tm1','flow_tm2']]
model2.fit(x2,y)
r_sq = model2.score(x2, y)
print('coefficient of determination:', np.round(r_sq,2))
print('intercept:', np.round(model2.intercept_, 2))
print('slope:', np.round(model2.coef_, 2))

# generate preditions with the funciton
q_pred2_train = model2.predict(train[['flow_tm1', 'flow_tm2']])

# or by hand
q_pred2 = model2.intercept_   \
         + model2.coef_[0]* train['flow_tm1'] \
         +  model2.coef_[1]* train['flow_tm2'] 

# %% 
# Here are some examples of things you might want to plot to get you started:

# 1. Timeseries of observed flow values
# Note that date is the index for the dataframe so it will 
# automatically treat this as our x axis unless we tell it otherwise
fig, ax = plt.subplots()
ax.plot(flow_weekly['flow'], '-g', label='observed', alpha=.5)
ax.plot(train['flow'], 'b:', label='training')
ax.set(title="Flow Time Series with Training Period", xlabel="Date", 
        ylabel="Weekly Avg Flow [cfs]",
        yscale='log')
ax.legend()
# an example of saving your figure to a file
fig.set_size_inches(6,4)
fig.savefig("Plot_1.png")

#2. Time series of flow values with the x axis range limited
fig, ax = plt.subplots()
ax.plot(flow_weekly['flow'], '-g',label='full', alpha=.5)
ax.plot(train['flow'], 'b:', label='training')
ax.set(title="Observed Flow", xlabel="Date", ylabel="Weekly Avg Flow [cfs]",
        yscale='log', xlim=[datetime.date(2000, 1, 26), datetime.date(2014, 2, 1)])
ax.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1)


# 3. Line  plot comparison of predicted and observed flows
fig, ax = plt.subplots()
ax.plot(train['flow'], color='green', linewidth=2, label='observed', alpha=.5)
ax.plot(train.index, q_pred_train, color='red', linestyle='--', 
        label='simulated')
ax.set(title="Flow Time Series with Simulated Results", xlabel="Date", ylabel="Weekly Avg Flow [cfs]",
        yscale='log')
ax.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1)
fig.set_size_inches(6,4)
fig.savefig("Plot_2.png")

# 4. Scatter plot of t vs t-1 flow with log log axes
fig, ax = plt.subplots()
ax.scatter(train['flow_tm1'], train['flow'], marker='v',
              color='green', label='obs', alpha=.5)
ax.set(title="Autoregression (log) of Flow vs Lagged Flow (1-week)",xlabel='flow t-1', ylabel='flow t', yscale='log', xscale='log')
ax.plot(np.sort(train['flow_tm1']), np.sort(q_pred_train), label='AR model',color='red')
ax.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1)
fig.set_size_inches(6,4)
fig.savefig("Plot_3.png")

# 5. Scatter plot of t vs t-1 flow with normal axes
fig, ax = plt.subplots()
ax.scatter(train['flow_tm1'], train['flow'], marker='v',
              color='green', label='observations', alpha=.5)
ax.set(title="Autoregression (linear) of Flow vs Lagged Flow (1-week)",xlabel='flow t-1', ylabel='flow t')
ax.plot(np.sort(train['flow_tm1']), np.sort(q_pred_train), label='AR model', color='red')
ax.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1)
fig.set_size_inches(6,4)
fig.savefig("Plot_4.png")

plt.show()


# %% Forecasting
z = flow_weekly[(flow_weekly['year']==2019) & (flow_weekly['month']>=8)]
print(z['flow_tm2'])
# %%  Actual Results
# week 1, 9/5:   57.1
# week 2, 9/12:  42.26
# week 3, 9/19:  56.2
# week 4, 9/26:  58.43
# week 5, 10/5:
# %%
