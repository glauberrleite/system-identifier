function [phi, y] = montaRegressoresLinear(N, Ny, Nu, Y, U)
%Algoritmo para montagem de matriz de regressores lineares ARX
%function phi = regres_lin(N, Ny, Nu, Y, U)
%N = Número de dados
%Ny = Número de regressores na saída
%Nu = Número de regressores na entrada
%Y = Vetor de dados de saída
%U = Vetor de dados de entrada
%psi = matriz de regressores montada

k = max(Ny,Nu);
phi = zeros(N - k + 1, Ny + Nu);

for j = 1:Ny
   phi(:,j) = Y(k-j+1:N-j+1);
end

for j = 1:Nu
   phi(:,j+Ny) = U(k-j+1:N-j+1); 
end

phi = phi(1:end-1, :);

y = Y(max(Ny, Nu) + 1:end)';