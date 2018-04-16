%% abre os valores de entrada com ruido
% entrada_rand2.txt

fileID = fopen('entrada_rand2.txt', 'r');
formatSpec = '%f';
sizeData = Inf;
data = fscanf(fileID, formatSpec, sizeData);
x = data;


%% fazer 100x
x = ones(100, 1);

Y = ones(100, 1);
noise = 0.5*randn(length(Y), 1);

n = 100;
y(1:2) = 0;
Y(1:2) = 0;
for k=3:n
    y(k) = 1.881*y(k-1) - 0.9048*y(k-2) ...
        + 0.01207*x(k-1)-0.01167*x(k-2);
    Y(k) = y(k);
    y(k) = y(k) + noise(k);
end

data = ones(100,2);
data(:, 1) = x;
data(:, 2) = y;

LS(3, 3, data);