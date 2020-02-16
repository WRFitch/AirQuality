#!/bin/sh
# launcher.sh 
# 
# first arg is project root 

if [ -z "$1" ]
then 
    echo "missing project root"
    return 1
fi

PROJECT_ROOT=$1

arduino --upload ${PROJECT_ROOT}/src/airquality/airquality.ino
cu -l /dev/ttyACM0 -s 9600 >> "${PROJECT_ROOT}/logs/$(date +%Y_%m_%d).log"
