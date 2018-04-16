%%
order_input = 5;
order_output = 5;
n = order_input + order_output;

fileID = fopen('stepG2.txt', 'r');
formatSpec = '%f %f';
sizeData = [2 Inf];
data = fscanf(fileID, formatSpec, sizeData);
data = data';

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

%% order 1
theta1 = theta;
error_mean1 = error_mean;

%% order 2
theta2 = theta;
error_mean2 = error_mean;

%% order 3
theta3 = theta;
error_mean3 = error_mean;

%% order 4
theta4 = theta;
error_mean4 = error_mean;

%% order 5
theta5 = theta;
error_mean5 = error_mean;

%% Save in .mat file
Estimative.theta1 = theta1;
Estimative.theta2 = theta2;
Estimative.theta3 = theta3;
Estimative.theta4 = theta4;
Estimative.theta5 = theta5;
Estimative.error1 = error_mean1;
Estimative.error2 = error_mean2;
Estimative.error3 = error_mean3;
Estimative.error4 = error_mean4;
Estimative.error5 = error_mean5;
save('part2-2.mat', '-struct', 'Estimative');