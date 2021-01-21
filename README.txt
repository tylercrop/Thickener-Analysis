This repository includes my work for the Thickener Project

Analysis of Thickener Data Requires two files to work: 
Sensor_Names.csv  *found in this repository
train.csv  *you can find that in Sam's dropbox (the file is too big)

***********
Analysis of Thickener Data

There are some functions that might be helpful

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

