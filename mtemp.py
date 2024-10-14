import pandas as pd
import io
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def temp_dataframe(folders, filename):
    dftemp = pd.read_csv(folders + filename, skiprows=6)
    dftemp['Time'] = pd.to_datetime(dftemp['Date/Time'])
    dftemp['Time'] = dftemp['Time'].dt.strftime('%H:%M:%S')
    dftemp = dftemp.set_index(pd.DatetimeIndex(dftemp['Time']))
    dftemp = dftemp.drop(['Sample', 'Date/Time', 'Time'], axis=1)
    dftemp = dftemp.reindex(sorted(dftemp.columns), axis=1)
    return dftemp
    
def get_headers(folders, filename):    
    dheaders = {}
    with io.open(folders + filename, mode='r', encoding='UTF-8-sig') as csus:
      for i, row in enumerate(csus):
          if(i>5):
              pass
          else:
            row = row.replace('"', '')
            num1 = row.split(':', 1)[0].strip('"')
            num2 = row.split(':', 1)[1]
            num2 = num2.strip()
            num2 = num2.strip('\n')
            dheaders[num1] = num2   

    dheaders["folders"] = folders
    dheaders["filename"] = filename       
    return dheaders

def tempCtoF(dataframeC):
    dataframeF = dataframeC.apply(lambda x: x*(9/5) + 32)
    dataframeF.columns = dataframeF.columns.str.replace("°C", "°F", regex=True)
    return dataframeF

def tempFtoC(dataframeF):
    dataframeC = dataframeF.apply(lambda x: (x-32)*(5/9))
    dataframeC.columns = dataframeC.columns.str.replace("°F", "°C", regex=True)
    return dataframeC

def tempIR_VtoC(dataframeV):
    dataframeC = dataframeV.filter(like='IR').apply(lambda x: (x-0.620) * 105.263)
    dataframeC.columns = dataframeC.columns.str.replace("Raw \(V\)", "°C", regex=True)
    return dataframeC

# Temperature Time Series
def lineplots(dftemp, headers):

    ##gen unit from column names
    s = dftemp.columns[0]
    unit = s[s.find("(")+1:s.find(")")]
    testunit = "AI0 (" + unit + ")"

    ## determine cart number from DAQ serial numbers
    daqnum = headers["Serial Number"]
    if (daqnum == "21AD4B7" or daqnum =="2082107"):
        cart = "Cart 1" 
        configs = {'AI0 (°C)': '1.8 ft (°C)', 
                   'AI1 (°C)': '5.4 ft (°C)',  
                   'AI2 (°C)': '0.6 ft (°C)', 
                   'AI3 (°C)': '3.6 ft (°C)', 
                   'AI4 (°C)': '7.2 ft (°C)', 
                   'AI5 (°C)': '9.0 ft (°C)', 
                   'AI6 (°C)': '3.6 ft b (°C)' , 
                   'AI7 (°C)': '5.4 ft b (°C)'
                   }    
    if daqnum == "1DE5504" or daqnum == "2082107bbbb":
        cart = "Cart 2" 
        configs = {'AI2 (°C)': '1.8 ft (°C)', 
                   'AI1 (°C)': '0.6 ft (°C)',  
                   'AI3 (°C)': '3.6 ft (°C)', 
                   'AI4 (°C)': '3.6 ft b (°C)', 
                   'AI0 (°C)': '5.4 ft (°C)', 
                   'AI5 (°C)': '5.4 ft b (°C)', 
                   'AI6 (°C)': '7.2 ft (°C)' , 
                   'AI7 (°C)': '9.0 ft (°C)'
                   }

    if testunit in dftemp.columns:
        dftemp.rename(columns=configs, inplace=True)

    dftemp = dftemp.reindex(sorted(dftemp.columns), axis=1)

    # I want heights to be explicity referenced here, so there's no mucking it up, even if the hardware changes. 
    plt.figure(figsize=(40, 10))
    colordict = {
        "5.4 ft b": (0, 0.8, 0.8),   # cyan light
        "3.6 ft b": (0.7, 0.5, 0.5),  # maroon light
        "9.0 ft": (0.6, 0.6, 0.6),  # 
        "7.2 ft": (0.4, 0.4, 0.4),   #
        "5.4 ft": (0, 0.5, 0.5), # cyan
        "3.6 ft": (0.6, 0, 0),  # maroon
        "1.8 ft": (0.3, 0.3, 0.3), # 
        "0.6 ft": (0.0, 0.0, 0.0),  # 
    }

    #if 'btemps' ==True:
    lablist = []
    for column in dftemp.columns:
        lab = column.replace(unit, "")
        lab = lab.replace(" ()", "")
        plt.plot(dftemp.index, dftemp[column], label=column,
            color=colordict[lab], linewidth=5.0)
        lablist.append(lab)


    
    ylabel = 'Temperature (' + unit + ")"
    title =  cart + ":" + headers["folders"] + headers["filename"]
    #lablist.reverse()

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.xlabel('Time (HH:MM)', fontsize=50)    
    plt.tick_params(axis='both', which='major', labelsize=40)
    plt.ylabel(ylabel, fontsize=50)
    plt.title(title, fontsize=60)
    #handles, labels = plt.gca().get_legend_handles_labels()
    #labels = lablist
    #plt.legend(reversed(handles), reversed(labels), loc=(1.04, 0), fontsize=40)
    plt.legend(loc=(1.04, 0), fontsize=40, labels = lablist)
    plt.tight_layout()
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    # plt.savefig('/content/drive/MyDrive/Environmental Frontiers Autumn 2024/M-TEMP Tests/QA Testing 091624/Cart 1 Indoor Test 2 Data')
    plt.show()  


# Temperature Time Series
def main_lineplots(folders, filename, tempunit = "C"):
    ##run using just folders and filename and running other functions within this function

    dftemp = temp_dataframe(folders, filename)
    headers = get_headers(folders, filename)

    s = dftemp.columns[0]
    unit = s[s.find("(")+1:s.find(")")]
    if tempunit in unit:
        lineplots(dftemp, headers)  
        return dftemp, headers
    if tempunit not in unit: 
        if tempunit == "C":
            dftemp = tempFtoC(dftemp)
        if tempunit == "F":
            dftemp = tempCtoF(dftemp)
        lineplots(dftemp, headers)      
        return dftemp, headers

    