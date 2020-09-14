# Start code for assignment 3
# this code sets up the lists you will need for your homework
# and provides some examples of operations that will be helpful to you

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
filename = 'C:/Users/Richard/Desktop/class/Course_Materials/homework-richardmarcelain/data/streamflow_week3.txt'
filepath = os.path.join('data', filename)
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

#make lists of the data
flow = data.flow.values.tolist()
date = data.datetime.values.tolist()
year = data.year.values.tolist()
month = data.month.values.tolist()
day = data.day.values.tolist()

# Getting rid of the pandas dataframe since we wont be using it this week
del(data)

# %%
# Here is some starter code to illustrate some things you might like to do
# Modify this however you would like to do your homework. 
# From here on out you should use only the lists created in the last block:
# flow, date, year, month and day

# Calculating some basic properites
print("Total Dataset Flow Values (cubic feet per second)")
print("Min:  ",min(flow))
print("Max:  ",max(flow))
print("Mean: ",np.mean(flow))
print("Std:  ",np.std(flow))

# Making an empty list that I will use to store
# index values I'm interested in
ilist = []

# Loop over the length of the flow list
# and adding the index value to the ilist
# if it meets some criteria that I specify
for i in range(len(flow)):
        if flow [i] > 600 and month[i] == 7:
                ilist.append(i)

# see how many times the criteria was met by checking the length
# of the index list that was generated
#print(len(ilist))

# Alternatively I could have  written the for loop I used 
# above to  create ilist like this
ilist2 = [i for i in range(len(flow)) if flow[i] > 600 and month[i]==7]
#print(len(ilist2))

# Grabbing out the data that met the criteria
# This  subset of data is just the elements identified 
# in the ilist
subset = [flow[j] for j in ilist]


# %% HW3 Q1

print("Identifying type of objects in various lists \n")

if type(flow[1]) is int:
        print ("Flow object type: integer")
else:
        print ("Flow object type: float")

if type(year[1]) is int:
        print ("Year object type: integer")
else:
        print ("Year object type: float")  

if type(month[1]) is int:
        print ("Month object type: integer")
else:
        print ("Month object type: float") 

if type(day[1]) is int:
        print ("Day object type: integer")
else:
        print ("Day object type: float") 

# %% HW3 Q2
sep_a = []
sep_b = []
for i in range(len(flow)):
        if month [i] == 9 and year [i] == 2020:
                if flow [i] > 56: 
                        sep_a.append(flow[i])
                else:
                        sep_b.append(flow[i])

print("9/2020 daily streamflows compared to weekly prediction of 56 \n")
print("Days above 56: ", len(sep_a))
print("Days below 56: ", len(sep_b))
print ("Percentage of days above 56: ",len(sep_a) / (len(sep_a) + len(sep_b)) *100, "%")
# %% HW3 Q3
sep_a_old = []
sep_b_old = []
sep_a_new = []
sep_b_new = []
for i in range(len(flow)):
        if month [i] == 9 and year [i] < 2000:
                if flow [i] > 56: 
                        sep_a_old.append(flow[i])
                else:
                        sep_b_old.append(flow[i])
        elif month [i] == 9 and year [i] > 2010:
                if flow [i] > 56: 
                        sep_a_new.append(flow[i])
                else:
                        sep_b_new.append(flow[i])
print("September daily streamflows before 2000 compared to weekly prediction of 56 \n")
print("Days above 56: ", len(sep_a_old))
print("Days below 56: ", len(sep_b_old))
print ("Percentage of days above 56: ",len(sep_a_old) / (len(sep_a_old) + len(sep_b_old)) *100, "% \n\n")   

print("September daily streamflows after 2010 compared to weekly prediction of 56 \n")
print("Days above 56: ", len(sep_a_new))
print("Days below 56: ", len(sep_b_new))
print ("Percentage of days above 56: ",len(sep_a_new) / (len(sep_a_new) + len(sep_b_new)) *100, "%")
# %% HW3 Q4
yr=np.arange(1989,2020)

earlyflow = []
laterflow = []
for k in range(len(yr)):
        sep_early = [i for i in range(len(flow)) if day [i] <= 15 and month[i]==9 and year[i] == yr[k]]
        sep_late = [i for i in range(len(flow)) if day [i] > 15 and month[i]==9 and year[i] == yr[k]]
        d1 = [flow[j] for j in sep_early]
        d2 = [flow[j] for j in sep_late]
        if d1 > d2:
                print("Average flow greater in early September,", yr[k])
                earlyflow.append(d1)
        else:
                print("Average flow greater in late September, ", yr[k])
                earlyflow.append(d2)

if len(earlyflow) > len(laterflow):
        print("\nAverage flow generally decreases with time in September")
else:
        print("Average flow generally increases with time in September")


# %%
