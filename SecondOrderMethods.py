from Util import Util
import numpy

class SecondOrderMethod:
    def __init__(self, data):
        # Preallocation
        self.data = data
        self.y_r = data[-1, 1]
        self.estimative = numpy.zeros(len(self.data[:, 0]))
        self.zeta = 0
        self.w_n = 0
        self.delay = 0

    def _estimate(self):
        if self.zeta < 1:
            beta = numpy.sqrt(1 - (self.zeta ** 2))
            phi = numpy.arctan(self.zeta/beta)
            estimative = 1 - (1 / beta) * numpy.exp(-self.zeta * self.w_n * self.data[:, 0]) * numpy.cos(self.w_n * beta * self.data[:, 0] - phi)
        else:
            tau1 = (self.zeta + numpy.sqrt((self.zeta**2) - 1))/self.w_n
            tau2 = (self.zeta - numpy.sqrt((self.zeta**2) - 1))/self.w_n
            print("zeta >= 1")


class Mollenkamp(SecondOrderMethod):
    def __init__(self, data):
        
        SecondOrderMethod.__init__(self, data) 

        y_1 = 0.15 * self.y_r
        y_2 = 0.45 * self.y_r
        y_3 = 0.75 * self.y_r

        t_1 = Util.findTimeOnData(data, y_1)
        t_2 = Util.findTimeOnData(data, y_2)
        t_3 = Util.findTimeOnData(data, y_3)

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

