#!/usr/bin/python -tt
#
# $Id$

'''
This script requires that you are connected to a badgelet
with a serial cable.  It will repetively run the showBattery command
until 'count' iterations writing results to an optional logfile
'''

import time, datetime
import serial
import sys
from optparse import OptionParser

def main():
    # Use optparse for all of the command line arguments
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-p", "--port", dest="port", type="str",
                    help="Serial port to use", metavar="PORT")
    parser.add_option("-l", "--lfile", dest="logfile", type="str",
                    help="Output file for logging results", metavar="LOGFILE")
    parser.add_option("-c", "--count", dest="count", type="int", default=10,
                    help="stop after count iterations (default=%default)", metavar="COUNT")

    (options, args) = parser.parse_args()

    # If the script is executed with no arguments, then print the help and exit
    # Seems like a hack, I could not figure out how to do this using optparse
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

##### Put your code in here #######

    # Open the files
    if isinstance(options.logfile, str):
        log_file = open(options.logfile, 'w')

    # configure the serial connections (the parameters differs on the device you are connecting to)
    ser = serial.Serial(
        port = options.port,
        baudrate=115200)
#        parity=serial.PARITY_ODD,
#        stopbits=serial.STOPBITS_TWO,
#        bytesize=serial.SEVENBITS

    ser.isOpen()

    for i in range(1, options.count+1):
        # send the command to the device
        # (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
        ser.write('showBattery\r\n')
        out = ''
        # let's wait one second before reading output (let's give device time to answer)
        time.sleep(1)
        print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), 'Iteration:', i
        while ser.inWaiting() > 0:
            out += ser.read(1)
        if out != '':
            print ">>" + out
            if isinstance(options.logfile, str):
                log_file.write( datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + ' Iteration: ' + str(i) + '\n' )
                log_file.write( ">>" + out )
            
    # Close files
    if isinstance(options.logfile, str):
        log_file.close()

    # Close the serial port
    ser.close()

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
