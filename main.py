#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 12:51:20 2018

@author:glauberrleite
        lfelipev
"""

from FirstOrderMethods import *

import numpy
import matplotlib.pyplot as pyplot
import sys, getopt

# Ziegler-Nichols
def zieglerNichols(data):
    method = ZieglerNichols(data)
    return method

# Hagglund
def hagglund(data):
    method = Hagglund(data)
    return method

# Smith
def smith(data):
    method = Smith(data)
    return method

# Sundaresan-Krishnaswamy
def sundaresanKrishnaswamy(data):
    method = SundaresanKrishnaswamy(data)
    return method

# Mollenkamp
def mollenkamp(data):
    y_r = data[-1, 1]
    y1 = 0.15 * y_r
    y2 = 0.45 * y_r
    y3 = 0.75 * y_r

    t1 = findTimeOnData(data, y1)
    t2 = findTimeOnData(data, y2)
    t3 = findTimeOnData(data, y3)

    x = (t2 - t1)/(t3 - t1)
    zeta = (0.0805 - (5.547 * ((0.475 - x) ** 2))) / (x - 0.356)

    f2 = 0
    if (zeta < 1):
        f2 = 0.708 * (2.811 ** zeta)
    else:
        f2 = 2.6 * zeta - 0.6

    w_n = f2 / (t3 - t1)

    f3 = 0.922 * (1.66 ** zeta)

    delay = t2 - f3/w_n

    tau1 = tau2 = 0

    estimative = None

    if (zeta >= 1):
        tau1 = (zeta + numpy.sqrt((zeta**2) - 1))/w_n
        tau2 = (zeta - numpy.sqrt((zeta**2) - 1))/w_n
        
    beta = numpy.sqrt(1 - (zeta ** 2))
    phi = numpy.arctan(zeta/beta)

    estimative = 1 - (1 / beta) * numpy.exp(-zeta * w_n * data[:, 0]) * numpy.cos(w_n * beta * data[:, 0] - phi)

    pyplot.plot(data[:,0], data[:,1], 'b', data[:,1], estimative, 'r')
    pyplot.show()

# Invalid option
def invalidOption(data):
    print("Invalid option")
    main()

# Switch options
def switch2(opt, data):
    switcher = {
        1: zieglerNichols,
        2: hagglund,
        3: smith,
        4: sundaresanKrishnaswamy,
        5: mollenkamp
    }
    chosenClass = switcher.get(opt, invalidOption)
    method = chosenClass(data)    
    return method
    

def main(argv):
    print("-------------------")
    print("System identifier")
    print("-------------------")
   
    version = 1.0
    # Treating arguments
    dataFile = ""
    skipRows = 0
    fitting = False
    fitDegree = 2
    
    if (argv[0] in ["-h", "--version"]) == False:
        dataFile = argv[0]
        argv.pop(0)

    opts, args = getopt.getopt(argv, "hs:", ["skip-rows=", "curve-fitting=", "version", "meanfit"])

    for opt, arg in opts:
        if opt == "-h":
            print("Usage:")
            print("main.py <dataFile> --skip-rows=<skip-rows> --curve-fitting=<degree> --mean-fit")
            print("main.py -h")
            print("main.py --version")
            sys.exit(0)
        elif opt in ("-s", "--skip-rows"):
            skipRows = int(arg)
        elif opt == "--curve-fitting":
            fitting = True
            fitDegree = int(arg)
        elif opt == "--version":
            print("System Identifier v" + str(version))
            sys.exit(0)
        elif opt == "--mean-fit":
            meanFit = True

    # Loading data
    print("Loading data")
    data = numpy.loadtxt(dataFile, skiprows=skipRows)
    print("Data loaded")

    # Applying curve fitting if it's set
    if fitting:
        print("Using " + str(fitDegree) + " degrees curve fitting")
        coefficients = numpy.polyfit(data[:, 0], data[:, 1], fitDegree)
        pol = numpy.poly1d(coefficients)

        for i in range(len(data[:, 1])):
            data[i, 1] = pol(data[i, 0])

    
    # Menu
    print("-------------------")
    print("Choose an Identification Method:")
    print("1 - Ziegler-Nichols")
    print("2 - Hagglund")
    print("3 - Smith")
    print("4 - Sundaresan-Krishnaswamy")
    print("5 - Mollenkamp")
    opt = input("Method: ")
    
    method = None
    method = switch2(opt, data)
    method.plot()
    

    # Printing performance measures
    print("-------------------")
    print("MSE: "+ str(Util.mse(data, method.estimative)))    
    print("IAE: " + str(Util.iae(data, method.estimative)))
    print("ISE: " + str(Util.ise(data, method.estimative)))
    print("ITAE: "+ str(Util.itae(data, method.estimative)))

if __name__ == "__main__":
    main(sys.argv[1:])
