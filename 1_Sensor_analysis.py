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


app = QtGui.QApplication([])

win = pg.GraphicsWindow(title="Basic plotting examples")
win.resize(1000, 600)
win.setWindowTitle('Sensor analysis')

pg.setConfigOptions(antialias=True)

p1 = win.addPlot(title="Raw Decay Signal")
p2 = win.addPlot(title="Logarithm of decay signal with linear fit")

win.nextRow()


p3 = win.addPlot(title="Calculated decay times")

p6 = win.addPlot(title="Updating plot")


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

    import sys

    ser = connect_Serial()

    for k in xrange(1, 300):

        try:
            data = ser.readline().decode('utf-8')[:-2]

            while data != "NewDataSet":

                data = ser.readline().decode('utf-8')[:-2]
            filename = "test" + str(k) + ".csv"

            names, values = read_dataset(ser, filename)

            # test_set = {
            #     "file": filename,
            #     "header": "T",
            #     "data": values,
            #     "names": names
            # }

            # csvExp.csvExport(test_set)

            p1.plot(values[0], values[1], clear=True)
            pg.QtGui.QApplication.processEvents()

            print "ok"

        except Exception, e:
            print "fail"
