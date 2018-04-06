import numpy

class LeastSquares:
    def __init__(self, data, inputArray, orderOutput, orderInput):
        self.data = data
        self.inputArray = inputArray
        self.estimative = numpy.zeros(len(data))
        self.error = numpy.zeros(len(data))

        self.phi = self.__buildRegressionMatrix(orderOutput, orderInput)

        print(self.phi)

        self.theta = numpy.dot(numpy.linalg.pinv(self.phi), data[:, 1])

        self._estimate()

        self.error = self.data[:, 1] - self.estimative
    
    def _estimate(self):
        self.estimative = numpy.dot(self.phi , self.theta)

    def showResults(self):
        print("Theta:")
        print(self.theta)

        print("Error:")
        print(numpy.mean(self.error))


    def __buildRegressionMatrix(self, orderOutput, orderInput):
        regressionMatrix = numpy.zeros((len(self.data), orderOutput + orderInput))

        for i in range(len(regressionMatrix)):
            for j in range(1, orderOutput + 1):
                if (i - j) < 0:
                    regressionMatrix[i, j - 1] = 0
                else:
                    regressionMatrix[i, j - 1] = self.data[i - j, 1]

            for j in range(1, orderInput + 1):
                if (i - j) < 0:
                    regressionMatrix[i, j - 1 + orderOutput] = 0
                else:
                    regressionMatrix[i, j - 1 + orderOutput] = self.inputArray[i - j]

        return regressionMatrix

