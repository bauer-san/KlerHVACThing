import os
import time
import sys
import Adafruit_DHT

#load our drivers:
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# The next step is to define our sensor?s output file (the w1_slave file).
# Remember to utilise your own temperature sensor?s serial code!

MySensors = {'sys/bus/w1/devices/3b-############/w1_slave', \
             'sys/bus/w1/devices/3b-############/w1_slave', \
             'sys/bus/w1/devices/3b-############/w1_slave'
            }

def temp_raw():

    f = open(temp_sensor, 'r')
    lines = f.readlines()
    f.close()
    return lines

# First, we check our variable from the previous function for any errors. If you
# study our original output as defined in the terminal example, we get two lines
# of code (Line 0 = 72 01 4b 46 7f ff 0e 10 57 : crc=57 YES); we strip this line
# except for the last three digits, and check for the ?YES? signal, indicating a
# successful temperature reading from the sensor. In Python, not-equal is defined
# as ?!=?, so here we?re saying whilst the reading does not equal YES, sleep for
# 0.2s and repeat.
def read_temp():

    lines = temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = temp_raw()

# Once the program is happy that the YES signal has been received, we proceed
# to our second line of output code (Line 1 = 72 01 4b 46 7f ff 0e 10 57 t=23125).
# We find our temperature output ?t=?, check it for errors, strip the output of
# the ?t=? phrase to leave just the temperature numbers, and run two
# calculations to give us the figures in Celsius and Fahrenheit.

    temp_output = lines[1].find('t=')

    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f

def read_AM2302():
    # read_retry method which will retry up to 15 times to get a sensor
    # reading (waiting 2 seconds between each retry).
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, pin)
    temperature = temperature * 9/5.0 + 32
    return temperature, humidity

#Main loop
while True:
        for temp_sensor in MySensors:
            print(temp_sensor, read_temp())
        print(read_AM2302())
        time.sleep(1)