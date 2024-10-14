# M-TEMP data analysis

This is python code used to process data from the University of Chicago mobile temperature measurement system (M-TEMP). 

The analysis functions are included in mtemp.py. 

main.py shows an example processing script. 

## Code processing basics

In order to run the main.py scrip, change the path to the location of the "Walks and Tests" folder on your system. 

```python
path = "C:/Users/cweyt/Dropbox/_Papers/2a_M-Temp/data/raw/Mapping/Walks and Tests/"
```

You can run a file, by selecting the folders and filename of a datafile. Currently, this code is only running the USB-TEMP DAQ, RTD sensors.  

```python
folders = 'Roosevelt Walk Day 1 M-TEMP 072224/sensordata/walk_data_roosevelt/'
filename = 'temproosevelt.csv'

dftemp, headers = mtemp.main_lineplots(folders, filename, tempunit = "C") 
```

You can also use the functions in mtemp to more manually process the data. 

*temp_dataframe* is used to bring the data in the folder into a dataframe using the folders and filename as inputs.

```python
dftemp = mtemp.temp_dataframe(folders, filename)
```
*get_headers* is used to can the meta data from the file header. 

```python
headers = mtemp.get_headers(folders, filename)
```
*tempCtoF* and *tempFtoC* can be used to change the temperature unit. It also changes the unit in the variable names. 

```python
dftempF = mtemp.tempCtoF(dftemp)
```

## Remaining issues

1. Need to code a way to plot a subset of the channels by adding an option to lineplots. 
2. Running in F is currently not working in lineplots - I broke it in the lastest version and need to de-bug. opps. 
3. Need to have a merge files function. 
4. Need to build start and endtimes as option in lineplot to quickly plot only a portion of the data. 
5. IR functionallity is started but not complete in mtemp.py. We need to have an averaging time option because the data is so coarse. 
6. Configs may need to be updated if cart 1 and cart 2 have not always had the same configurations. See mtemp lines 58-79.
