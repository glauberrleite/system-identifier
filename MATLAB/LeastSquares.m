%%
order_input = 2;
order_output = 2;
n = order_input + order_output;

fileID = fopen('stepG2.txt', 'r');
formatSpec = '%f %f';
sizeData = [2 Inf];
data = fscanf(fileID, formatSpec, sizeData);
data = data';

data = [
    1.0, 0.9; 
    0.8, 2.5;
    0.6, 2.4;
    0.4, 1.3;
    0.2, 1.2;
    0.0, 0.8;
    0.2, 0.0;
    0.4, 0.9;
    0.6, 1.4;
    0.8, 1.9;
    1.0, 2.3;
    0.8, 2.4;
    0.6, 2.3;
    0.4, 1.3;
    0.2, 1.2
    ];

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

phi_pinv = pinv(phi);
theta = phi_pinv * data(:,2);
estimative = phi * theta;
error = data(:,2) - estimative;
disp('Theta:')
theta
disp('Error:')
mean(error)