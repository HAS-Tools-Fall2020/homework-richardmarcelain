# Starter code for Homework 4

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
filename = 'streamflow_week4.txt'
filepath = os.path.join('C:/Users/Richard/Desktop/class/Course_Materials/homework-richardmarcelain/data/', filename)
print(os.getcwd())
print(filepath)

#Read the data into a pandas dataframe
data=pd.read_table(filepath, sep = '\t', skiprows=30,
        names=['agency_cd', 'site_no', 'datetime', 'flow', 'code']
        )

# Expand the dates to year month day
data[["year", "month", "day"]] =data["datetime"].str.split("-", expand=True)
data['year'] = data['year'].astype(int)
data['month'] = data['month'].astype(int)
data['day'] = data['day'].astype(int)

# Make a numpy array of this data
flow_data = data[['year', 'month','day', 'flow']].to_numpy()

# Getting rid of the pandas dataframe since we wont be using it this week
del(data)

# %%  Prediction

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
