# demands_again.mod

# index sets
param Tmax integer, >0;
set T := 1..Tmax;
set T0 := 0..Tmax;

# parameters
param d{T} >= 0;   # service hour demands per month
param sigma >= 0;  # starting number of consultants
param omega >= 0;  # hours/month worked by each consultant
param gamma >= 0;  # monthly salary of each consultant
param tau >= 0;    # number of hours needed to train a new consultant
param delta >= 0;  # monthly salary of each trainee
param p >=0, <=1;  # fraction of trainees who leave the firm after training

# decision variables
var x{T0} integer, >= 0;     # number of trainees hired at month
var y{T0} integer, >= 0;     # number of consultants at month

# objective
minimize cost: gamma*sum{t in T} y[t] + tau*sum{t in T} x[t];

# constraints
subject to demand_satisfaction{t in T}: omega*y[t] - tau*x[t] >= d[t];
subject to boundary_condition1: y[0] = sigma;
subject to boundary_condition2: x[0] = 0;
# [error: since (1-p) not integer, but vars are integer, equation infeasible]
#subject to active_consultants{t in T}: y[t-1] + (1-p)*x[t-1] = y[t];

# this modelling linearizes floor((1-p)x[t-1]) with z[t]
var z{T} integer, >= 0;      # number of remaining trainees
subject to active_consultants{t in T}: y[t-1] + z[t] = y[t];
subject to floor_linearization1{t in T}: z[t] <= (1-p)*x[t-1];
subject to floor_linearization2{t in T}: z[t] >= (1-p)*x[t-1]-1;

