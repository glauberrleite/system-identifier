from Util import Util
import numpy

class SecondOrderMethod:
    def __init__(self, data):
        # Preallocation
        self.data = data
        self.y_r = data[-1, 1]
        self.estimative = numpy.zeros(len(self.data))
        self.zeta = 0
        self.w_n = 0
        self.delay = 0
        self.tau1 = 0
        self.tau2 = 0
        self.k = data[-1, 1] - data[0, 1]

    def _estimate(self):
        for i in range(len(self.data)):
            if self.data[i, 0] <= self.delay:
                self.estimative[i] = 0
            elif self.zeta < 1:
                beta = numpy.sqrt(1 - (self.zeta ** 2))
                phi = numpy.arctan(self.zeta/beta)
                self.estimative[i] = self.k * (1 - (1 / beta) * numpy.exp(-self.zeta * self.w_n * self.data[i, 0]) * numpy.cos(self.w_n * beta * self.data[i, 0] - phi))
            else:
                self.tau1 = (self.zeta + numpy.sqrt((self.zeta**2) - 1))/self.w_n
                self.tau2 = (self.zeta - numpy.sqrt((self.zeta**2) - 1))/self.w_n
                self.estimative[i] = (self.k/(self.tau1 * self.tau2)) \
                        * ((self.tau1*self.tau2) \
                        + ( ( (self.tau1**2)*(self.tau2) ) / (self.tau2 - self.tau1) ) * numpy.exp(-(self.data[i, 0] - self.delay)/self.tau1)  \
                        + ( ( (self.tau1)*(self.tau2**2) ) / (self.tau1 - self.tau2) ) * numpy.exp(-(self.data[i, 0] - self.delay)/self.tau2))


    def showTransferFunction(self):
        print("The Transfer Function is:")
        if self.zeta < 1:
            print(str(self.k) + " * (" + str(self.w_n) + "^2) * e^(-"+ str(self.delay)  +"s)")
            print("-----------------------")
            print("s^2 + 2 * "+ str(self.zeta) +" * " + str(self.w_n) + " * s + " + str(self.w_n) + "^2")
        else:
            print(str(self.k) + " * e^(-"+ str(self.delay) + "s)")
            print("(" + str(self.tau1) + "s + 1) * (" + str(self.tau2) + "s + 1)")


class Mollenkamp(SecondOrderMethod):
    def __init__(self, data):        
        SecondOrderMethod.__init__(self, data) 

        y_1 = 0.15 * self.y_r
        y_2 = 0.45 * self.y_r
        y_3 = 0.75 * self.y_r

        t_1 = Util.findTimeOnData(data, y_1)
        t_2 = Util.findTimeOnData(data, y_2)
        t_3 = Util.findTimeOnData(data, y_3)

        print("t1 = " + str(t_1))
        print("t2 = " + str(t_2))
        print("t3 = " + str(t_3))

        x = (t_2 - t_1)/(t_3 - t_1)

        self.zeta = (0.0805 - (5.547 * ((0.475 - x) ** 2))) / (x - 0.356)

        f_2 = 0
        if (self.zeta < 1):
            f_2 = 0.708 * (2.811 ** self.zeta)
        else:
            f_2 = 2.6 * self.zeta - 0.6

        self.w_n = f_2 / (t_3 - t_1)

        f_3 = 0.922 * (1.66 ** self.zeta)

        self.delay = t_2 - f_3/self.w_n

        self._estimate()

class Smith2(SecondOrderMethod):
    def __init__(self, data):
        SecondOrderMethod.__init__(self, data)

        y_1 = 0.2 * self.y_r
        y_2 = 0.6 * self.y_r

        t_1 = Util.findTimeOnData(data, y_1)
        t_2 = Util.findTimeOnData(data, y_2)

        self.delay = 1.5 * Util.findTimeOnData(data, 0.283 * self.y_r) - 0.5 * Util.findTimeOnData(data, 0.632 * self.y_r)

        t_1 = t_1 - self.delay
        t_2 = t_2 - self.delay

        print("t20 = " + str(t_1))
        print("t60 = " + str(t_2))
        print("t20/t60 = " + str(t_1/t_2))

        print("Use these values to find zeta and tau")
        self.zeta = input("zeta: ")
        tau = input("tau: ")

        self.w_n = 1/tau

        self._estimate()
