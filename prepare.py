# Function module to prepare my sales data:

# Importing libraries:

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import seaborn as sns

# splitting data:
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, QuantileTransformer, PowerTransformer, RobustScaler, MinMaxScaler

# Importing the os library specifically for reading the csv once I've created the file in my working directory.
import os

import warnings
warnings.filterwarnings("ignore")

# web-based requests
import requests

# Time based libraries
import datetime
from time import strftime

# Importing my acquire module:
import acquire
import env
import rapid_env

# This is to make sure matplotlib doesn't throw the following error:
# The next line fixes "TypeError: float() argument must be a string or a number, not 'Timestamp' matplotlib"
pd.plotting.register_matplotlib_converters()

# Main prep function, which works from my acquire file to just prior to splitting the data. Does not include any visualizations:
def prep_web_project(df):
    '''
    This function will prepare the dataframe for exploration. 
    '''
    
    # Combining the date and time into one column
    df['date_time'] = df['date'] + " " + df["timestamp"]
    df['date_time'] = pd.to_datetime(df.date_time)
    
    # Dropping old columns:
    df.drop(columns = ['date', 'timestamp'], inplace = True)
    
    # Now to set that dt as the index:
    df = df.set_index('date_time')
    
    # Adding columns for future analysis and exploration:
    
    df['year'] = df.index.year
    df['month'] = df.index.month
    df['day'] = df.index.day
    df['hour'] = df.index.hour
    df['weekday'] = df.index.day_name()

    # Idetifying datascience cohorts:
    df['is_ds'] = df.cohort_id.isin([30, 34, 55, 59])
    
    return df
    


# Germany ops function:

def prep_ops():
    
    # acquiring the data:
    ops_df = acquire.get_germany_power()
    
    # Converting the date column to datetime:
    ops_df.date = pd.to_datetime(ops_df.date)
    
    # Setting the date as the index:
    ops_df = ops_df.set_index('date').sort_index()

    
    # Visulizing the columns:
    for col in ops_df.columns:
        plt.figure(figsize = (4, 2))
        plt.hist(ops_df[col])
        plt.title(col)
        plt.show()
    
    # Adding month and year columns:
    ops_df['month'] = ops_df.index.day
    ops_df['month'] = ops_df.index.month
    ops_df['year'] = ops_df.index.year
    
    # filling missing values:
    ops_df = ops_df.fillna(0)
    
    return ops_df


# Splitting the data:

    # split dataset
def split_data(df):
    '''
    This function will split a dataframe into 3 dataframes: train, validate and test.
    The random state is set to 123 by default, the validate test_size argument is set to .2, and the test test_size is set to .3.
    '''
    train_validate, test = train_test_split(df, test_size = .2, random_state = 123)
    train, validate = train_test_split(train_validate, test_size = .3, random_state = 123)
    return train, validate, test
    print(train.shape, validate.shape, test.shape)

# computing Entropy in a pandas series:

def compute_entropy(series):
    '''
    Function for computing Entropy in a series. Simply enter the series name (needs to be int or float).
    '''
    counts = series.value_counts()
    if len(counts)==1:
        ent = 0
    else:
        value, counts = np.unique(series, return_counts=True)
        ent = entropy(counts, base=None)
    return ent



print('Loaded all prepare functions.')