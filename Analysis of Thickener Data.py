import numpy as np
import matplotlib.pyplot as plt

#for reading timestamps on the CSV file
import datetime

#%%

"""
Functions that I call throughout
"""
def plotdata(time_start,time_end,col,plot = True):
    """
    This function requires the data to be loaded as it is in Section 1. 
    """
    startindex = 0
    endindex = 0
    for i in range(0,len(time_obj)):
        if (time_obj[i] == time_start):
            startindex = i
        if(time_obj[i] == time_end):
            endindex = i+1
    if(startindex<=badindex<=endindex):
        raise Exception ("This plot/data is inaccurate and over the wierd timeindex.")
    if(plot == True):
        t = np.linspace(0,(endindex-startindex-1),(endindex-startindex))
        reading = data[startindex:endindex,col-1]
        plt.plot(t,reading,label = header[col-1])
        plt.xlabel("Time (min)")
        plt.ylabel("Sensor Reading")
        title = "Sensor " + header[col-1] + " \nFrom " + time_start.strftime("%m/%d/%Y, %H:%M:%S") +" to "+ time_end.strftime("%m/%d/%Y, %H:%M:%S")
        plt.title(label = title)
        plt.show()
        print("Sensor Description:",sensor_description[col-1])
        print("Sensor Units:",sensor_units[col-1])
    return data[startindex:endindex,col-1]
#%%
"""
This section imports the data from publishable_test_set.CSV
Section 1
"""
    

#Round about way of getting the dimension size so we know what cols to read
data_raw = np.loadtxt("publishable_test_set.CSV",delimiter = ",",dtype=object)
data_dimensions = np.shape(data_raw)
usecol_input = np.linspace(1,data_dimensions[1]-1,data_dimensions[1]-1,dtype = int)

#get a string of headers
header_file = open("publishable_test_set.CSV")
header = header_file.readline()
header = header.split(',')

#Get the explanation of what sensors do
sensor_description = np.loadtxt("Sensor_Names.CSV", delimiter = ",", dtype = str, usecols = 0)
sensor_units = np.loadtxt("Sensor_Names.CSV",delimiter = ",", dtype = str, usecols = 1)

#Extract all the data points we can. Change "No Data" and "Bad Input" cells to None
data_raw = np.loadtxt("publishable_test_set.CSV",delimiter = ",",skiprows = 1, usecols = usecol_input, dtype = str)
time = np.loadtxt("publishable_test_set.CSV", delimiter = ",",skiprows =1, usecols = 0, dtype = str)
data_dimensions = np.shape(data_raw)
number_sensors = len(data_raw[1])

data_dimensions = np.shape(data_raw)
data = np.zeros(data_dimensions)
for i in range(0,data_dimensions[0]):
    for j in range(0,data_dimensions[1]):
        try:
            data[i,j] = float(data_raw[i,j])
        except:
            data[i,j] = None
        

#convert all time stamps into datetime objects for convience
time_obj = []
for i in range(0,len(time)):
    time_obj1 = datetime.datetime.strptime(time[i],"%Y-%m-%d %H:%M:%S") 
    time_obj.append(time_obj1)

"""
End of Section 1
"""
#%%
print("Quality Tests of data:")
print("Are there equivalent time intervals?")
#test to see if all timestamps have the same time interval of 1 minute
for i in range(0,len(time_obj)-1):
    dt = time_obj[i+1]-time_obj[i]
    if(str(dt) != "0:01:00"):
        print("Not Equal time interval of 1 minute")
        print("time interval:", dt)
        print("Index Location for time_obj array", i)
        badindex = i
print("Conclusion: Yes, time intervals are every minute accept for one value")

#sensor1 =plotdata(time_obj[0],time_obj[60],1)
for i in range(1,number_sensors+1):
    plotdata(time_obj[0],time_obj[240],i)

