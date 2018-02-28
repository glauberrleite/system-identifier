import numpy
from Util import Util

class YuwanaSeborg:
    def __init__(self, data):
        self.data = data
        self.estimative = numpy.zeros(len(self.data))

        [y_p1, y_m1, y_p2] = Util.findCriticalPoints(self.data, 3)

        print("y_p1 = " + str(y_p1))
        print("y_m1 = " + str(y_m1))
        print("y_p2 = " + str(y_p2))

    def showTransferFunction(self):
        pass
