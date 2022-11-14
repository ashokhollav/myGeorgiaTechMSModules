'''
Please add to your model the following constraints (which might require adding more variables)
and solve the new model:
a. If a food is selected, then a minimum of 1/10 serving must be chosen. (Hint: now you will
need two variables for each food i: whether it is chosen, and how much is part of the diet.
You’ll also need to write a constraint to link them.)

b. Many people dislike celery and frozen broccoli. So at most one, but not both, can be
selected.
c. To get day-to-day variety in protein, at least 3 kinds of meat/poultry/fish/eggs must be
selected. [If something is ambiguous (e.g., should bean-and-bacon soup be considered
meat?), just call it whatever you think is appropriate – I want you to learn how to write this
type of constraint, but I don’t really care whether we agree on how to classify foods!]
'''

from variables import *
from pulp import *



# Create the 'prob' variable to contain the problem data
prob = LpProblem("The Army Diet Problem", LpMinimize)


# additional variables
food_chosen = LpVariable.dicts("Chosen",food_items,0,1,cat='Integer')

#Food portion with lower bound = 0
ingredient_vars = LpVariable.dicts("Portion",food_items,0,cat='Continuous')



# The objective function is added to 'prob' first
prob += lpSum([costs[i]*ingredient_vars[i] for i in food_items]), "Total Cost of food_items per food"

# Constraints
#                       Calories	Cholesterol mg	Total_Fat g	Sodium mg	Carbohydrates g	Dietary_Fiber g	Protein g	Vit_A IU	Vit_C IU	Calcium mg	Iron mg
# Minimum daily intake	1500	    30	            20	        800	            130	            125	            60	        1000	    400	        700	    10
#Maximum daily intake	2500	    240	            70	        2000	        450	            250	            100	        10000	    5000	    1500	40



#Add the constraints based on the table above

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

#Additional Constraints

#Adding constraint linking ingredient_vars and food_chosen

for i in food_items:
    #If a food is selected, then a minimum of 1/10 serving must be chosen.
    prob += ingredient_vars[i] >= food_chosen[i]*0.1

    #No upper bound so select any max, 1e5 this case
    prob += ingredient_vars[i] <= food_chosen[i]*1e5

#Adding constraint of celery and frozen broccoli, either celery or broccoli can be picked not both to satisfy the condition
# i.e. celery=0 + broccoli=1 or celery=1 + broccoli=0
prob += food_chosen['Frozen Broccoli']+food_chosen['Celery, Raw']<=1

'''
To get day-to-day variety in protein, at least 3 kinds of meat/poultry/fish/eggs must be
selected. [If something is ambiguous (e.g., should bean-and-bacon soup be considered
meat?), just call it whatever you think is appropriate – I want you to learn how to write this
type of constraint, but I don’t really care whether we agree on how to classify foods!]

'''
#Adding protein choices
protein_choices = ['Beanbacn Soup,W/Watr','Bologna,Turkey','Frankfurter, Beef','Ham,Sliced,Extralean',
                  'Hamburger W/Toppings','Hotdog, Plain','Kielbasa,Prk','Neweng Clamchwd','Pizza W/Pepperoni',
                  'Poached Eggs','Pork','Roasted Chicken','Sardines in Oil','Scrambled Eggs','Vegetbeef Soup',
                   'White Tuna in Water']

#Atleast 3 proteins need to be chosen
prob += lpSum([food_chosen[p] for p in protein_choices]) >= 3.0



# The problem data is written to an .lp file
prob.writeLP("ArmyDiet_2.lp")

# The problem is solved using PuLP's choice of Solver
prob.solve()

# The status of the solution is printed to the screen
print ("Status:{}".format(LpStatus[prob.status]))

# Each of the variables is printed with it's resolved optimum value
for v in prob.variables():
    if v.varValue>0 :
        print("{}={}".format(v.name, v.varValue))

# The optimised objective function value is printed to the screen    
print ("Total Cost of food_items per can = {}".format( value(prob.objective)))

'''
Output:

Status:Optimal

Chosen Ingredients:

Chosen_Celery,_Raw=1.0
Chosen_Kielbasa,Prk=1.0
Chosen_Lettuce,Iceberg,Raw=1.0
Chosen_Oranges=1.0
Chosen_Peanut_Butter=1.0
Chosen_Poached_Eggs=1.0
Chosen_Popcorn,Air_Popped=1.0
Chosen_Scrambled_Eggs=1.0

Portion sizes:

Portion_Celery,_Raw=42.399358
Portion_Kielbasa,Prk=0.1
Portion_Lettuce,Iceberg,Raw=82.802586
Portion_Oranges=3.0771841
Portion_Peanut_Butter=1.9429716
Portion_Poached_Eggs=0.1
Portion_Popcorn,Air_Popped=13.223294
Portion_Scrambled_Eggs=0.1

Total Cost:

Total Cost of food_items per can = 4.512543427000001

'''