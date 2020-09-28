# Example solution for HW 4

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
filename = 'streamflow_week5.txt'
filepath = os.path.join('C:/Users/Richard/Desktop/class/Course_Materials/homework-richardmarcelain/data/', filename)
print(os.getcwd())
print(filepath)

#filepath = '../Assignments/Solutions/data/streamflow_week1.txt'

# %%
#Read the data into a pandas dataframe
data=pd.read_table(filepath, sep = '\t', skiprows=30,
        names=['agency_cd', 'site_no', 'datetime', 'flow', 'code']
        )

# Expand the dates to year month day
data[["year", "month", "day"]] =data["datetime"].str.split("-", expand=True)
data['year'] = data['year'].astype(int)
data['month'] = data['month'].astype(int)
data['day'] = data['day'].astype(int)

# %%
# Sorry no more helpers past here this week, you are on your own now :) 
# Hints - you will need the functions: describe, info, groupby, sort, head and tail.

# %% Q1
data.info()


# %% Q2
print("Statistics of Daily Flow [cfs]")
dflow = np.round(data['flow'].describe(), decimals=2); dflow


# %% Q3
print("Statistics of Monthly Flow [cfs]")
mflow = np.round(data.groupby(["month"])[["flow"]].describe(), decimals=2); mflow


# %% Q4
print("5 Lowest Flow Days\n")
print(data.sort_values(['flow']).head())
print("\n\n5 Highest Flow Days\n")
print(data.sort_values(['flow']).tail())


# %% Q4
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.DataFrame()
df['Date'] = ['2012-07-01', '2012-07-02', '2012-06-30', '2012-06-29', '2012-07-03', '1995-03-06', '2005-02-12', '1995-02-15', '1993-02-20', '1993-01-08']
df['Month'] = ['July', 'July', 'June', 'June', 'July', 'March', 'February', 'February', 'February', 'January']
df['Flow [cfs]'] = [19.0, 20.1, 22.1, 22.5, 23.4, 30500.0, 35600.0, 45500.0, 61000.0, 63400.0 ]

def render_mpl_table(data, col_width=3.0, row_height=0.625, font_size=14,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')
    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)
    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in mpl_table._cells.items():
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0]%len(row_colors) ])
    return ax.get_figure(), ax

fig,ax = render_mpl_table(df, header_columns=0, col_width=2.0)
fig.savefig("HW5_table1.png")

# %% Q5

print("Highest Daily Flow of each Month \n")
print(data.groupby(["month"], as_index=False)[["flow"]].max())
print("\n\nLowest Daily Flow of each Month \n")
print(data.groupby(["month"], as_index=False)[["flow"]].min())

# %% Q5 location of max and min flows per month

# Max
print(data.iloc[np.flatnonzero(data['flow'] == 63400.0)]) #'93
print(data.iloc[np.flatnonzero(data['flow'] == 61000.0)]) #'93
print(data.iloc[np.flatnonzero(data['flow'] == 30500.0)]) #'95
print(data.iloc[np.flatnonzero(data['flow'] == 4690.0)]) #'91
print(data.iloc[np.flatnonzero(data['flow'] == 546.0)]) #'92
print(data[(data['flow'] == 481.0) & (data['month'] == 6)]) #'92
print(data[(data['flow'] == 1040.0) & (data['month'] == 7)]) #'06
print(data.iloc[np.flatnonzero(data['flow'] == 5360.0)]) #'92
print(data.iloc[np.flatnonzero(data['flow'] == 5590.0)]) #'04
print(data[(data['flow'] == 1910.0) & (data['month'] == 10)]) #'10
print(data.iloc[np.flatnonzero(data['flow'] == 4600.0)]) #'04
print(data.iloc[np.flatnonzero(data['flow'] == 28700.0)]) #'04

print('\n\n')

# Min
print(data[(data['flow'] == 158.0) & (data['month'] == 1)]) #'03
print(data[(data['flow'] == 136.0) & (data['month'] == 2)]) #'91
print(data[(data['flow'] == 97.0) & (data['month'] == 3)]) #'89
print(data[(data['flow'] == 64.9) & (data['month'] == 4)]) #'18
print(data[(data['flow'] == 46.0) & (data['month'] == 5)]) #'04
print(data.iloc[np.flatnonzero(data['flow'] == 22.1)]) #'12
print(data.iloc[np.flatnonzero(data['flow'] == 19.0)]) #'12
print(data.iloc[np.flatnonzero(data['flow'] == 29.6)]) #'19
print(data[(data['flow'] == 36.6) & (data['month'] == 9)]) #'20
print(data[(data['flow'] == 69.9) & (data['month'] == 10)]) #'12
print(data[(data['flow'] == 117.0) & (data['month'] == 11)]) #'16
print(data[(data['flow'] == 155.0) & (data['month'] == 12)]) #'12


# %% Q5

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.DataFrame()
df['Month'] = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
df['Max Flow'] = [1993,1993,1995,1991,1992,1992,2006,1992,2004,2010,2004,2004]
df['Min Flow'] = [2003,1991,1989,2018,2004,2012,2012,2019,2020,2012,2016,2012 ]

def render_mpl_table(data, col_width=3.0, row_height=0.625, font_size=14,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')
    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)
    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in mpl_table._cells.items():
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0]%len(row_colors) ])
    return ax.get_figure(), ax

fig,ax = render_mpl_table(df, header_columns=0, col_width=2.0)
fig.savefig("HW5_table2.png")

# %% Q6

print(data[(data['flow'] > (101.5*.9)) & (data['flow'] < (101.5*1.1)) & (data['month'] == 8) & (data['day'] == 31)])



# %% Forecasting

z = data[(data['month'] == 8) & (data['year'] == 2019) & (data['day'] >= 25) & (data['day'] <= 31)].mean()
print("8/31: ",np.round(z['flow'], decimals=2))

z = data[(data['month'] == 9) & (data['year'] == 2019) & (data['day'] >= 1) & (data['day'] <= 7)].mean()
print("9/7: ",np.round(z['flow'], decimals=2))

z = data[(data['month'] == 9) & (data['year'] == 2019) & (data['day'] >= 8) & (data['day'] <= 14)].mean()
print("9/14: ",np.round(z['flow'], decimals=2))

z = data[(data['month'] == 9) & (data['year'] == 2019) & (data['day'] >= 15) & (data['day'] <= 21)].mean()
print("9/21: ",np.round(z['flow'], decimals=2))

z = data[(data['month'] == 9) & (data['year'] == 2019) & (data['day'] >= 22) & (data['day'] <= 28)].mean()
print("9/28: ",np.round(z['flow'], decimals=2))

z = data[(data['month'] == 10) & (data['year'] == 2019) & (data['day'] >= 1) & (data['day'] <= 5)].mean()
print("10/5: ",np.round(z['flow'], decimals=2))

z = data[(data['month'] == 10) & (data['year'] == 2019) & (data['day'] >= 6) & (data['day'] <= 12)].mean()
print("10/12: ",np.round(z['flow'], decimals=2))

z = data[(data['month'] == 10) & (data['year'] == 2019) & (data['day'] >= 13) & (data['day'] <= 19)].mean()
print("10/19: ",np.round(z['flow'], decimals=2))

z = data[(data['month'] == 10) & (data['year'] == 2019) & (data['day'] >= 20) & (data['day'] <= 26)].mean()
print("10/26: ",np.round(z['flow'], decimals=2))

z = data[(data['month'] == 10) & (data['year'] == 2019) & (data['day'] >= 23) & (data['day'] <= 31)].mean()
print("11/2: ",np.round(z['flow'], decimals=2))

z = data[(data['month'] == 11) & (data['year'] == 2019) & (data['day'] >= 1) & (data['day'] <= 9)].mean()
print("11/9: ",np.round(z['flow'], decimals=2))

z = data[(data['month'] == 11) & (data['year'] == 2019) & (data['day'] >= 10) & (data['day'] <= 16)].mean()
print("11/16: ",np.round(z['flow'], decimals=2))

z = data[(data['month'] == 11) & (data['year'] == 2019) & (data['day'] >= 17) & (data['day'] <= 23)].mean()
print("11/23: ",np.round(z['flow'], decimals=2))

z = data[(data['month'] == 11) & (data['year'] == 2019) & (data['day'] >= 24) & (data['day'] <= 30)].mean()
print("11/30: ",np.round(z['flow'], decimals=2))

z = data[(data['month'] == 12) & (data['year'] == 2019) & (data['day'] >= 1) & (data['day'] <= 7)].mean()
print("12/7: ",np.round(z['flow'], decimals=2))

z = data[(data['month'] == 12) & (data['year'] == 2019) & (data['day'] >= 8) & (data['day'] <= 14)].mean()
print("12/14: ",np.round(z['flow'], decimals=2))
# %%
