function phi = buildRegressionMatrix(order, dataOutput, dataInput, dataError)
    m = length(dataOutput);

    n = 2 * order;
    %if (varargin == 4)
        n = n + order;
    %end
    
    phi = zeros(m, n);

    for row = 1:m
        for col = 1:order
           if(row-col) < 1
               phi(row, col) = 0;
               phi(row, col + order) = 0;
               
               %if (varargin == 4)
                   phi(row, col + 2*order) = 0;
               %end
           else
               phi(row, col) = dataOutput(row-col);
               phi(row, col + order) = dataInput(row-col);
               
               %if (varargin == 4)
                    phi(row, col + 2*order) = dataError(row-col);
               %end
           end
        end
    end
end