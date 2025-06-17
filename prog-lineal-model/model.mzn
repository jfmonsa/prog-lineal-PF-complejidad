% ---- Params from .dzn -----
int: N; % Tamaño del plano NxN
int: num_ciudades; % Cantidad de ciudades
% Arrays for the locations (x,y) of each city
array[CIUDADES] of int: ciudad_x;
array[CIUDADES] of int: ciudad_y;

% name the range [1 , num_ciudades] as CIUDADES to iterate easily over the cities
set of int: CIUDADES = 1..num_ciudades;

% ---- Variables de decisión ---
var 0..N-1: x_concierto;
var 0..N-1: y_concierto;

% ---- Aux Variables -----
% Arrays to hold the absolute distances in X and Y
% dx[i]: Distancia absoluta en X entre el concierto y la ciudad i
% dy[i]: Distancia absoluta en Y entre el concierto y la ciudad i
% NOTE: range bound 0..2*N explained in the Report
array[CIUDADES] of var 0..2*N: dx;
array[CIUDADES] of var 0..2*N: dy;

% ----- Constraints -----
% used to fill the absolute distance arrays dx and dy
% For each city i, the distance in X and Y is defined as:
% |x_concierto - ciudad_x[i]| == dx[i]
% |y_concierto - ciudad_y[i]| == dy[i]
constraint forall(i in CIUDADES)(
  dx[i] = abs(x_concierto - ciudad_x[i]) /\
  dy[i] = abs(y_concierto - ciudad_y[i])
);

constraint forall(i in CIUDADES)(
  % A city cannot be at the same location as the concert
  (x_concierto != ciudad_x[i]) /\ (y_concierto != ciudad_y[i])
);

% ---- Objective Function -----
% distancia total entre el concierto y todas las ciudades
% suma de las distancias manhattan desde el concierto a cada ciudad, esto es justo lo que el problema pide minimizar.
var int: total_distancia = sum(i in CIUDADES)(dx[i] + dy[i]);
solve minimize total_distancia;

output [
  "Concierto en: (", show(x_concierto), ", ", show(y_concierto), ")\n",
  "Distancia total: ", show(total_distancia), "\n",
];

% TODO: pasar explicación del limite superior de dx[i] y dy[i] a el informe en latex.
% Variables auxiliares para representar valores absolutos
% dx[i]: Representa la distancia absoluta en X entre el concierto y la ciudad i, es decir: |x_concierto - ciudad_x[i]|.
% dy[i]: Representa la distancia absoluta en Y entre el concierto y la ciudad i, es decir: |y_concierto - ciudad_y[i]|.
% Se usa 2*N como límite superior porque en el peor caso la distancia entre dos puntos puede ser hasta 2*N - 2 (por ejemplo de (0,0) a (N-1,N-1)).
% ¿Cuál es la mayor distancia posible en un plano de tamaño N×NN×N?

% Si el plano tiene tamaño N×N, los valores posibles para cada coordenada son desde 0 hasta N−1.
% Entonces:

%     La mayor diferencia en X es:
%     ∣0−(N−1)∣=N−1

%     Lo mismo para Y:
%     ∣0−(N−1)∣=N−1

% Entonces la máxima distancia Manhattan posible es:
% maxima distancia=(N−1)+(N−1)=2N−2

% Estas restricciones modelan la distancia absoluta (|a - b|) usando desigualdades lineales.
% MiniZinc no permite usar directamente abs(a - b) dentro de la función objetivo, por eso usamos estas restricciones para forzar que:
% dx[i] siempre sea mayor o igual a la diferencia positiva o negativa entre x_concierto y ciudad_x[i].
% dy[i] lo mismo pero con la coordenada Y.
% Esto asegura que dx[i] = |x_concierto - ciudad_x[i]| y dy[i] = |y_concierto - ciudad_y[i]|.
% alternativa convirtiendo a forma standard:
% dx[i] >= x_concierto - ciudad_x[i] /\
% dx[i] >= ciudad_x[i] - x_concierto /\

% dy[i] >= y_concierto - ciudad_y[i] /\
% dy[i] >= ciudad_y[i] - y_concierto
