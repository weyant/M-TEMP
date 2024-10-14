#!/usr/bin/env python
# coding: utf-8

# ## Imports
import pandas as pd
import numpy as np
import os
print(os.getcwd())

import mtemp as mtemp
import warnings
warnings.filterwarnings('ignore')
warnings.filterwarnings("ignore", category=DeprecationWarning)


# ## Data location
path = "C:/Users/cweyt/Dropbox/_Papers/2a_M-Temp/data/raw/Mapping/Walks and Tests/"
os.chdir(path)

#folders = 'QA Testing 091624/Cart 1 Indoor Data/'
#filename = 'USB-TEMP (Device 0) - Analog - 9-16-2024 2-09-36.6 PM.csv'
#filenameIR = 'USB-1208FS-Plus (Device 1) - Analog - 9-16-2024 2-09-37.1 PM.csv'

#folders = 'QA Testing 091624/Cart 1 Outdoor Data/'
#filename = 'USB-TEMP (Device 0) - Analog - 9-16-2024 1-09-41.2 PM.csv'

#folders = 'QA Testing 091624/Cart 1 Indoor Data/Messed up sample rates/'
#filename = 'USB-TEMP (Device 0) - Analog - 9-16-2024 10-49-03.8 AM.csv'

folders = 'Roosevelt Walk Day 1 M-TEMP 072224/sensordata/walk_data_roosevelt/'
filename = 'temproosevelt.csv'

dftemp, headers = mtemp.main_lineplots(folders, filename, tempunit = "C") 


# # read in data
##read in mtemp tempdaq data using the folder and filename of your desired file
dftemp = mtemp.temp_dataframe(folders, filename)

##read in mtemp IR data using the folder and filename of your desired file
dftempIR = mtemp.temp_dataframe(folders, filenameIR)

##read in file headers as dictionary datatype
headers = mtemp.get_headers(folders, filename)
headersIR = mtemp.get_headers(folders, filenameIR)


##example data
headers
##accessing example data from dictionary datatype
headers["Device"]


##unit converstion functions
dftempF = mtemp.tempCtoF(dftemp)
dftempIRc = mtemp.tempIR_VtoC(dftempIR)
dftempIRf = mtemp.tempCtoF(dftempIRc)


# Temperature Time Series
mtemp.lineplots(dftemp, headers)

