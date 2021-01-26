import numpy as np
import matplotlib.pyplot as plt

#for reading timestamps on the CSV file
import datetime

#%%

"""
Functions that I call throughout
"""
def plotdata(time_start,time_end,col,plot = True, extrainfo = True, overlay = False):
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
    for i in range(0,len(badindex)):
        if(startindex<=badindex[i]<=endindex):
            print("Accept bad time range? (no/anything else)")
            answer = input()
            if(answer == "no"):
                raise Exception ("This plot/data is inaccurate and over the wierd timeindex.")
    if(plot == True):
        t = np.linspace(0,(endindex-startindex-1),(endindex-startindex))
        reading = data[startindex:endindex,col]
        plt.plot(t,reading,label = header[col])
        if(extrainfo == True):
            avg = np.mean(reading)
            avg_plt = np.ones(len(t))*avg
            plt.plot(t,avg_plt, label = "Average")
            if(parameter[col] != 0 and parameter[col] !=1):
                constraint = parameter[col]
                con_plt = np.ones(len(t))*constraint
                label_str = parameter_description[col]+" Constraint"
                plt.plot(t,con_plt,label = label_str)
            if(parameter[col] == 1.0):
                con_plt = np.ones(len(t))
                solids_con = data[startindex:endindex,col+1]
                for i in range(0, len(t)):
                    def Min_UFR(solids_con): #Returns the minimum underflow rate based on the solids_concentration
                        return -2.7857*solids_con**2 + 392.3*solids_con - 12443
                    con_plt[i] = Min_UFR(solids_con[i])
                    label_str = parameter_description[col] + " Constraint"
                plt.plot(t,con_plt,label = label_str)
        plt.xlabel("Time (min)")
        plt.ylabel("Sensor Reading")
        title = "Sensor: " + header[col] + " \nFrom " + time_start.strftime("%m/%d/%Y, %H:%M:%S") +" to "+ time_end.strftime("%m/%d/%Y, %H:%M:%S")
        plt.title(label = title)
        plt.legend()
        if(overlay == False):
            plt.show()
        print("Sensor Description:",sensor_description[col])
        print("Sensor Units:",sensor_units[col])
        print("Standard Deviation:", np.std(reading))
    return data[startindex:endindex,col]

def plothist(time_start,time_end,col,plot = True):
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
    for i in range(0,len(badindex)):
        if(startindex<=badindex[i]<=endindex):
            print("Accept bad time range? (no/anything else)")
            answer = input()
            if(answer == "no"):
                raise Exception ("This plot/data is inaccurate and over the wierd timeindex.")
    reading = data[startindex:endindex,col]

    if(plot == True):
        try:
            plt.hist(reading, bins = 100)
            title = "Sensor: " + header[col] + " \nFrom " + time_start.strftime("%m/%d/%Y, %H:%M:%S") +" to "+ time_end.strftime("%m/%d/%Y, %H:%M:%S")
            plt.title(label = title)
            plt.show()
            print("Sensor Description:",sensor_description[col])
            print("Sensor Units:",sensor_units[col])
        except:
            print("Skipped Histogram:", header[col], "because of nan values")
    return data[startindex:endindex,col]
def detectspikes(dataset,std_from_mean = 3,print_it = True,col =0):
    stdv = np.std(dataset)
    mean = np.mean(dataset)

    spike_indexes = []
    spike_values = []
    for i in range(0,len(dataset)):
        value = dataset[i]
        if(value>= (mean+std_from_mean*stdv) or value <= (mean-std_from_mean*stdv)):
            spike_indexes.append(i)
            spike_values.append(value)
    if(print_it == True):
        print("Sensor", header[col])
        print("Spike Indexes:",spike_indexes)
        print("Spike Values:", spike_values)
    return [spike_indexes,spike_values]

def subplotdata(rows,col,sensor_start,sensor_finish,time_start,time_end):
    plt.figure(figsize=(15,15))
    count = 1
    for i in range(sensor_start,sensor_finish):
        plt.subplot(rows,col,count)
        t= np.linspace(time_start,time_end,time_end-time_start+1)
        values = plotdata(time_obj[time_start],time_obj[time_end],i,plot = False)
        plt.plot(t,values, label = sensor_description[i])
        startindex = time_start
        endindex = time_end+1
        if(parameter[i] != 0 and parameter[i] !=1):
            constraint = parameter[i]
            con_plt = np.ones(len(t))*constraint
            label_str = parameter_description[col]+" Constraint"
            plt.plot(t,con_plt,label = label_str)
        if(parameter[i] == 1):
            con_plt = np.ones(len(t))
            solids_con = data[startindex:endindex,i+1]
            for j in range(0, len(t)):
                def Min_UFR(solids_con): #Returns the minimum underflow rate based on the solids_concentration
                    return -2.7857*solids_con**2 + 392.3*solids_con - 12443
                con_plt[j] = Min_UFR(solids_con[j])
                label_str = parameter_description[col] + " Constraint"
            plt.plot(t,con_plt,label = label_str)
        count +=1
        plt.xlabel("time (min)")
        plt.legend(loc = "best")

#%%
"""
This section imports the data from publishable_test_set.CSV
Section 1
"""


#Round about way of getting the dimension size so we know what cols to read
data_raw = np.loadtxt("train.csv",delimiter = ",",dtype=object,encoding = 'unicode_escape')
data_dimensions = np.shape(data_raw)
usecol_input = np.linspace(0,data_dimensions[1]-1,data_dimensions[1],dtype = int)

#get a string of headers
header_file = open("train.csv")
header = header_file.readline()
header = header.split(',')

#Get the explanation of what sensors do
sensor_description = np.loadtxt("Sensor_Names.csv", delimiter = ",", dtype = str, usecols = 0,encoding = 'unicode_escape')
sensor_units = np.loadtxt("Sensor_Names.csv",delimiter = ",", dtype = str, usecols = 1,encoding = 'unicode_escape')

#get the parameters of sensors
parameter = np.loadtxt("Sensor_Names.csv", delimiter = ",", dtype = float,usecols = 2,encoding = 'unicode_escape')
parameter_description = np.loadtxt("Sensor_Names.csv", delimiter = ",", dtype = str, usecols = 3,encoding = 'unicode_escape')


#Extract all the data points we can. Change "No Data" and "Bad Input" cells to None
data_raw = np.loadtxt("train.csv",delimiter = ",",skiprows = 1, usecols = usecol_input, dtype = str,encoding = 'unicode_escape')
time = np.loadtxt("train.csv", delimiter = ",",skiprows =1, usecols = 0, dtype = str,encoding = 'unicode_escape')
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
print("Quality Tests of data:\n")
print("Number of Times time interval is not 1 min")
#test to see if all timestamps have the same time interval of 1 minute
number_bad_times = 0
badindex = []
for i in range(0,len(time_obj)-1):
    dt = time_obj[i+1]-time_obj[i]
    if(str(dt) != "0:01:00"):
        print("Not Equal time interval of 1 minute")
        print("time interval:", dt)
        print("Index Location for time_obj array", i,"\n")
        badindex.append(i)
        number_bad_times += 1
print("Total Number Bad Time Intervals:", number_bad_times,"\n")

#plot what it looks like for the first 4 hours
for i in range(1,number_sensors):
    plotdata(time_obj[0],time_obj[1000],i)

#plot the averages
#%%
for i in range(1,number_sensors):
    plothist(time_obj[0],time_obj[4000],i)

#%%
# find the spikes
for i in range(1,2):
    plotdata(time_obj[2000],time_obj[2500],i)
    plothist(time_obj[2000],time_obj[2500],i)
    dataset =plotdata(time_obj[2500],time_obj[2500],i,plot = False)
    a =detectspikes(dataset,col = i,std_from_mean = 6)
    print("") 

#%%
real = np.array(plotdata(time_obj[0],time_obj[2000],19,overlay = True))
target = np.array(plotdata(time_obj[0],time_obj[2000],28))

Error = np.abs(real-target)
t = np.linspace(0,2000,2001)
plt.plot(t,Error)

#%%
plotdata(time_obj[2420],time_obj[2460],1)
subplotdata(9,3,1,28,0,500)
