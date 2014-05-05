# reads serial and plots all transmitted values which are separated by a " " in a dynamic plot
# on demand saves the values in a csv file

import matplotlib.pylab as plt
import numpy as np
import csv
from matplotlib import rcParams
from collections import deque
from types import *
rcParams.update({'figure.autolayout': True})
import pyqtgraph as pg

import sys
sys.path.append("/Volumes/Daten/ds_Admin_Andreas/Studium/Vorlagen/Phyton")


import argument_parser as argpars
import csvImport as csvImp
import csvExport as csvExp
import my_plot as plot
from Qt_example_python import Window
from PyQt4 import QtGui


import serial
import time
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg

# This class should plot all serial


def connect_Serial():

    ser = serial.Serial(port='/dev/tty.usbserial-A603H9E1', baudrate=115200)

    print ser.isOpen()

    print("connected to: " + ser.portstr)

    return ser


def read_dataset(ser, filename):
# This function reads comma separated datasets from the serial port and
# returns the names of the variales and their values in a list.

    data = ser.readline().decode('utf-8')[:-2]

    names = data.split(",")
    values = []
    # build the right data structures
    for i in xrange(0, len(names)):
        values.append([])

    data = ser.readline().decode('utf-8')[:-2]

    while (data != "EndDataSet"):

        for j in xrange(0, len(values)):
            values[j].append(float(data.split(",")[j]))

        data = ser.readline().decode('utf-8')[:-2]

    return names, values


if __name__ == '__main__':

    ser = connect_Serial()

    for k in xrange(1, 10):

        try:
            data = ser.readline().decode('utf-8')[:-2]

            while data != "NewDataSet":

                data = ser.readline().decode('utf-8')[:-2]
            filename = "test" + str(k) + ".csv"

            names, values = read_dataset(ser, filename)

            test_set = {
                "file": filename,
                "header": "T",
                "data": values,
                "names": names
            }

            csvExp.csvExport(test_set)
            win.addPlot(values[0], values[1], row=0, col=0)

            print "ok"

        except Exception, e:
            print "fail"











# Here you have to verify, whether the data has been fully received.
