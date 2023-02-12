minimize cost:
	200*x[1,1] + 350*x[1,2] + 450*x[1,3] + 200*x[2,1] + 350*x[2,2] + 
	450*x[2,3] + 200*x[3,1] + 350*x[3,2] + 450*x[3,3] + 200*x[4,1] + 
	350*x[4,2] + 450*x[4,3];

subject to demand_satisfaction[1]:
	x[1,1] + x[1,2] + x[1,3] >= 9;

subject to demand_satisfaction[2]:
	x[1,2] + x[1,3] + x[2,1] + x[2,2] + x[2,3] >= 5;

subject to demand_satisfaction[3]:
	x[1,3] + x[2,2] + x[2,3] + x[3,1] + x[3,2] + x[3,3] >= 7;

subject to demand_satisfaction[4]:
	x[2,3] + x[3,2] + x[3,3] + x[4,1] + x[4,2] + x[4,3] >= 9;

