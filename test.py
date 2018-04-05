from Util import Util
import numpy
import matplotlib.pyplot as pyplot

inputArray = numpy.ones(100)
theta = [ 2.705, -2.448, 0.7408, 0.0523, -0.0855, 0.035 ]
orderOutput = 3
orderInput = 3
sampleRate = 0.1


y = Util.computeOutput(inputArray, theta, orderOutput, orderInput)
t = numpy.arange(0, len(y)*sampleRate, sampleRate)

pyplot.plot(t, y, 'r')
pyplot.plot(t, inputArray, 'b--')
pyplot.show()
