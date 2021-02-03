import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

#for reading timestamps on the CSV file
import datetime

#%%

"""
Functions that I call throughout
"""
def Min_UFR(solids_con): #Returns the minimum underflow rate based on the solids_concentration
    return -2.7857*solids_con**2 + 392.3*solids_con - 12443
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

def detectspikes(col, dataset = [0],std_from_mean = 3,print_it = True, below_value = False, objective = 50):
    if(dataset == [0]):
        dataset = data[:,col]
    stdv = np.nanstd(dataset)
    mean = np.nanmean(dataset)

    spike_indexes = []
    spike_values = []
    for i in range(0,len(dataset)):
        value = dataset[i]
        if(value>= (mean+std_from_mean*stdv) or value <= (mean-std_from_mean*stdv)):
            spike_indexes.append(i)
            spike_values.append(value)
    if(print_it == True):
        if(below_value == False):
            print("Sensor", header[col])
            print("Spike Indexes:",spike_indexes)
            print("Spike Values:", spike_values)
            return [spike_indexes,spike_values]
        elif(below_value == True):
            indexes_below = np.array([],dtype = int)
            values_below = np.array([])
            print("Sensor", header[col])
            for i in range(0,len(spike_indexes)-1):
                if(np.isnan(spike_values[i])==False and spike_values[i] <= objective):
                    indexes_below = np.append(indexes_below,i)
                    values_below =np.append(values_below,(spike_values[i]))
#                    print("(Spike Index, Spike Value) (",spike_indexes[i],",",spike_values[i],")") uncomment to print
            constraint01 = np.zeros((data_dimensions[0]))
            for i in range(0,len(indexes_below)): #loop through each index value and return an array of T/F was their a constraint broken
                constraint01[indexes_below[i]] = 1
            return(indexes_below,values_below,constraint01)

def detect_broken_constraints(constraint,col,minimum = False, minUFR = False): #constraint must be passed as a float, the col correpsonds to which sensor you are focused on
            indexes = np.array([],dtype = int)
            readings = np.array([])
            for i in range(0,data_dimensions[0]):
                value = data[i,col]
                if(minimum == True and minUFR == False):
                    if(np.isnan(value)==False and value <= constraint):
                        indexes = np.append(indexes,i)
                        readings =np.append(readings,value)
                if(minUFR == True):
                    solidscon = data[i,col+1]
                    min_ufr = Min_UFR(solidscon)
                    if(np.isnan(value)==False and min_ufr <=solidscon):
                        indexes = np.append(indexes,i)
                        readings =np.append(readings,value)                        
                else:
                    if(np.isnan(value)==False and value >= constraint):
                        indexes = np.append(indexes,i)
                        readings =np.append(readings,value)
            constraint01 = np.zeros((data_dimensions[0]))
            for i in range(0,len(indexes)): #loop through each index value and return an array of T/F was their a constraint broken
                constraint01[indexes[i]] = 1
            return(indexes,readings,constraint01)

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
                con_plt[j] = Min_UFR(solids_con[j])
                label_str = parameter_description[col] + " Constraint"
            plt.plot(t,con_plt,label = label_str)
        count +=1
        plt.xlabel("time (min)")
        plt.legend(loc = "best")
def convert_to_minutes(timeobject):
    days = float(timeobject.days)
    seconds = float(timeobject.seconds)
    return days*1440 + seconds/60
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

print("Data Cleaning and Analysis:\n")
print("Removed str inputs and changed to None")
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
"""
Section 2:
Objective: Clean the data so it is ready for modeling
"""
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
print("What is the best way to deal with this?")
#%%create a t-array that is in minutes setting the first point to time zero
data[0,0] = 0
for i in range(1,data_dimensions[0]):
    t_data = time_obj[i]-time_obj[0]
    data[i,0] = convert_to_minutes(t_data)

#%% Prove empty sensor arrays
print("\n Remove empty sensors")
testsensors = [20,21,25,26,27]
for i in range(0,len(testsensors)):
    for j in range(0, data_dimensions[0]):
        if(np.isnan(data[j,testsensors[i]]) == False):
            print("Not Empty", sensor_description[testsensors[i]])
            break
for i in range(0,len(testsensors)):
    print("Snesor", sensor_description[testsensors[i]]," is empty")

#get rid of the bad sensors and update other pertenant sensors; remember you can always refer back to data_raw
#The goal here is to format data so it outputs nicely for other people to use in modelling
datam = data[:,0:20]
data = np.column_stack((datam,data[:,22:25]))

sensor_descriptionm = sensor_description[0:20]
sensor_description = np.hstack((sensor_descriptionm,sensor_description[22:25]))

sensor_unitsm = sensor_units[0:20]
sensor_units = np.hstack((sensor_unitsm,sensor_units[22:25]))

parameterm = parameter[0:20]
parameter = np.hstack((parameterm,parameter[22:25]))

parameter_descriptionm = parameter_description[0:20]
parameter_description = np.hstack((parameter_descriptionm,parameter_description[22:25]))

timem = time[0:20]
time = np.hstack((timem,time[22:25]))

headerm = header[0:20]
header = np.hstack((headerm,header[22:25]))

data_dimensions = np.shape(data)
number_sensors = len(data)

#%%Conformation that the different floc variables are distinctly different
print("Test if Floc Setpoint and Floc Addition flow are within 5% of each other always")
percent_difference = 0.10
diff_index = []
diff_value = []
for i in range(3000,data_dimensions[0]):
    diff = np.abs(data[i,8]-data[i,9])
    if(diff>= data[i,8]*percent_difference):
        diff_index.append(i)
        diff_value.append(diff/data[i,8])
print("Number of times they are different:",len(diff_index))
print("Floc Setpoint and Floc Addition flow follow each other closely, are significantly different")
#%% Smooth out the lab data

smoothsensors = [4,5,6] #sensors to smooth out
splines = []
for i in range(0,len(smoothsensors)): #loop through each sensor
    col = smoothsensors[i]
    smooth_curve_p = np.array([data[0,col]])
    smooth_curve_t = np.array([0])
    for j in range(1,data_dimensions[0]): #loop through rows
        if(data[j,col] != data[j-1,col] and np.isnan(data[j,col])!=True): #make sure the data does not equal the previous and is not NaN
            smooth_curve_p = np.append(smooth_curve_p,data[j,col])
            smooth_curve_t = np.append(smooth_curve_t,j)
    cubic_spline = interp1d(smooth_curve_t,smooth_curve_p,kind="quadratic") #make a spline of the data
    splines.append(cubic_spline)
    
    

sensor4 = splines[0](data[:,0])
sensor5 = splines[1](data[:,0])
sensor6 = splines[2](data[:,0])
#store the splined sensor data 
for i in range(0,len(time_obj)):
    data[i,4] = sensor4[i]
    data[i,5] = sensor5[i]
    data[i,6] = sensor6[i]

for i in range(4,7):
    plotdata(time_obj[0],time_obj[200],i)
#%% select the pump that is on
pumps_max = np.empty(len(time_obj))
pumps_min = np.empty(len(time_obj))
count = 0
t = []
for i in range(0,len(time_obj)):
    pumps = [data[i,20],data[i,21]] #find which pump is on by finding the max value
    pumps_data = max(pumps)
    pumps_max[i] = max(pumps)
    pumps_min[i] = min(pumps)
    if(min(pumps)>1):
        t.append(i)
        count += 1
print("There are", count, " instances where the minimum pump speed was greater than 1.")
print("This occured between time indexes",min(t),",",max(t))

#%%
#update the data wil the new pump reading
for i in range(0,data_dimensions[0]):
    data[i,20] = pumps_max[i]
    data[i,21] = pumps_min[i]
sensor_description[20] = "Greater Pump Speed"
sensor_description[21] = "Lesser Pump Speed"
header[20] = "Greater Pump Speed"
header[21] = "Lesser Pump Speed"
#%%
#make arrays for where constraints were broken
pH_constraint = detect_broken_constraints(9.5,12)[2]
bed_pressure = detect_broken_constraints(19,15)[2]
rake_t = detect_broken_constraints(40,14)[2]
underflow_rate = detect_broken_constraints(0,18,minUFR = True)[2]
mill_trip_failure = detectspikes(col=1,std_from_mean = 0, below_value = True,objective = 50)[2]

#%%create files to export
header_out = "Time (min),Max pH Constraint Broken,Max Bed Pressure Broken,Max Torque Broken,Min Underflow Rate Broken,Mill Trip Failure"
header_out2 = "Time(min)'Flotation Circuit Feed (tons per hour),Con 2 Cycl Overflow 80 % passing Size,Con 2 Cycl O/F  % Passing 106 mic,Flotation Tails  - % Cu,Flotation Tails - % Fe,Flotation Tails -%Solid,TH602 Solids Feedrate,TH602 Flocculant Addition Flow PV,TH602 Floc Flow Setpoint,TH602 Floc Addition G/T Setpoint,Flocculant Addition Process Water Dilution,TH602 Tailings Thickener pH Cntrl PV,TH602 Tail Thickener Rake Height,TH602 Rake Torque Ctrl PV,TH602 Bed Pressure Ctrl PV,TH602 Bed Level Ctrl PV,TH602 Tails Thicknr Settling Rate Controller PV,PU664/665 Discharge Flow Ctrl PV,PU664/665 Discharge %Sol PV,Greater Pump Speed,Lesser Pump Speed,TH602 U/F Mass Calc CPV"
constraint_output = np.column_stack((data[:,0],pH_constraint,bed_pressure,rake_t,underflow_rate,mill_trip_failure))
np.savetxt("Broken_Constraints.csv",constraint_output,delimiter =",",header =header_out)
np.savetxt("Data_Cleaned.csv",data,delimiter = ",",header = header_out2)

#%%
"""
Old Code that can be used for reference on how to use the functions

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

find = target[50]
for i in range(0,500):
    if(real[i]==find):
        print("Find:",find,"index:50")
        print("Real:",real[i],"index:",i)
print("Complete")
#%%
plotdata(time_obj[2420],time_obj[2460],1)
subplotdata(9,3,1,28,0,500)
#%%
#test data is empty
import math
testsensors = [20,21,25,26,27]
for i in range(0,len(testsensors)):
    for j in range(0, data_dimensions[0]):
        if(math.isnan(data[j,testsensors[i]]) == False):
            print("Not Empty", sensor_description[testsensors[i]])
            break
print("Finished")
#%%
for i in range(0,data_dimensions[0]):
    if(data[i,10] != 19.0):
        print("Not always 19.0",data[i,10])
        break
    #%%
plotdata(time_obj[0],time_obj[500000],10)

#%%
from scipy.integrate import quad

t = np.linspace(0,2000,2001)
cu_percent = data[0:2001,4]
fe_percent = data[0:2001,5]
fl_percent = data[0:2001,6]

"""
#%%
