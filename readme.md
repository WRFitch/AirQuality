# AirQuality

An arduino project to measure & log air quality. Runs on a cron job on a battery-powered Raspberry Pi. There's a number of factors not taken into account here, such as sensor calibration, temperature and humidity, but this project only exists to satisfy my curiosity.

## Physical Setup
1. Buy an Arduino Uno, an Adafruit SGP30 Air Sensor, and some cables. Assemble whatever needs assembling. 
1. Connect the ports on the SGP30 to the corresponding ports on the Arduino. The only differences are 1V8, which doesn't need to connect to anything, and VIN, which connects to the 5V arduino output. 
1. Connect your arduino to a linux pc and run the code in this repo
1. Notice that there's an uncomfortably high volume of CO2 everywhere, because we live in a cyberpunk hellscape these days.

[there's a marginally more detailed writeup here](https://willfitch.com/projects/arduino_air_sensor.html) 
