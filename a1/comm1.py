import gurobipy as gp

#Sets
telescopes = ["AU1", "CL1", "SA1", "AU2", "CL2", "HI1"]
days = ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"]

T = range(len(telescopes))
D = range(len(days))

#Data
efficiency = [0.99, 0.99, 0.93, 0.41, 0.40, 0.33] #efficiency in detecting NEOs
discovery_rate = [2.4, 3.4] #discovery rate per belt (hourly)
total_visibility_per_day = [4.8, 5.5, 6.5, 4.7, 5.4, 5.6, 6.1]
neo_visibility_per_day = [3.3, 3.9, 4.0, 3.6, 3.6, 3.8, 4.8]

#Setup model
m = gp.Model("ASC")

#Create variables
X = {} #hrs per telescope per day main/total belt
Y = {} #hrs per telescope per day on neo belt
for t in T:
    for d in D:
        X[t, d] = m.addVar(vtype=gp.GRB.CONTINUOUS)
        Y[t, d] = m.addVar(vtype=gp.GRB.CONTINUOUS)

#Objective
m.setObjective(gp.quicksum(efficiency[t]*discovery_rate[0]*X[t, d]+efficiency[t]*discovery_rate[1]*Y[t, d] for d in D for t in T), gp.GRB.MAXIMIZE)

#Add constraints
for t in T:
    for d in D:
        m.addConstr(Y[t, d] <= neo_visibility_per_day[d])
        m.addConstr(X[t, d] + Y[t, d] <= total_visibility_per_day[d])

#Run model
m.optimize()

#Find hours per day
for t in T:
    for d in D:
        print(f"Hours on main belt on {telescopes[t]} on {days[d]}: {X[t, d].x}")
        print(f"Hours on neo belt on {telescopes[t]} on {days[d]}: {Y[t, d].x}")

#Find optimal discoveries
print(m.ObjVal)