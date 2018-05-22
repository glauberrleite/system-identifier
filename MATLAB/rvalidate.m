function [estimative, error_v] = rvalidate(theta, epsilon, dataOutput, dataInput)
    y_v = dataOutput(epsilon:end);
    estimative = zeros(length(y_v), 1);
    
    order = length(theta(end, :))/2;
    
    for i = 1:length(estimative)
        phi = zeros(2*order, 1);
        
        for j = 1:order
            if (i - j) < 1
                phi(j) = dataOutput(i - j + epsilon - 1);
            else
                phi(j) = estimative(i - j);
            end        
            
            phi(j + order) = dataInput(i - j + epsilon - 1);
        end
        
        estimative(i) = theta(i + epsilon - 1, :) * phi;
    end
    
    error_v = y_v - estimative;
end