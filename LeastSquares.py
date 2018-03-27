import numpy

class LeastSquares:
    def __init__(self, data, inputArray, orderOutput, orderInput):
        self.data = data
        self.inputArray = inputArray
        self.estimative = numpy.zeros(len(data))
        
        phi = self.__buildRegressionMatrix(orderOutput, orderInput)

        print(phi)
    
    def _estimate(self):
        pass

    def showTransferFunction(self):
        pass

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
