function [theta, estimative] = ...
    LS(order, dataOutput, dataInput, dataError)

    if (nargin == 4)
        phi = buildRegressionMatrix(order, dataOutput, dataInput, dataError);
    else
        phi = buildRegressionMatrix(order, dataOutput, dataInput);
    end

    Y = dataOutput;
    phi_pinv = pinv(phi);

    % theta
    theta = phi_pinv * Y;

    % Y estimado ou Y^
    estimative = phi * theta;

end