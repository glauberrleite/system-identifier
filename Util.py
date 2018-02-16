class Util:
    @staticmethod
    def findTimeOnData(data, y):
        "Given a numpy array of time and respective output, locates the times where y1 and y2 are reached"
        t = data[-1, 0]

        # Finding t1 and t2 paying attention to step size
        for i in range(len(data)):
            if i == len(data) - 1:
                # There isn't a next value
                break
                                                                    
            if data[i, 1] <= y and data[i + 1, 1] > y:
                t = data[i, 0]
                break

        return t
    
    @staticmethod
    def findInflectionPoint(data):
        "Given a numpy array of time and respective output, locates the inflection point and the derivative on it"
        m = 0
        x0 = data[0, 0]
        y0 = data[0, 1]
        y_min = data[-1,1]/3
        
        for i in range(len(data)):
            delta = abs((data[i, 1] - data[i + 1, 1]) / (data[i, 0] - data[i + 1, 0]))
            if delta < m and data[i, 1] > y_min:
                x0 = data[i, 0]
                y0 = data[i, 1]
                break
            m = delta
                                                                                                                                                                                           
        print("Inflection detected at [" + str(x0) + ", " + str(y0) + "]")
        return [x0, y0, m]

    @staticmethod
    def findTimeOnTangentLine(x0, y0, m, y):
        # Tangent line equation: (y - y0) = m * (x - x0)
        t = x0 + (y - y0) / m
        return t

    @staticmethod
    def iae(data, estimative):
        result = 0

        n = len(data[:, 0])

        for i in range(n):
            result = result + abs(estimative[i] - data[i, 1])

        return result

    @staticmethod
    def ise(data, estimative):
        result = 0

        n = len(data[:, 0])

        for i in range(n):
            result = result + ((estimative[i] - data[i, 1])**2) 

        return result
    
    @staticmethod
    def mse(data, estimative):
        result = 0

        n = len(data[:, 0])

        for i in range(n):
            result = result + ((estimative[i] - data[i, 1])**2) 

        return result/n

    @staticmethod
    def itae(data, estimative):
        result = 0

        n = len(data[:, 0])

        for i in range(n):
            result = result + data[i, 0] * abs(estimative[i] - data[i, 1]) 

        return result
