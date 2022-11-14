'''
1. Formulate an optimization model (a linear program) to find the cheapest diet that satisfies the
maximum and minimum daily nutrition constraints, and solve it using PuLP. Turn in your code
and the solution. (The optimal solution should be a diet of air-popped popcorn, poached eggs,
oranges, raw iceberg lettuce, raw celery, and frozen broccoli. UGH!)
'''

from variables import *
from pulp import *

# Create the 'prob' variable to contain the problem data
prob = LpProblem("The Army Diet Problem", LpMinimize)

#Food portion with lower bound = 0
ingredient_vars = LpVariable.dicts("Portion",food_items,0,cat='Continuous')

# The objective function is added to 'prob' first
prob += lpSum([costs[i]*ingredient_vars[i] for i in food_items]), "Total Cost of Ingredients per food"

# Constraints
#                       Calories	Cholesterol mg	Total_Fat g	Sodium mg	Carbohydrates g	Dietary_Fiber g	Protein g	Vit_A IU	Vit_C IU	Calcium mg	Iron mg
# Minimum daily intake	1500	    30	            20	        800	            130	            125	            60	        1000	    400	        700	    10
#Maximum daily intake	2500	    240	            70	        2000	        450	            250	            100	        10000	    5000	    1500	40


# Add the other constraints based on the constraints table above

prob += lpSum([calories[i] * ingredient_vars[i] for i in food_items]) >=1500.0, "Calories Min"
prob += lpSum([calories[i] * ingredient_vars[i] for i in food_items]) <=2500.0, "Calories Max"


prob += lpSum([cholestral[i] * ingredient_vars[i] for i in food_items]) >=30, "Cholesterol Min"
prob += lpSum([cholestral[i] * ingredient_vars[i] for i in food_items]) <=240, "Cholesterol Max"

prob += lpSum([totalfat[i] * ingredient_vars[i] for i in food_items]) >= 20, "Total_Fat Min"
prob += lpSum([totalfat[i] * ingredient_vars[i] for i in food_items]) <= 70, "Total_Fat Max"

prob += lpSum([sodium[i] * ingredient_vars[i] for i in food_items]) >= 800, "Sodium Min"
prob += lpSum([sodium[i] * ingredient_vars[i] for i in food_items]) <= 2000, "Sodium Max"

prob += lpSum([carbs[i] * ingredient_vars[i] for i in food_items]) >= 130, "Carbohydrates Min"
prob += lpSum([carbs[i] * ingredient_vars[i] for i in food_items]) <=450, "Carbohydrates Max"

prob += lpSum([fiber[i] * ingredient_vars[i] for i in food_items]) >= 125, "Dietary_Fiber Min"
prob += lpSum([fiber[i] * ingredient_vars[i] for i in food_items]) <= 250, "Dietary_Fiber Max"

prob += lpSum([protein[i] * ingredient_vars[i] for i in food_items]) >= 60, "Protein Min"
prob += lpSum([protein[i] * ingredient_vars[i] for i in food_items]) <= 100, "Protein Max"

prob += lpSum([vit_a[i] * ingredient_vars[i] for i in food_items]) >= 1000, "Vit_A Min"
prob += lpSum([vit_a[i] * ingredient_vars[i] for i in food_items]) <= 10000, "Vit_A Max"

prob += lpSum([vit_c[i] * ingredient_vars[i] for i in food_items]) >= 400, "Vit_C Min"
prob += lpSum([vit_c[i] * ingredient_vars[i] for i in food_items]) <= 5000, "Vit_C Max"

prob += lpSum([calcium[i] * ingredient_vars[i] for i in food_items]) >= 400, "Calcium Min"
prob += lpSum([calcium[i] * ingredient_vars[i] for i in food_items]) <= 1500, "Calcium Max"

prob += lpSum([iron[i] * ingredient_vars[i] for i in food_items]) >= 10, "Iron Min"
prob += lpSum([iron[i] * ingredient_vars[i] for i in food_items]) <= 40, "Iron Max"

# The problem data is written to an .lp file
prob.writeLP("ArmyDiet.lp")

# The problem is solved using PuLP's choice of Solver
prob.solve()

# The status of the solution is printed to the screen
print ("Status:{}".format(LpStatus[prob.status]))

# Each of the variables is printed with it's resolved optimum value
for v in prob.variables():
    if v.varValue>0:
        print("{}={}".format(v.name, v.varValue))

# The optimised objective function value is printed to the screen    
print ("Total Cost of Ingredients per can = {}".format( value(prob.objective)))

'''
Output: The optimal solution is:

Portion_Celery,_Raw=52.64371
Portion_Frozen_Broccoli=0.25960653
Portion_Lettuce,Iceberg,Raw=63.988506
Portion_Oranges=2.2929389
Portion_Poached_Eggs=0.14184397
Portion_Popcorn,Air_Popped=13.869322

Total Cost of Ingredients per can = 4.337116797399999
'''