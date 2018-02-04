import numpy
import matplotlib.pyplot as pyplot

def findTimesOnData(data, y1, y2):
    "Given a numpy array of time and respective output, locates the times where y1 and y2 are reached"
    t1 = data[0, 0]
    t2 = data[-1, 0]

    # Finding t1 and t2 paying attention to step size
    for i in range(len(data)):
        if i == len(data) - 1:
            # There isn't a next value
            break
        
        if data[i, 1] <= y1 and data[i+1, 1] > y1:
            t1 = data[i, 0]
        elif data[i, 1] <= y2 and data[i+1, 1] > y2:
            t2 = data[i, 0]
            break

    return [t1, t2]

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

def findTimesOnTangentLine(x0, y0, m, y1, y2):
    # Tangent line equation: (y - y0) = m * (x - x0)
    # For t1: (y1 - y0) = m * (t1 - x0)
    t1 = x0 + (y1 - y0) / m

    # For t2: (y2 - y0) = m * (t2 - x0)
    t2 = x0 + (y2 - y0) / m

    return [t1, t2]


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

y_r = data[-1, 1]

if opt >= 1 and opt <= 4:
    # First Order Identification Method
    y1 = None
    y2 = None
    K_p = None
    tau = None
    delay = None

    if opt == 1:
        # Ziegler-Nichols
        [x0, y0, m] = findInflectionPoint(data)
        
        y1 = 0
        y2 = y_r

        [t1, t2] = findTimesOnTangentLine(x0, y0, m, y1, y2)

        delay = t1
        tau = t2 - t1
        
    elif opt == 2:
        # Hagglund
        [x0, y0, m] = findInflectionPoint(data)

        y1 = 0
        y2 = 0.632 * y_r

        [t1, t2] = findTimesOnTangentLine(x0, y0, m, y1, y2)

        delay = t1
        tau = t2 - t1

        
    elif opt == 3:
        # Smith
    
        y1 = 0.283 * y_r
        y2 = 0.632 * y_r
    
        [t1, t2] = findTimesOnData(data, y1, y2)

        tau = 1.5 * (t2 - t1)
        delay = 1.5 * t1 - 0.5 * t2

    elif opt == 4:
        # Sundaresan-Krishnaswamy

        y1 = 0.353 * y_r
        y2 = 0.853 * y_r

        [t1, t2] = findTimesOnData(data, y1, y2)

        tau = 0.67 * (t2 - t1)
        delay = 1.3 * t1 - 0.29 * t2

    K_p = y2 - y1

    print "The Transfer Function is: "
    print str(K_p) + " * e^(-" + str(delay) + " * s)"
    print "-------------------"
    print str(tau) + " * s + 1)"

    tf = r"$Kp * \frac{1}{Ts + 1} * e^{-delays}$"

    estimative = (1 - numpy.exp(-(data[:,0] - delay)/tau)) * K_p

    pyplot.plot(data[:, 0], data[:, 1], 'b', estimative, 'r')
    pyplot.xlabel("Time (seconds)")
    pyplot.title("Comparison")
    pyplot.text(60, .025, tf)
    pyplot.show()

elif opt <= 5:
    # Second Order Identification Method
    print "test"
else:
    print "Invalid option"
