#!/usr/bin/python3 

"""
python stats script to look through logs and graph results. 

TODO put the metadata and matrix in an object, you clown. Also make the matrix
an actual matrix.
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
    #AAAAAAAAAA
    # TODO this is garbage - put it in a numpy matrix or something. I miss real arrays. 
    VOC = [float(item[0]) for item in measurements[1:]]
    CO2 = [float(item[1]) for item in measurements[1:]]
    H2 = [float(item[2]) for item in measurements[1:]]
    ethanol = [float(item[3]) for item in measurements[1:]]
    date = [item[4] for item in measurements[1:]]
    time = [item[5] for item in measurements[1:]]

    _, axs = pyplot.subplots(4)
    axs[0].plot(time, VOC)
    axs[1].plot(time, CO2)
    axs[2].plot(time, H2)
    axs[3].plot(time, ethanol)
    pyplot.show()

#gets this rough logfile and presents it in a nice clean 2d list
def get_data_from_file(logfile):
    print("getting data from " + logfile)
    log = open(logfile, "r")

    #first row is metadata - [date, timestamp, step value]
    date = logfile[-14:-4]
    data = [[date]]

    # TODO refactor, this is nasty
    while True:
        line = log.readline().replace("\n", "")
        if not line: break
        #ignore useless lines. onnected matches Disconnected and Connected. 
        if line.find("#") != -1 or line.find("onnected") != -1:
            #get metadata 
            if line[1:11] == "TIMESTAMP=": 
                #fuck timestamps. this is why we can't have nice things. 
                timestamp = datetime(year = int(date[0:4]), month = \
                        int(date[5:7]), day = int(date[8:10]), \
                        hour = int(line[12:14]), minute = int(line[15:17]), \
                        second = int(line[18:20]))
                data[0].append(timestamp)
            if line[1:6] == "STEP=": 
                repeat_interval = int(line[6:])
                data[0].append(repeat_interval)
            continue

        #calculate timestamp - this doesn't work if there's any number of broken steps. 
        timestamp += timedelta(seconds = repeat_interval)
        line += " " + str(timestamp)
        data.append(line.split(" "))
    return data

#get average greenhouse gas data for that logfile, preserving metadata header
#there has to be a better way of doing this. 
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

#still using separate print methods for lines? come on
def print_help():
    print("args:\n")
    print("tail - tail today's results\n")
    print("today - graph today's results\n")
    print("day - graph a given date's results (given in the format YYYY_MM_DD)\n")
    print("all - graph average daily results\n")

def format_date(date):
    return logdir + date + ".log"

logdir = "/src/AirQuality/logs/"
logfile_today = format_date(os.popen("date +%Y_%m_%d").read()).replace("\n", "")
main(sys.argv)
