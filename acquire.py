# Creating the aquire.py file

# Make a new python module, acquire.py to hold the following data aquisition functions:
# get_titanic_data
# get_iris_data

# Importing libraries:

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Importing the os library specifically for reading the csv once I've created the file in my working directory.
import os

# web-based requests
import requests

# Make a function named get_titanic_data that returns the titanic data from the codeup data science database as a pandas data frame. Obtain your data from the Codeup Data Science Database.

# Setting up the user credentials:

from env import host, user, password

def get_db(db, user=user, host=host, password=password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

####################### REST API Acquire #######################

# Writing to a csv:

def write_csv(df, csv_name):
    '''
    The first argument (df) is the dataframe you want written to a .csv file. 
    The second argument (csv_name) must be a string, including the .csv extention. eg: 'example_df.csv'
    '''
    
    df.to_csv(csv_name, index = False)
    print('Completed writing df to .csv file')



# Acquiring the time series data:
def get_time_series(raw_data = 'anonymized-curriculum-access.txt'):
    '''
    Function will pull data from a .txt file that contains the logs from CodeUp's webpage access hits. 
    The function is specifically designed to ingest that kind of text file, and parse the data appropriately.
    '''

    colnames = ['date', 'timestamp', 'webpage', 'user_id', 'cohort_id', 'ip']

    df = pd.read_csv('anonymized-curriculum-access.txt', engine='python',
                     header=None,
                     index_col=False,
                     names=colnames,
                     sep=r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)(?![^\[]*\])',
                     na_values='"-"',
                     usecols=[0,1,2,3,4,5])
    return df


print('End of acquire.py file.')