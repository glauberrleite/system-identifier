#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 12:51:20 2018

@author:glauberrleite
        lfelipev
"""

import numpy
import matplotlib.pyplot as pyplot
import matplotlib.patches as mpatches
import sys, getopt

def findTimeOnData(data, y):
    "Given a numpy array of time and respective output, locates the times where y1 and y2 are reached"
    t = data[-1, 0]

    # Finding t1 and t2 paying attention to step size
    for i in range(len(data)):
        if i == len(data) - 1:
            # There isn't a next value
            break
        
        if data[i, 1] <= y and data[i + 1, 1] > y:
            t = data[i, 0]
            break

    return t

def findInflectionPoint(data):
    "Given a numpy array of time and respective output, locates the inflection point and the derivative on it"
    m = 0
    x0 = data[0, 0]
    y0 = data[0, 1]
    y_min = data[-1,1]/3

    for i in range(len(data)):
        delta = abs((data[i, 1] - data[i + 1, 1]) / (data[i, 0] - data[i + 1, 0]))
        if delta < m and data[i, 1] > y_min:
            x0 = data[i, 0]
            y0 = data[i, 1]
            break
        m = delta
   
    print("Inflection: [" + str(x0) + ", " + str(y0) + "]")
    return [x0, y0, m]

def findTimeOnTangentLine(x0, y0, m, y):
    # Tangent line equation: (y - y0) = m * (x - x0)
    t = x0 + (y - y0) / m
    return t

# Plot the result of the chosen method
def plotResult(data, delay, tau):
    K_p = data[-1, 1] - data[0, 1]

    print "The Transfer Function is: "
    print str(K_p) + " * e^(-" + str(delay) + " * s)"
    print "-------------------"
    print "(" +str(tau) + " * s + 1)"

    tf = r"$"+ "{:.2f}".format(K_p)  +" * \frac{1}{"+ "{:.2f}".format(tau)  +"s + 1} * e^{-"+ "{:.2f}".format(delay) +"s}$"
    
    estimative = numpy.zeros(len(data[:,0]))

    for i in range(len(data[:,0])):
        if data[i, 0] <= delay:
            estimative[i] = 0
        else:
            estimative[i] = (1 - numpy.exp(-(data[i, 0] - delay)/tau)) * K_p
    
    pyplot.plot(data[:, 0], data[:, 1], 'b', data[:, 0], estimative, 'r')
    pyplot.xlabel("Time (seconds)")
    pyplot.title("Comparison")
    pyplot.text(1, .025, tf)
    legend = mpatches.Patch(color='red', label='Estimative')
    legend2 = mpatches.Patch(color='blue', label='Data')
    pyplot.legend(handles=[legend, legend2], loc=4)
    pyplot.show()

# Ziegler-Nichols
def zieglerNichols(data):
    y_r = data[-1, 1]
    [x0, y0, m] = findInflectionPoint(data)    

    y1 = data[0, 1]
    y2 = y_r
    t1 = findTimeOnTangentLine(x0, y0, m, y1)
    t2 = findTimeOnTangentLine(x0, y0, m, y2)

    delay = t1
    tau = t2 - t1
    plotResult(data, delay, tau)
    
# Hagglund
def hagglund(data):
    y_r = data[-1,1]
    [x0, y0, m] = findInflectionPoint(data)
    
    y1 = 0
    y2 = 0.632 * y_r
    t1 = findTimeOnTangentLine(x0, y0, m, y1)
    t2 = findTimeOnTangentLine(x0, y0, m, y2)

    delay = t1
    tau = t2 - t1
    plotResult(data, delay, tau)
    
# Smith
def smith(data):
    y_r = data[-1,1]
    y1 = 0.283 * y_r
    y2 = 0.632 * y_r
    
    t1 = findTimeOnData(data, y1)
    t2 = findTimeOnData(data, y2)

    tau = 1.5 * (t2 - t1)
    delay = 1.5 * t1 - 0.5 * t2
    plotResult(data, delay, tau)

# Sundaresan-Krishnaswamy
def sundaresanKrishnaswamy(data):
    y_r = data[-1,1]
    y1 = 0.353 * y_r
    y2 = 0.853 * y_r
    
    t1 = findTimeOnData(data, y1)
    t2 = findTimeOnData(data, y2)

    tau = 0.67 * (t2 - t1)
    delay = 1.3 * t1 - 0.29 * t2
    plotResult(data, delay, tau)

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
def switch(opt, data):
    switcher = {
        1: zieglerNichols,
        2: hagglund,
        3: smith,
        4: sundaresanKrishnaswamy,
        5: mollenkamp
    }
    chosenMethod = switcher.get(opt, invalidOption)
    return chosenMethod(data)

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

    # Applying mean fitting
    #if meanFit:
        
    
    # Menu
    print("-------------------")
    print("Choose an Identification Method:")
    print("1 - Ziegler-Nichols")
    print("2 - Hagglund")
    print("3 - Smith")
    print("4 - Sundaresan-Krishnaswamy")
    print("5 - Mollenkamp")
    opt = input("Method: ")
    switch(opt, data)

if __name__ == "__main__":
    main(sys.argv[1:])
