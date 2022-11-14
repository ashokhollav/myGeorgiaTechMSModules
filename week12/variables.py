import pandas as pd

df = pd.read_excel("data15.2/diet.xls",nrows=64)
#

# Creates a list of the Ingredients
food_items = list(df['Foods'])

# A dictionary of the costs of each of the Ingredients is created
costs = dict(zip(food_items,df['Price/ Serving']))

# Calories
calories = dict(zip(food_items,df['Calories']))


#Cholestral
cholestral =  dict(zip(food_items,df['Cholesterol mg']))

#Total Fat
totalfat = dict(zip(food_items,df['Total_Fat g']))

#Sodium mg	
sodium= dict(zip(food_items,df['Sodium mg']))

#Carbohydrates g	
carbs = dict(zip(food_items,df['Carbohydrates g']))

# Dietary_Fiber g	
fiber = dict(zip(food_items,df['Dietary_Fiber g']))

# Protein g	
protein = dict(zip(food_items,df['Protein g']))
# Vit_A IU	

vit_a=dict(zip(food_items,df['Vit_A IU']))

# Vit_C IU	
vit_c=dict(zip(food_items,df['Vit_C IU']))

# Calcium mg	

calcium=dict(zip(food_items,df['Calcium mg']))
# Iron mg

iron=dict(zip(food_items,df['Iron mg']))