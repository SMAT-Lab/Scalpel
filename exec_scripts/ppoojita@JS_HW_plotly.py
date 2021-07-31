#!/usr/bin/env python
# coding: utf-8
# In[2]:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import warnings
import json 
# In[3]:
df = pd.read_csv('belly_button_biodiversity_otu_id.csv')
otu_df=df.set_index('otu_id')
# otu_df
# In[4]:
# json_otu=json.dumps(json.loads(otu_df.to_json(orient='index')), indent=2)
# json_otu= otu_df.to_json(orient='index'), indent=2
# print(json_otu)
      
# In[5]:
otu_desc = otu_df["lowest_taxonomic_unit_found"].tolist()
# otu_desc
# In[6]:
df1 = pd.read_csv('Belly_Button_Biodiversity_Metadata.csv')
metadata_df=df1.set_index('SAMPLEID')
# metadata_df
# In[7]:
json_metadata=metadata_df.to_json(orient='index')
# json_metadata
# In[8]:
metadata_dict = metadata_df.to_dict(orient="index")
# metadata_dict
# In[9]:
search_term=1517
metadata_dict[search_term]['WFREQ']
# for key, value in metadata_dict.items():   
#     if key == search_term:
#         print(value)
        
# In[10]:
df2 = pd.read_csv('belly_button_biodiversity_samples.csv')
samples_df=df2.set_index('otu_id')
# samples_df
# In[11]:
json_samples=json.dumps(json. loads(samples_df.to_json(orient='index')), indent=4)
print(json_samples)
# In[12]:
samples_header=list(samples_df.columns.values)
samples_header
# In[13]:
df3 = pd.read_csv('metadata_columns.csv')
metadata_col_df=df3.set_index('COLUMN')
# metadata_col_df
# In[14]:
json_metadata_col=json.dumps(json.loads(metadata_col_df.to_json(orient='index')), indent=6)
print(json_metadata_col)
# In[15]:
def get_num_from_string(string):  
    '''This function retrieves numbers from a string and converts them to integers'''  
    # Create empty string to store numbers as a string  
    num = ''  
    # Loop through characters in the string  
    for i in string:  
        # If one of the characters is a number, add it to the empty string  
        if i in '1234567890':  
            num+=i  
    # Convert the string of numbers to an integer  
    integer = int(num)  
    return integer  
# In[22]:
string="BB_940"
temp_df=samples_df[[string]]
temp_df = temp_df.sort_values(string, ascending=False)
temp_df=temp_df.fillna(0)
temp_df
sample_values = temp_df[string].tolist()
otu_id_list = temp_df.index.tolist()
otu_id_list=list(map(int, otu_id_list))
samples_dict = {"otu_id":otu_id_list, "sample_values":sample_values}
# print(samples_dict)
samples_list=[]
    
samples_list.append(dict(samples_dict))
print(samples_list[0])
# In[98]:
string="BB_940"
def get_num_from_string(string):  
        num = ''  
    # Loop through characters in the string  
        for i in string:  
            # If one of the characters is a number, add it to the empty string  
            if i in '1234567890':  
                num+=i  
        # Convert the string of numbers to an integer  
        integer = int(num)  
        return integer
    
# string= sample
    
sample_id = get_num_from_string(string)
# print(sample_id)
metadata_dict[sample_id]
sample_item={}
sample_item['AGE'] = metadata_dict[sample_id]['AGE']
sample_item['BBTYPE'] = metadata_dict[sample_id]['BBTYPE']
sample_item['ETHNICITY'] = metadata_dict[sample_id]['ETHNICITY']
sample_item['GENDER'] = metadata_dict[sample_id]['GENDER']
sample_item['LOCATION'] = metadata_dict[sample_id]['LOCATION']
sample_item['SAMPLEID'] = sample_id
print(sample_item)