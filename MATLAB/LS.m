function [theta, estimative] = ...
    LS(order, dataOutput, dataInput)

    phi = buildRegressionMatrix(order, dataOutput, dataInput);

    Y = dataOutput;
    phi_pinv = pinv(phi);

    % theta
    theta = phi_pinv * Y;

    % Y estimado ou Y^
    estimative = phi * theta;

end