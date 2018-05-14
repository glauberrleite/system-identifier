import numpy

class LeastSquares:
    def __init__(self, y, u, e, orderOutput, orderInput, orderError):
        self.y = y
        self.u = u
        self.e = e
        self.estimative = numpy.zeros(len(y))
        self.error = numpy.zeros(len(y))

        self.phi = self.__buildRegressionMatrix(orderOutput, orderInput, orderError)

        self.theta = numpy.dot(numpy.linalg.pinv(self.phi), y)

        self._estimate()

        self.error = self.y - self.estimative
    
    def _estimate(self):
        self.estimative = numpy.dot(self.phi , self.theta)

    def showResults(self):
        print("Theta:")
        print(self.theta)

        print("Error:")
        print(numpy.mean(self.error))


    def __buildRegressionMatrix(self, orderOutput, orderInput, orderError):
        regressionMatrix = numpy.zeros((len(self.y), orderOutput + orderInput + orderError))

        for i in range(len(regressionMatrix)):
            for j in range(1, orderOutput + 1):
                if (i - j) < 0:
                    regressionMatrix[i, j - 1] = 0
                else:
                    regressionMatrix[i, j - 1] = self.y[i - j]

            for j in range(1, orderInput + 1):
                if (i - j) < 0:
                    regressionMatrix[i, j - 1 + orderOutput] = 0
                else:
                    regressionMatrix[i, j - 1 + orderOutput] = self.u[i - j]

            for j in range(1, orderError + 1):
                if (i - j) < 0:
                    regressionMatrix[i, j - 1 + orderOutput + orderInput] = 0
                else:
                    regressionMatrix[i, j - 1 + orderOutput + orderInput] = self.e[i - j]

        return regressionMatrix

