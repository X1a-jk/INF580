# multiperiod.mod

# index sets
param Tmax integer, >0; # month indices
set T := 1..Tmax;
set T0 := 0..Tmax;

# parameters
param f{T} >= 0;   # sales forecasts for month t
param p >= 0;      # max in-house monthly production
param d >= 0;      # min in-house monthly production
param r >= 0;      # max subcontracted monthly production
param cn >= 0;     # unit cost of in-house production
param csub >= 0;   # unit cost of subcontracted production
param cstore >= 0; # unit storage cost

# decision variables
var x{T} >= 0;     # unit produced during month t
var w{T} binary;   # =1 iff normal production active at month t
var y{T} >= 0;     # units subcontracted during month t
var z{T0} >= 0;    # units stored during month t

# objective
minimize cost:
  cn*sum{t in T} x[t] + csub*sum{t in T} y[t] + cstore*sum{t in T} z[t];

# constraints
subject to demand_satisfaction{t in T}: x[t] + y[t] + z[t-1] >= f[t];
subject to storage_balance{t in T}: x[t] + y[t] + z[t-1] = z[t] + f[t];
subject to max_inhouse{t in T}: x[t] <= p;
subject to max_subcontracted{t in T}: y[t] <= r;
subject to empty_storage_t0: z[0] = 0;
subject to min_inhouse1{t in T}: x[t] >= d*w[t]; # these two constraints state
subject to min_inhouse2{t in T}: x[t] <= p*w[t]; # that w_t=0 => x_t=0
