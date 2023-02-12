# blending.mod
param Cmax integer;   # Number of crudes
param Nfuels integer; # Number of different fuels

set C := 1..Cmax;
set F := 1..Nfuels;

param res{C};         # Storage of each crude
param mix_min{F,C};   # Minimum required of a certain crude
param mix_max{F,C};   # Maximum allowed of a certain crude
param price{C};       # Each crude has a price
param revenue{F};     # Each fuel gains money

var x{F,C} >= 0.0, <= 1.0;  # Proportion of mix

maximize gain: sum{i in F, j in C} res[j]*(revenue[i] - price[j])*x[i,j];

subject to reserve{j in C}:
	sum{i in F} x[i,j] <= 1;

subject to mix_constraint1{i in F, j in C}:
	x[i,j] <= mix_max[i,j];
	
subject to mix_constraint2{i in F, j in C}:
	x[i,j] >= mix_min[i,j];
