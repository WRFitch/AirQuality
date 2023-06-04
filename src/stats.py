#!/usr/bin/python3 

"""
python stats script to look through logs and graph results. 

TODO put the metadata and matrix in an object, you clown. Also make the matrix
an actual matrix.
TODO fix whatever is making matplotlib take so long. Maybe it's the thousands and thousands of timestamps it has to manage? 
"""

from datetime import datetime, timedelta
import numpy as np 
import os
import matplotlib
from matplotlib import pyplot as pyplot
import sys
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

def graph(measurements):
    VOC = []
    CO2 = [] 
    H2 = []
    ethanol = [] 
    time = []  
    date = []
    # TODO simplify 
    for line in measurements[1:]:
        VOC.append(float(line[0]))
        CO2.append(float(line[1]))
        H2.append(float(line[2]))
        ethanol.append(float(line[3]))
        date.append(line[4])
        time.append(line[5])

    _, axs = pyplot.subplots(4)
    axs[0].plot(time, VOC)
    axs[1].plot(time, CO2)
    axs[2].plot(time, H2)
    axs[3].plot(time, ethanol)
    pyplot.show()

# gets this rough logfile and presents it in a clean 2d list
def get_data_from_file(logfile):
    print("getting data from " + logfile)
    # first row is metadata - [timestamp, step value]. This should be extracted into a separate list in a class. 
    datestamp = logfile[-14:-4]
    data = [[]]

    with open(logfile, "r") as log:
        for logline in log:
            line = logline.rstrip()
            #check line matches standard numeric format 
            if line.replace(" ", "").replace(".", "").isnumeric():
                #calculate timestamp - this doesn't work if there's any number of broken steps. 
                timestamp += timedelta(seconds = repeat_interval)
                line += " " + str(timestamp)
                data.append(line.split(" "))
                continue

            #get metadata where available
            if line[1:11] == "TIMESTAMP=": 
                timestamp = datetime(year = int(datestamp[0:4]), \
                    month = int(datestamp[5:7]), day = int(datestamp[8:10]), \
                    hour = int(line[12:14]), minute = int(line[15:17]), \
                    second = int(line[18:20]))
                data[0].append(timestamp)
            elif line[1:6] == "STEP=": 
                repeat_interval = int(line[6:])
                data[0].append(repeat_interval)
            elif "Measurement failed" in line:
                # error messages are posted once a second - update timestamp to be sure. 
                timestamp += timedelta(seconds = 1)
    return data

# get average greenhouse gas data for that logfile, preserving metadata header
# there has to be a better way of doing this. 
def get_avg_measurements(logfile):
    avgs = [logfile[0]]
    for line in logfile[1:]:
        #don't append the time value
        avgs.append(line[:-1])
    for val in avgs[1]:
        val = val / len(logfile)-1
    return avgs

#monitor logfile for changes
def tail(logfile):
    os.system("tail -n +0 -f " + logfile)

def main(args):
    if 'today' in args:
        graph(get_data_from_file(logfile_today))
    elif 'tail' in args:
        tail(logfile_today)
    elif 'day' in args:
        day = args[2]
        graph(get_data_from_file(format_date(day)))
    elif 'all' in args:
        avg_list = []
        for file in os.listdir(logdir):
            avg_list.append(get_avg_measurements(get_data_from_file(logdir + file)))
        #graph(avg_list)
    else:
        print_help()

def print_help():
    print("""args:
tail - tail today's results
today - graph today's results
day - graph a given date's results (given in the format YYYY_MM_DD)
all - graph average daily results""")

def format_date(date):
    return logdir + date + ".log"

logdir = "/src/AirQuality/logs/"
logfile_today = format_date(os.popen("date +%Y_%m_%d").read()).replace("\n", "")
main(sys.argv)
