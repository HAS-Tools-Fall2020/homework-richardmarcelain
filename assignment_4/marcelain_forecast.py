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

# %%
# DON'T change this part -- this creates the lists you 
# should use for the rest of the assignment
# no need to worry about how this is being done now we will cover
# this in later sections. 

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

# %%
# Starter Code
# Count the number of values with flow > 600 and month ==7
flow_count = np.sum((flow_data[:,3] > 600) & (flow_data[:,1]==7))

# this gives a list of T/F where the criteria are met
(flow_data[:,3] > 600) & (flow_data[:,1]==7)

# this give the flow values where that criteria is met
flow_pick = flow_data[(flow_data[:,3] > 600) & (flow_data[:,1]==7), 3]

# this give the year values where that criteria is met
year_pic = flow_data[(flow_data[:,3] > 600) & (flow_data[:,1]==7), 0]

# this give the all rows  where that criteria is met
all_pic = flow_data[(flow_data[:,3] > 600) & (flow_data[:,1]==7), ]

# Calculate the average flow for these same criteria 
flow_mean = np.mean(flow_data[(flow_data[:,3] > 600) & (flow_data[:,1]==7),3])

print("Flow meets this critera", flow_count, " times")
print('And has an average value of', flow_mean, "when this is true")

# Make a histogram of data
# Use the linspace  funciton to create a set  of evenly spaced bins
mybins = np.linspace(0, 1000, num=15)
# another example using the max flow to set the upper limit for the bins
#mybins = np.linspace(0, np.max(flow_data[:,3]), num=15) 
#Plotting the histogram
plt.hist(flow_data[:,3], bins = mybins)
plt.title('Streamflow')
plt.xlabel('Flow [cfs]')
plt.ylabel('Count')

# Get the quantiles of flow
# Two different approaches ---  you should get the same answer
# just using the flow column
flow_quants1 = np.quantile(flow_data[:,3], q=[0,0.1, 0.5, 0.9])
print('Method one flow quantiles:', flow_quants1)
# Or computing on a colum by column basis 
flow_quants2 = np.quantile(flow_data, q=[0,0.1, 0.5, 0.9], axis=0)
# and then just printing out the values for the flow column
print('Method two flow quantiles:', flow_quants2[:,3])

# %% Q2 - Find shape of array 
print(flow_data.shape)
print(4*11578)

sep21 = flow_data[(flow_data[:,2] == 20) & (flow_data[:,1]==9), ]
print(np.quantile(sep21[:,3], q=[0]))

# %% Q1 - Histograms with quantitative analysis

# Average flow on sep21
sep21 = flow_data[(flow_data[:,2] == 20) & (flow_data[:,1]==9), ]

# Plotting the histogram
mybins = np.linspace(0, 650, num=15)
plt.hist(sep21[:,3], bins = mybins)
plt.title('Streamflow on Sep 20 (1989 - 2020)')
plt.xlabel('Flow [cfs]')
plt.ylabel('Count')

flow_quants1 = np.quantile(sep21[:,3], q=[0,0.1, 0.5, 0.9])
print('Streamflow quantiles:', flow_quants1)
# %% Average flow on sep21 without anomalous year
sep21new = flow_data[(flow_data[:,2] == 21) & (flow_data[:,1]==9) & (flow_data[:,0]!=2004), ]

# Plotting the histogram
mybins = np.linspace(0, 250, num=15)
plt.hist(sep21new[:,3], bins = mybins)
plt.title('Streamflow on Sep 21 (1989 - 2003, 2005 - 2020)')
plt.xlabel('Flow [cfs]')
plt.ylabel('Count')

flow_quants1 = np.quantile(sep21new[:,3], q=[0,0.1, 0.5, 0.9])
print('Streamflow quantiles:', flow_quants1)

# %%# Q3
p = 53.9
flow_h = np.sum((flow_data[:,3] > 53.9) & (flow_data[:,1]==9) & (flow_data[:,0]==2020))
flow_l = np.sum((flow_data[:,3] <= 53.9) & (flow_data[:,1]==9) & (flow_data[:,0]==2020))

print("9/2020 daily streamflows compared to weekly prediction of 53.9 \n")
print("Days above 56: ", (flow_h))
print("Days below 56: ", (flow_l))
print ("Percentage of days above 56: ",(flow_h) / ((flow_h) + (flow_l)) *100, "%")
# %%
# %%# Q4
p = 53.9
flow_h = np.sum((flow_data[:,3] > 53.9) & (flow_data[:,1]==9) & (flow_data[:,0]<2000))
flow_l = np.sum((flow_data[:,3] <= 53.9) & (flow_data[:,1]==9) & (flow_data[:,0]<2000))

print("9/2020 daily streamflows before 2000 compared to weekly prediction of 53.9 \n")
print("Days above 56: ", (flow_h))
print("Days below 56: ", (flow_l))
print ("Percentage of days above 56: ",(flow_h) / ((flow_h) + (flow_l)) *100, "%")

flow_h = np.sum((flow_data[:,3] > 53.9) & (flow_data[:,1]==9) & (flow_data[:,0]>2010))
flow_l = np.sum((flow_data[:,3] <= 53.9) & (flow_data[:,1]==9) & (flow_data[:,0]>2010))

print("9/2020 daily streamflows after 2010 compared to weekly prediction of 53.9 \n")
print("Days above 56: ", (flow_h))
print("Days below 56: ", (flow_l))
print ("Percentage of days above 56: ",(flow_h) / ((flow_h) + (flow_l)) *100, "%")
# %% Q5

sep_early = flow_data[(flow_data[:,2] <= 15) & (flow_data[:,1]==9) & (flow_data[:,0]==2011), 3]
sep_late = flow_data[(flow_data[:,2] > 15) & (flow_data[:,1]==9) & (flow_data[:,0]==2011), 3]
if (np.mean(sep_early)) > (np.mean(sep_late)):
        print ("Daily flow is greater in first half of September 2011")
else:
        print ("Daily flow is greater in second half of September 2011")

sep_early = flow_data[(flow_data[:,2] <= 15) & (flow_data[:,1]==9) & (flow_data[:,0]==2012), 3]
sep_late = flow_data[(flow_data[:,2] > 15) & (flow_data[:,1]==9) & (flow_data[:,0]==2012), 3]
if (np.mean(sep_early)) > (np.mean(sep_late)):
        print ("Daily flow is greater in first half of September 2012")
else:
        print ("Daily flow is greater in second half of September 2012")

sep_early = flow_data[(flow_data[:,2] <= 15) & (flow_data[:,1]==9) & (flow_data[:,0]==2013), 3]
sep_late = flow_data[(flow_data[:,2] > 15) & (flow_data[:,1]==9) & (flow_data[:,0]==2014), 3]
if (np.mean(sep_early)) > (np.mean(sep_late)):
        print ("Daily flow is greater in first half of September 2014")
else:
        print ("Daily flow is greater in second half of September 2014")

sep_early = flow_data[(flow_data[:,2] <= 15) & (flow_data[:,1]==9) & (flow_data[:,0]==2015), 3]
sep_late = flow_data[(flow_data[:,2] > 15) & (flow_data[:,1]==9) & (flow_data[:,0]==2015), 3]
if (np.mean(sep_early)) > (np.mean(sep_late)):
        print ("Daily flow is greater in first half of September 2015")
else:
        print ("Daily flow is greater in second half of September 2015")

sep_early = flow_data[(flow_data[:,2] <= 15) & (flow_data[:,1]==9) & (flow_data[:,0]==2015), 3]
sep_late = flow_data[(flow_data[:,2] > 15) & (flow_data[:,1]==9) & (flow_data[:,0]==2015), 3]
if (np.mean(sep_early)) > (np.mean(sep_late)):
        print ("Daily flow is greater in first half of September 2015")
else:
        print ("Daily flow is greater in second half of September 2015")

sep_early = flow_data[(flow_data[:,2] <= 15) & (flow_data[:,1]==9) & (flow_data[:,0]==2016), 3]
sep_late = flow_data[(flow_data[:,2] > 15) & (flow_data[:,1]==9) & (flow_data[:,0]==2016), 3]
if (np.mean(sep_early)) > (np.mean(sep_late)):
        print ("Daily flow is greater in first half of September 2016")
else:
        print ("Daily flow is greater in second half of September 2000")
# %%
