import numpy
from Util import Util

class YuwanaSeborg:
    def __init__(self, data):
        self.data = data
        self.estimative = numpy.zeros(len(self.data))

        k_c = 1.0
        k = 1.0
        setpoint = 1.0

        [y_p1, y_m1, y_p2] = Util.findCriticalPoints(self.data, 3)

        print("y_p1 = " + str(y_p1))
        print("y_m1 = " + str(y_m1))
        print("y_p2 = " + str(y_p2))

        # Finding y when steady-state
        y_ss = (y_p2 * y_p1 - (y_m1**2))/(y_p1 + y_p2 - 2*y_m1)

        # Computing zeta process which is important to find other process parameters
        aux1 = numpy.log((y_ss - y_m1)/(y_p1 - y_ss))

        aux2 = numpy.log((y_p2 - y_ss)/(y_p1 - y_ss))

        zeta_1 = -aux1 / numpy.sqrt(numpy.pi**2 + aux1**2)
        zeta_2 = -aux2 / numpy.sqrt(4 * (numpy.pi**2) + aux2**2)

        zeta_m = (zeta_1*zeta_2)/2

        # Determining overshootDuration
        deltaT = self.__getOvershootDuration(data, y_ss)

        print("deltaT = " + str(deltaT))

        k_m = y_ss / (k_c * (setpoint - y_ss))
        k_f = k_c * k_m

        # Finding process parameters
        aux1 = numpy.sqrt((1 - zeta_m**2) * (k_f + 1))
        aux2 = zeta_m * numpy.sqrt(k_f + 1) + numpy.sqrt((zeta_m**2) * (k_f + 1) + k_f)

        theta_m = 2 * (deltaT / numpy.pi) * (aux1 / aux2)

        tau_m = (deltaT / numpy.pi) * aux1 * aux2

        # Estimating transfer function parameters

        self.k_tf = k_f / (k_f + 1)

        self.tau_tf = numpy.sqrt((theta_m * tau_m) / (2 * (k_f + 1)))

        self.zeta_tf = (tau_m + 0.5 * theta_m * (1 - k_f)) / numpy.sqrt(2 * theta_m * tau_m * (k_f + 1))

        self.theta_tf = theta_m

        print("K' = " + str(self.k_tf))
        print("theta = " + str(self.theta_tf))
        print("tau = " + str(self.tau_tf))
        print("zeta = " + str(self.zeta_tf))

    def __getOvershootDuration(self, data, y_ss):
        t1 = data[0, 0]
        t2 = data[-1, 0]
        flag = True

        for value in data:
            if flag: 
                if value[1] >= y_ss:
                    t1 = value[0]
                    flag = False
            else:
                if value[1] <= y_ss:
                    t2 = value[0]
                    break

        return (t2 - t1)

    def showTransferFunction(self):
        print("The transfer function")
        print("G(s) = " + str(self.k_tf) + " * (1 - 0.5 * " + str(self.theta_tf)+ " * s)")
        print("---------------------------")
        print(str(self.tau_tf) + "**2 * s**2 + 2 * "+ str(self.zeta_tf) +" * " + str(self.tau_tf) + " * s + 1")
