import gurobipy as gp

""" Model Data (given) """


# Sets
Foods = ['White Rice', 'Boiled Egg', 'Greek Yoghurt', 'Dark Chocolate', 
         'Canned Chickpeas', 'Canned Tuna', 'Peanut Butter', 'Pasta Spirals', 
         'White Bread', 'Frozen Blueberries', 'Frozen Corn', 'Potato Wedges', 
         'Frozen Peas', 'Vanilla Custard', 'Almonds', 'Milk', 'Canned Peaches', 
         'Canned Tomatoes', 'Baked Beans', 'Chicken Breast', 'Beef Sausages']

Nutrients = ['Energy', 'Protein', 'Fibre', 'Iron', 'Calcium', 'Vitamin C',
             'Thiamin', 'Riboflavin', 'Vitamin A', 'Zinc', 'Folate',
             'Niacin', 'Sodium']

F = range(len(Foods))
N = range(len(Nutrients))

# Costs ($/100g) from coles.com.au [2026-01-22]
# Mostly Coles brands - no specials or bulk sizes
C = [0.30, 0.93, 0.38, 4.40, 0.24, 0.78, 0.68, 0.20, 0.49, 1.20, 0.42, 0.60, 0.45, 
     0.30, 1.87, 0.16, 0.36, 0.28, 0.35, 1.45, 1.18 ]

# Nutritional data from the Australian Food Composition Database
# https://www.foodstandards.gov.au/science/monitoringnutrients/afcd/Pages/default.aspx
NV = [
    [659, 3.1, 0.8, 0.09, 2, 0, 0.02, 0.013, 0, 0.58, 5, 0.07, 0],
    [204, 11.6, 0, 0.2, 6, 0, 0, 0.31, 0, 0, 5, 0, 175],
    [306, 5.1, 0.1, 0, 175, 0, 0.02, 0.22, 50, 0.57, 25, 0, 58],
    [2210, 3.9, 1.2, 4.4, 52, 0, 0.05, 0.13, 21, 2, 13, 1.3, 55],
    [474, 6.3, 5.7, 1.8, 45, 0, 0, 0, 4, 1, 63, 0.5, 250],
    [540, 26.1, 0, 1.16, 5, 0, 0, 0.02, 0, 0.76, 26, 12, 250],
    [2495, 22.2, 5.8, 1.72, 54, 6, 0.105, 0.12, 0, 2.84, 155, 15.9, 477],
    [694, 7.5, 2.6, 0.87, 16, 0, 0.1, 0, 0, 0.71, 14, 1.1, 4],
    [1032, 9.7, 6.4, 1.44, 56, 0, 0.638, 0.035, 0, 0.8, 12, 1.5, 448],
    [208, 0.5, 3, 0.36, 11, 2, 0.029, 0, 0, 0.08, 0, 0, 2],
    [452, 3.1, 3.5, 0.6, 5, 5, 0.06, 0.06, 9, 0.6, 31, 1.6, 8],
    [733, 3.8, 3.8, 0.96, 10, 1, 0.11, 0.06, 0, 0.43, 26, 2.8, 230],
    [261, 5.2, 6.1, 1.6, 27, 11, 0.211, 0.05, 30, 1.8, 59, 1.14, 3],
    [411, 3.2, 1.2, 0.02, 115, 0, 0.04, 0.215, 66, 0.36, 3, 0, 54],
    [2386, 19.7, 11, 3.77, 267, 0, 0.19, 0.07, 0, 3.55, 37, 4.5, 0],
    [270, 3.3, 0, 0.02, 106, 0, 0.022, 0.183, 44, 0.33, 5, 0.26, 35],
    [184, 0.6, 1.3, 0.32, 4, 10, 0, 0.022, 38, 0.18, 18, 0.4, 8],
    [79, 0.9, 1, 0.79, 20, 5, 0.01, 0.01, 62, 0.14, 19, 0.3, 52],
    [381, 4.8, 4.8, 1.01, 39, 2, 0.045, 0.02, 5, 0.51, 50, 0.3, 298],
    [598, 29.8, 0, 0.4, 5, 0, 0.11, 0.03, 0, 0.68, 54, 6.9, 43],
    [1031, 16.4, 0.4, 1.37, 11, 1, 0, 0.32, 58, 3.05, 0, 3.7, 788]
]

# Recommended nutritional requirements
# https://www.eatforhealth.gov.au/nutrient-reference-values
# Adult female 19-30 years
# A maximum value of None indicates there is no upper limit
DMIN = [9600, 46, 25, 18, 1000, 45, 1.1, 1.1, 700, 8, 400, 14, 460]
DMAX = [9600, None, None, 45, 2500, None, None, None, 3000, 40, 1000, 35, 920]

m = gp.Model("Cost of Subsistence")

#Variables
X = {}
for f in range(len(Foods)):
    X[f] = m.addVar()

#Objective (minimum cost of diet)
m.setObjective(gp.quicksum(C[f]*X[f] for f in range(len(Foods))), gp.GRB.MINIMIZE)

#Add constraints
for n in range(len(Nutrients)):
    m.addConstr(gp.quicksum(NV[f][n]*X[f] for f in range(len(Foods))) >= DMIN[n])
    if DMAX[n] is not None:
        m.addConstr(gp.quicksum(NV[f][n]*X[f] for f in range(len(Foods))) <= DMAX[n])

m.optimize()

for f in F:
    if X[f].x:
        print(Foods[f], 100*X[f].x) #*100 since untis are 100g

print(f"Cost = ${m.ObjVal}")

print("Nutrients")
for n in range(len(Nutrients)):
    print(Nutrients[n]), sum(NV[f][n]*X[f].x for f in range(len(Foods)))