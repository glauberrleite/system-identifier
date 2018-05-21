function [estimative, error_v] = validate(theta, epsilon, dataOutput, dataInput, dataError)

    if nargin == 5
        extended = true;
    else
        extended = false;
    end
    
    if extended
        order = length(theta)/3;
    else
        order = length(theta)/2;
    end
    
    y_v = dataOutput(epsilon:end);
    estimative = zeros(length(y_v), 1);
    
    for i = 1:length(estimative)
        if (extended)
            phi = zeros(1, 3*order);
        else
            phi = zeros(1, 2*order);
        end
        
        for j = 1:order
            if (i - j) < 1
                phi(j) = dataOutput(i - j + epsilon - 1);
            else
                phi(j) = estimative(i - j);
            end        
            
            phi(j + order) = dataInput(i - j + epsilon - 1);

            if (extended)
                phi(j + 2*order) = dataError(i - j + epsilon - 1);
            end
        end
        
        estimative(i) = phi * theta;
    end
    
    error_v = y_v - estimative;

end

