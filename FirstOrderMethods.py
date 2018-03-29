import numpy
import matplotlib.pyplot as pyplot
from Util import Util

class FirstOrderMethod:
    def __init__(self, data):
        self.data = data
        
        # Preallocating common parameters
        self.K_p = data[-1, 1] - data[0, 1]
        self.y_r = data[-1, 1]
        self.estimative = numpy.zeros(len(self.data))
        self.delay = 0
        self.tau = 0
        self.x_0 = 0
        self.y_0 = 0
        self.m = 0

    def _estimate(self):
        for i in range(len(self.data)):
            if self.data[i, 0] <= self.delay:
                self.estimative[i] = 0
            else:
                self.estimative[i] = (1 - numpy.exp(-(self.data[i, 0] - self.delay)/self.tau)) * self.K_p


    def showResults(self):
        print("The Transfer Function is: ")
        print(str(self.K_p) + " * e^(-" + str(self.delay) + " * s)")
        print("-------------------")
        print("(" + str(self.tau) + " * s + 1)")

    
class ZieglerNichols(FirstOrderMethod):
    def __init__(self, data):
        FirstOrderMethod.__init__(self, data)

        [x_0, y_0, m] = Util.findInflectionPoint(self.data)

        y_1 = self.data[0, 1]
        y_2 = self.y_r

        t_1 = Util.findTimeOnTangentLine(x_0, y_0, m, y_1)
        t_2 = Util.findTimeOnTangentLine(x_0, y_0, m, y_2)

        self.delay = t_1
        self.tau = t_2 - t_1

        self._estimate()
        
        # Tangent line plot
        delta = 10 * (self.data[-1, 0] - self.data[0, 0])/len(data)
        x = numpy.linspace(x_0 - delta, x_0 + delta)
        y = m * (x - x_0) + y_0

        pyplot.plot(x, y, 'g--')

class Hagglund(FirstOrderMethod):
    def __init__(self, data):
        FirstOrderMethod.__init__(self, data)

        [x_0, y_0, m] = Util.findInflectionPoint(self.data)

        y_1 = self.data[0, 1]
        y_2 = 0.632 * self.y_r

        t_1 = Util.findTimeOnTangentLine(x_0, y_0, m, y_1)
        t_2 = Util.findTimeOnTangentLine(x_0, y_0, m, y_2)

        self.delay = t_1
        self.tau = t_2 - t_1

        self._estimate()

        # Tangent line plot
        delta = 10 * (self.data[-1, 0] - self.data[0, 0])/len(data)
        x = numpy.linspace(x_0 - delta, x_0 + delta)
        y = m * (x - x_0) + y_0

        pyplot.plot(x, y, 'g--')

class Smith(FirstOrderMethod):
    def __init__(self, data):
        FirstOrderMethod.__init__(self, data)

        y_1 = 0.283 * self.y_r
        y_2 = 0.632 * self.y_r
        
        t_1 = Util.findTimeOnData(self.data, y_1)
        t_2 = Util.findTimeOnData(self.data, y_2)

        self.tau = 1.5 * (t_2 - t_1)
        self.delay = 1.5 * t_1 - 0.5 * t_2

        self._estimate()

class SundaresanKrishnaswamy(FirstOrderMethod):
    def __init__(self, data):
        FirstOrderMethod.__init__(self, data)

        y_1 = 0.353 * self.y_r
        y_2 = 0.853 * self.y_r

        t_1 = Util.findTimeOnData(self.data, y_1)
        t_2 = Util.findTimeOnData(self.data, y_2)

        self.tau = 0.67 * (t_2 - t_1)
        self.delay = 1.3 * t_1 - 0.29 * t_2

        self._estimate()
