import gurobipy as gp

#Sets
cakes = ["Choc", "Plain"]
ingredients = ["Eggs", "Time", "Milk"]

#Data
revenue = [4, 2]                    # revenue per cake
availability = [30, 480, 5000]      # of ingredients
usage = [
            [4, 20, 250],           # usage per ingredient for chocolate cake
            [1, 50, 200]            # usage per ingredient for plain cake
        ]

#Setup Model
m = gp.Model("Farmer Jones")

#Create variables
X = {}
for c in range(len(cakes)):
    X[c] = m.addVar(vtype=gp.GRB.INTEGER)

#Objective (to optimize)
m.setObjective(gp.quicksum(revenue[c]*X[c] for c in range(len(cakes))), gp.GRB.MAXIMIZE)

#Add constraints
for i in range(len(ingredients)):
    m.addConstr(gp.quicksum(usage[c][i]*X[c] for c in range(len(cakes))) <= availability[i])

#Run model
m.optimize()

#Find number of each cake
for c in range(len(cakes)):
    print(f"Make {X[c].x} {cakes[c]}")

    # X[n].lb = lowerbound
    # X[n].ub = upperbound
    # X[n].obj = coefficient in objective
    # where n is variable

print(f"Revenue is {m.ObjVal}")