function [theta, error_mean] = ...
    LS(order_input, order_output, data)

    n = order_input + order_output;
    m = length(data);
    input = ones(m);

    phi = zeros(m,n);

    for row = 1:m
        for col = 1:order_output
           if(row-col) < 1
               phi(row, col) = 0;
           else
               phi(row, col) = data(row-col, 2);
           end
        end
        for col = 1:order_input
            if(row-col) < 1
                phi(row, col + order_output) = 0;
            else
                phi(row, col + order_output) = input(row-col);
            end
        end
    end


    Y = data(:,2);
    phi_pinv = pinv(phi);

    % theta
    theta = phi_pinv * Y;

    % Y estimado ou Y^
    Y_e = phi * theta;

    % eps = Y - Y^
    error = Y - Y_e;

    disp('Theta:')
    theta
    disp('Error:')
    error_mean = mean(error);
    error_mean
    plot(Y, 'b')
    hold on
    plot(Y_e, 'r')
    legend('Y', 'Y estimado')
end