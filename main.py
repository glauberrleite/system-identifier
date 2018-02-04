# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 12:51:20 2018

@author:glauberrleite
        lfelipev
"""

import numpy
import matplotlib.pyplot as pyplot

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

    for i in range(len(data)):
        delta = abs((data[i, 1] - data[i + 1, 1]) / (data[i, 0] - data[i + 1, 0]))
        if delta < m:
            x0 = data[i, 0]
            y0 = data[i, 1]
            break
        m = delta
    
    return [x0, y0, m]

def findTimeOnTangentLine(x0, y0, m, y):
    # Tangent line equation: (y - y0) = m * (x - x0)
    t = x0 + (y - y0) / m
    return t

# Plot the result of the chosen method
def plotResult(y1, y2, delay, tau, data):
    K_p = y2 - y1

    print "The Transfer Function is: "
    print str(K_p) + " * e^(-" + str(delay) + " * s)"
    print "-------------------"
    print "(" +str(tau) + " * s + 1)"

    tf = r"$Kp * \frac{1}{Ts + 1} * e^{-delays}$"

    estimative = (1 - numpy.exp(-(data[:,0] - delay)/tau)) * K_p
    
    pyplot.plot(data[:, 0], data[:, 1], 'b', data[:, 0], estimative, 'r')
    pyplot.xlabel("Time (seconds)")
    pyplot.title("Comparison")
    pyplot.text(60, .025, tf)
    pyplot.show()

# Ziegler-Nichols
def zieglerNichols(data):
    y_r = data[-1, 1]
    [x0, y0, m] = findInflectionPoint(data)    

    y1 = 0
    y2 = y_r
    t1 = findTimeOnTangentLine(x0, y0, m, y1)
    t2 = findTimeOnTangentLine(x0, y0, m, y2)

    delay = t1
    tau = t2 - t1
    plotResult(y1,y2, delay, tau, data)
    
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
    plotResult(y1, y2, delay, tau, data)
    
# Smith
def smith(data):
    y_r = data[-1,1]
    y1 = 0.283 * y_r
    y2 = 0.632 * y_r
    
    t1 = findTimeOnData(data, y1)
    t2 = findTimeOnData(data, y2)

    tau = 1.5 * (t2 - t1)
    delay = 1.5 * t1 - 0.5 * t2
    plotResult(y1, y2, delay, tau, data)

# Sundaresan-Krishnaswamy
def sundaresanKrishnaswamy(data):
    y_r = data[-1,1]
    y1 = 0.353 * y_r
    y2 = 0.853 * y_r
    
    t1 = findTimeOnData(data, y1)
    t2 = findTimeOnData(data, y2)

    tau = 0.67 * (t2 - t1)
    delay = 1.3 * t1 - 0.29 * t2
    plotResult(y1, y2, delay, tau, data)

# Invalid option
def invalidOption(data)
    print("Invalid option")
    main()

# Switch options
def switch(opt, data):
    switcher = {
        1: zieglerNichols,
        2: hagglund,
        3: smith,
        4: sundaresanKrishnaswamy
    }
    chosenMethod = switcher.get(opt, invalidOption)
    return chosenMethod(data)

def main():
    print "System identifier"

    print "Loading data"
    data = numpy.loadtxt("values.data", skiprows=1)
    print "Data loaded"
    
    print "Choose an Identification Method:"
    print "1 - Ziegler-Nichols"
    print "2 - Hagglund"
    print "3 - Smith"
    print "4 - Sundaresan-Krishnaswamy"
    opt = input("Method: ")
    switch(opt, data)

if __name__ == "__main__":
    main()
