function [theta, estimative] = ...
    RLS(order, loss, dataOutput, dataInput, dataError)
    
    if nargin == 5
        extended = true;
    else
        extended = false;
    end

    % Preallocation
    if (extended)
        theta = zeros(length(dataOutput), order*3); 
    else
        theta = zeros(length(dataOutput), order*2);
    end
    estimative = zeros(length(dataOutput), 1);
    
    % Initial values
    P = 10000;
    
    for i = 1:length(dataOutput)
        if (extended)
            phi = zeros(1, order*3);
        else
            phi = zeros(1, order*2);
        end
        
        % Filling phi
        for j = 1:order
            if (i - j) < 1
                phi(j) = 0;
                phi(j + order) = 0;
                if (extended)
                   phi(j + 2*order) = 0;
                end
            else
                phi(j) = dataOutput(i - j);
                phi(j + order) = dataInput(i - j);
                if (extended)
                    phi(j + 2*order) = dataError(i - j);
                end
            end
        end
        
        K = (P*phi) / (phi*P*transpose(phi) + loss);
                
        if (i > 1)
            theta(i, :) = theta(i - 1, :) + K * (dataOutput(i) - phi*transpose(theta(i - 1, :)));
        else 
            theta(i, :) = K * dataOutput(i);
        end
        
        P = (1 / loss) * (P - (P*phi*transpose(phi)*P)/(phi*P*transpose(phi) + loss));
        
        estimative(i) = phi*transpose(theta(i, :));
    end
end