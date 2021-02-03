This repository includes my work for the Thickener Project

Analysis of Thickener Data Requires two files to work: 
Sensor_Names.csv  *found in this repository
train.csv  *you can find that in Sam's dropbox (the file is too big)

***********
Analysis of Thickener Data

Outputs Broken_Constraints.csv: a file with the time index and if a constraint was broken (0 being false 1 being true)

Cleaned Data Makes the following modifications:

-Time is converted into minutes with the first point being time 0.
-Sensors PU664 Motor Current, PU665 Motor Current, Sensor PU664/665 Disch Proces Water Addition Valve
Position, Sensor PU664 Suct Process Water Addition Valve Position were all empty data sets and removed
-"No Data" and "Bad Input" were converted to "NaN"
-Flotation Tails -%Cu, % Fe, % Solid data was smoothed
-Pumps were switched into two arrays, the maximum pump speed and min pump speed (for the majority of the time either one is on and the other one is off)

The following observations were made:
1) Number of Times time interval is not 1 min
Not Equal time interval of 1 minute
time interval: -1 day, 23:01:00
Index Location for time_obj array 5939 

Not Equal time interval of 1 minute
time interval: 1:01:00
Index Location for time_obj array 268019 

Not Equal time interval of 1 minute
time interval: -1 day, 23:01:00
Index Location for time_obj array 530099 

Total Number Bad Time Intervals: 3 

2)Test if Floc Setpoint and Floc Addition flow are within 5% of each other always
Number of times they are different: 42140/530000
Floc Setpoint and Floc Addition flow follow each other closely, but are significantly different
***********
There are some functions that might be helpful for analyzing the data in future projects

plotdata: this will plot a graph of a specified sensor
time_start:   time_obj[index]
time_end:     time_obj[index]   **The indexes go up by minutes and the timestamps are created in the program
col:          column from excel file in train.csv you want to graph (1 through 28)

The function returns the sensor values from the excel file

plothist: this will plot a histogram of a specified sensor:
time_start:   time_obj[index]
time_end:     time_obj[index]   **The indexes go up by minutes and the timestamps are created in the program
col:          column from excel file in train.csv you want to graph (1 through 28)

The function returns the sensor values from the excel file

detectspikes: This will return the index values and sensor readings of unusually high/low values
dataset:      an array outputted from plotdata (you can turn off plotting by setting plot = False)
std_from_mean:number of standard deviations from the mean to pick up
col:          The sensor column from the excel file you want to read

subplotdata: This will create a subplot of multiple sensors
rows:         number of rows in subplot
col:          number of col in subplot
sensor_start: start index of sensors (1 through 28)
sensor_finish:end index of sensors (1 thorugh 28)
time_start:   this is an index (ideally you will find the index from detectspikes)
time_end:     this is the end index (ideally you will find the index from detect spikes)

