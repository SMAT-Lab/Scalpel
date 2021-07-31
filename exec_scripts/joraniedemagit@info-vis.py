#!/usr/bin/env python
# coding: utf-8
# In[195]:
import pandas as pd
import json
from collections import defaultdict
pd.set_option('display.max_columns', None)
MIGRATION_THRESHOLD = 0 #500000
countries = {}
migrations = {'1990': {}, '1995': {}, '2000': {}, '2005': {}, '2010': {}, '2015': {}, '2017': {}}
citiesDF = pd.read_csv("data/cities.csv")
migrationsDF = pd.read_csv("data/unprocessedMigrations.csv")
# renaming columns
migrationsDF.rename(columns={'Russian Federation': 'Russia'}, inplace=True)
migrationsDF.head(20)
# In[196]:
# migrationsDF[migrationsDF['Major area, region, country or area of destination'] == 'Russian Federation']
migrationsDF[migrationsDF['Major area, region, country or area of destination'] == 'Russian Federation'] = migrationsDF[migrationsDF['Major area, region, country or area of destination'] == 'Russian Federation'].replace('Russian Federation', 'Russia')
# In[197]:
# migrationsDF[migrationsDF['Major area, region, country or area of destination'] == 'Russian Federation'] = 'Russia'
migrationsDF[migrationsDF['Major area, region, country or area of destination'] == 'Russia']
# In[198]:
rus1 = migrationsDF[migrationsDF['Major area, region, country or area of destination'] == 'Russia']
# rus2 = migrationsDF[migrationsDF['Major area, region, country or area of destination'] == 'Russian Federation']
rus1.shape
# rus2.shape
# In[199]:
for key, row in citiesDF.iterrows():
    country = row['country']
    city = row['city']
    lat = row['lat']
    lng = row['lng']
    coords = {}
    coords['country'] = country
    coords['city'] = city
    coords['latitude'] = lat
    coords['longitude'] = lng
    countries[country] = coords
# countries
# In[200]:
c = 0
for key, row in migrationsDF.iterrows():
    country = row['Major area, region, country or area of destination']
    year = row['Year']
    
    if country in countries:
        for origin, migrants in row.items():
            if origin in countries and country != origin and migrants.isdigit() and int(migrants) > MIGRATION_THRESHOLD:
                migration = {}
                
                migration['origin'] = countries[origin]
                migration['destination'] = countries[country]
                migration['migrants'] = migrants
                
                ###### 
                c+=1
#                 print('Country/destination: ', country)
#                 print('Origin: ', origin)
#                 print('Migrants: ', migrants)
    
                if not country in migrations[str(year)]:
                    migrations[str(year)][country] = []
                
                migrations[str(year)][country].append(migration) 
    
#     if c > 10:
#         break
    
    
    
# In[201]:
for m in migrations:
    print(len(migrations[m]))
# In[202]:
for i in range(1995,2016,5):
    print('\n\n\n\n\n\n==========   ', i, '   ======================================\n\n\n\n\n')
    year = migrations[str(i)]
    for country in year:
        print('\n\n\n')
#         print("1. Current country = ", country, '\n')
#         print('2. This year flows = \n', year[country], '\n')
        for flow in year[country]:
            if country in migrations[str(i-5)]:
                prev_year_migrants = migrations[str(i-5)][country] 
                
                if country in migrations[str(1990)]:
                    init_year_migrants = migrations[str(1990)][country]
                
                    # get initial migrants
                    if str(i-5) != str(1990):
                        for k in range(0, len(init_year_migrants)):
                            if init_year_migrants[k]['origin']['country'] == flow['origin']['country']:
#                                 print("\n5B. Country of origin = ", flow['origin']['country'])
                                initial_migrants = int(init_year_migrants[k]['migrants'])
                    else:
                        initial_migrants = 0
                else:
                    initial_migrants = 0
                
#                 print('3. Progress current flow,\n ', flow, '\n')
#                 print("4. Look if flow exists in prev year")
#                 print(prev_year_migrants)
                for c in range(0, len(prev_year_migrants)):
                    if prev_year_migrants[c]['origin']['country'] == flow['origin']['country']:
#                         print("\n M. Progress current country = ", country)
#                         print("\n5. Country of origin = ", flow['origin']['country'])
#                         print("INITIAL MIGRANTS: ", initial_migrants)
                        actual_migrants = int(flow['migrants']) - int(prev_year_migrants[c]['migrants']) - initial_migrants
                        
#                         print('Total migrants', i, ' = ', flow['migrants'])
#                         print('Total migrants', i-5, ' = ', prev_year_migrants[c]['migrants'])
#                         print('Actual migrants', i, ' = ', actual_migrants, '\n\n\n')
                        flow['migrants'] = actual_migrants
            else:
                print("ERROR COUNTRY NOT FOUND = ", country, ' \n YEAR = ', str(i))
            
# # migrations
# In[203]:
# set minimum migrations to 0
for i in range(1995,2016,5):
    year = migrations[str(i)]
    for country in year:
        for flow in year[country]:
            if int(flow['migrants']) < 0:
                flow['migrants'] = 0
            
# In[204]:
with open('data/migrations_final.json', 'w') as fp:
    json.dump(migrations, fp)