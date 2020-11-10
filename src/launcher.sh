#!/bin/sh
# arduino logger script. 

# first arg is project root 

if [ -z "$1" ]
then 
    echo "missing project root"
    return 1
fi

PROJECT_ROOT=$1
LOGFILE="${PROJECT_ROOT}/logs/$(date +%Y_%m_%d).log"

# uncomment if airquality.ino is not already loaded onto the arduino - rPi uses
# an old compiler that doesn't work with this sketch, because reasons
# arduino --upload ${PROJECT_ROOT}/src/airquality/airquality.ino

# Calculating the recorded time from here does rely on the arduino being on 
# time and in sync - we'll see if this is a bad idea.
echo "#TIMESTAMP=$(date +_%H_%M_%S)" >> $LOGFILE
cu -l /dev/ttyACM0 -s 9600 >> $LOGFILE
