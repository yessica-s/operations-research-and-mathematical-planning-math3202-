import gurobipy as gp

#Setup Model
m = gp.Model("Farmer Jones")

#Create variables
#  - default non-negative constraints
x1 = m.addVar()
x2 = m.addVar()

#Objective (to optimize)
m.setObjective(4*x1+2*x2, gp.GRB.MAXIMIZE)

#Add constraints
#Matrix: 
#   - number of rows = number of constraints
#   - number of columns = number of variables
m.addConstr(4*x1 + x2 <= 30)            # eggs
m.addConstr(20*x1 + 50*x2 <= 480)       # time
m.addConstr(250*x1 + 200*x2 <= 5000)    # milk

#Run model
m.optimize()

#Find number of each cake
print(f"Make {x1.x} chocolate") #chocolate
print(f"Make {x2.x} plain") #plain
