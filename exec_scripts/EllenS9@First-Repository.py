#!/usr/bin/env python
# coding: utf-8
# In[47]:
name1="Ellie"
gender1 = "f"
height_m1 = 1.65
weight_kg1 = 55
name2="James"
gender2 = "m"
height_m2 = 1.70
weight_kg2 = 61.5
name3="Kate Moss"
gender3 = "f"
height_m3 = 1.7
weight_kg3 = 47
if(gender1== "f"):
    his_or_her1 = "her"
elif(gender1 == "m"):
    his_or_her1 = "his"
else:
    his_or_her1 = name1 + "'s"
if(gender2 == "f"):
    his_or_her2 = "her"
elif(gender2 == "m"):
    his_or_her2 = "his"
else:
    his_or_her2 = name + "'s"
if(gender3 == "f"):
    his_or_her3 = "her"
elif(gender3 == "m"):
    his_or_her3 = "his"
else:
    his_or_her3 = name + "'s"
    
bmi= weight_kg1/ (height_m1 ** 2)
print (name1, "'s BMI: ", bmi)
if bmi < 18:
    print (name + " is underweight. " + name1 +  "is suggested to increase " + his_or_her1 + " calorie intake & to get plenty of exercise.")
else:
    if 18< bmi <25:
        print (name1 + " is normal weight. It is suggested that " + name1 + " keep " + his_or_her1 + " calorie intake the same & maintain activity levels")
    if 25< bmi <30:
        print (name1 + " is overweight. It is suggested that " + name1 + " reviewed " + his_or_her1 + " calorie intake & activity levels")
    if bmi >30: 
        print (name1 + " is obese. It is suggested that " + name1 + " went to see a GP because there may be at risk of type 2 diabetes & heart disease.")
        
bmi2= weight_kg2/ (height_m2 ** 2)
print (name2, "'s BMI: ", bmi2)
if bmi2 < 18:
    print (name2 + " is underweight. " + name2 +  "is suggested to increase " + his_or_her2 + " calorie intake & to get plenty of exercise.")
else:
    if 18< bmi2 <25:
        print (name2 + " is normal weight. It is suggested that " + name2 + " keep " + his_or_her2 + " calorie intake the same & maintain activity levels")
    if 25< bmi2 <30:
        print (name2 + " is overweight. It is suggested that " + name2 + " reviewed " + his_or_her2 + " calorie intake & activity levels")
    if bmi2 >30: 
        print (name + " is obese. It is suggested that " + name2 + " went to see a GP because there may be at risk of type 2 diabetes & heart disease.")
        
bmi3= weight_kg3/ (height_m3 ** 2)
print (name3, "'s BMI: ", bmi3)
if bmi3 < 18:
    print (name3 + " is underweight. " + name3 +  "is suggested to increase " + his_or_her3 + " calorie intake & to get plenty of exercise.")
else:
    if 18< bmi3 <25:
        print (name3 + " is normal weight. It is suggested that " + name3 + " keep " + his_or_her3 + " calorie intake the same & maintain activity levels")
    if 25< bmi3 <30:
        print (name3 + " is overweight. It is suggested that " + name3 + " reviewed " + his_or_her3 + " calorie intake & activity levels")
    if bmi3 >30: 
        print (name3 + " is obese. It is suggested that " + name3 + " went to see a GP because there may be at risk of type 2 diabetes & heart disease.")