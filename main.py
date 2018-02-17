#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 12:51:20 2018

@author:glauberrleite
        lfelipev
"""

from FirstOrderMethods import *
from SecondOrderMethods import *

import numpy
import matplotlib.pyplot as pyplot
import matplotlib.patches as mpatches
import sys, getopt

def plot(data, estimative):
    pyplot.plot(data[:, 0], data[:, 1], 'b')
    pyplot.plot(data[:, 0], estimative, 'r')
    pyplot.xlabel("Time (seconds)")
    pyplot.title("Comparison")
    legend = mpatches.Patch(color='red', label='Estimative')
    legend2 = mpatches.Patch(color='blue', label='Data')
    pyplot.legend(handles=[legend, legend2], loc=4)
    pyplot.show()


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
    method = Mollenkamp(data)
    return method

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
    medianFitting = False
    medianFittingStep = 3
    
    if (argv[0] in ["-h", "--version"]) == False:
        dataFile = argv[0]
        argv.pop(0)

    opts, args = getopt.getopt(argv, "hs:", ["skip-rows=", "curve-fitting=", "version", "median-fitting="])

    for opt, arg in opts:
        if opt == "-h":
            print("Usage:")
            print("main.py <dataFile> --skip-rows=<skip-rows> --curve-fitting=<degree> --median-fitting=<step-size>")
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
        elif opt == "--median-fitting":
            medianFitting = True
            medianFittingStep = int(arg) 

    # Loading data
    print("Loading data")
    data = numpy.loadtxt(dataFile, skiprows=skipRows)
    print("Data loaded")

    # Applying curve fitting if it's set
    if fitting:
        print("Using " + str(fitDegree) + " degrees curve fitting")
        coefficients = numpy.polyfit(data[:, 0], data[:, 1], fitDegree)
        pol = numpy.poly1d(coefficients)

        for i in range(len(data)):
            data[i, 1] = pol(data[i, 0])

    # Applying median fitting
    if medianFitting:
        print("Using median fitting with " + str(medianFittingStep) + " step size")
        newData = numpy.zeros((len(data)/medianFittingStep, 2))

        aux = numpy.zeros((medianFittingStep, 2))

        for i in range(len(data)):
                aux[i % medianFittingStep] = data[i]
                if (i % medianFittingStep) == medianFittingStep - 1:
                    index = i/medianFittingStep
                    newData[index, 0] = numpy.median(aux[:, 0])
                    newData[index, 1] = numpy.median(aux[:, 1])

        data = newData

    
    # Menu
    print("-------------------")
    print("Choose an Identification Method:")
    print("1 - Ziegler-Nichols")
    print("2 - Hagglund")
    print("3 - Smith")
    print("4 - Sundaresan-Krishnaswamy")
    print("5 - Mollenkamp")
    opt = input("Method: ")
    
    print("-------------------")
    method = None
    method = switch2(opt, data)
    
    method.showTransferFunction()

    plot(data, method.estimative)
    

    # Printing performance measures
    print("-------------------")
    print("MSE: "+ str(Util.mse(data, method.estimative)))    
    print("IAE: " + str(Util.iae(data, method.estimative)))
    print("ISE: " + str(Util.ise(data, method.estimative)))
    print("ITAE: "+ str(Util.itae(data, method.estimative)))

if __name__ == "__main__":
    main(sys.argv[1:])
