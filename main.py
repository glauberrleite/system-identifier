#!/usr/bin/python3

# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 12:51:20 2018

@author:glauberrleite
        lfelipev
"""

from FirstOrderMethods import *
from SecondOrderMethods import *
from ClosedLoopMethods import *
from LeastSquares import *

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

# Smith2
def smith2(data):
    method = Smith2(data)
    return method

# Yuwana-Seborg
def yuwanaSeborg(data):
    method = YuwanaSeborg(data)
    return method

# Least Squares
def leastSquares(data):
    # Assuming step input
    inputArray = numpy.ones(len(data))

    # Defining parameters
    orderOutput = int(input("Select output order: "))
    orderInput = int(input("Select input order: "))
    orderError = int(input("Select error order: "))

    # Making an instance of LeastSquares
    method = LeastSquares(data[:, 1], inputArray, None, orderOutput, orderInput, orderError)

    return method

# Invalid option
def invalidOption(data):
    print("Invalid option")
    main(sys.argv[1:])

# Switch options
def switch(opt, data):
    switcher = {
        1: zieglerNichols,
        2: hagglund,
        3: smith,
        4: sundaresanKrishnaswamy,
        5: mollenkamp,
        6: smith2,
        7: yuwanaSeborg,
        8: leastSquares
    }

    chosenClass = switcher.get(opt, invalidOption)
    method = chosenClass(data)    
    return method
                                
def main(argv):
    print("-------------------")
    print("System identifier")
    print("-------------------")
   
    version = 2.0
    # Treating arguments
    dataFile = ""
    skipRows = 0
    fitting = False
    fitDegree = 2
    medianFitting = False
    medianFittingStep = 3
    saveEstimative = False
    estimativeFile = "outputEstimative.txt"
    savePerformance = False
    performanceFile = "outputPerformance.txt"
    
    if (argv[0] in ["-h", "--version"]) == False:
        dataFile = argv[0]
        argv.pop(0)

    opts, args = getopt.getopt(argv, "hs:", ["skip-rows=", "curve-fitting=", "version", "median-fitting=", "save-estimative=", "save-performance="])

    for opt, arg in opts:
        if opt == "-h":
            print("Usage:")
            print("main.py <dataFile> --skip-rows=<skip-rows> --curve-fitting=<degree> --median-fitting=<step-size> --save-estimative=<filename> --save-performance=<filename>")
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
        elif opt == "--save-estimative":
            saveEstimative = True
            estimativeFile = arg
        elif opt == "--save-performance":
            savePerformance = True
            performanceFile = arg


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
    print("6 - Smith2")
    print("7 - Yuwana-Seborg")
    print("8 - Least Squares")
    opt = int(input("Method: "))
    
    print("-------------------")
    method = switch(int(opt), data)

    print("-------------------")
    method.showResults()

    # Calculating and printing performance measures
    mse = Util.mse(data, method.estimative)
    iae = Util.iae(data, method.estimative)
    ise = Util.ise(data, method.estimative)
    itae = Util.itae(data, method.estimative)
    print("-------------------")
    print("Performance Measures")
    print("-------------------")
    print("MSE: "+ str(Util.mse(data, method.estimative)))    
    print("IAE: " + str(Util.iae(data, method.estimative)))
    print("ISE: " + str(Util.ise(data, method.estimative)))
    print("ITAE: "+ str(Util.itae(data, method.estimative)))

    if saveEstimative:
        numpy.savetxt(estimativeFile, method.estimative)

    if savePerformance:
        with open(performanceFile, "w") as eFile: 
            eFile.write("MSE: " + str(mse) + "\n")
            eFile.write("IAE: " + str(iae) + "\n")
            eFile.write("ISE: " + str(ise) + "\n")
            eFile.write("ITAE: " + str(itae) + "\n")

    plot(data, method.estimative)

if __name__ == "__main__":
    main(sys.argv[1:])
