#!/usr/bin/env python
# coding: utf-8
# In[1]:
#Import Dependencies
import pandas as pd                                                          
import numpy as np                                                      
import sqlalchemy 
from sqlalchemy.ext.automap import automap_base                             
from sqlalchemy.orm import Session                                          
from sqlalchemy import create_engine, desc                                  
# In[2]:
#Read in the CSV files for the DataSet
meta_pd = pd.read_csv("./DataSets/Belly_Button_Biodiversity_Metadata.csv") 
#OTU stands for Operational Taxonomy Unit
otu_pd = pd.read_csv("./DataSets/belly_button_biodiversity_otu_id.csv")     
samples_pd = pd.read_csv("./DataSets/belly_button_biodiversity_samples.csv") 
#This dataframe explains the meaning of the columns named in the metadata file
columns_pd = pd.read_csv("./DataSets/metadata_columns.csv") 
# In[3]:
#Inspecting the MetaData
meta_pd.tail()
meta_pd.dtypes
meta_pd.count()
# In[4]:
#Inspecting the Operational Taxonomy Unit Data
otu_pd.head()
otu_pd.dtypes
# In[5]:
#Inspecting the Samples DataSet
samples_pd
samples_pd.dtypes.head()
# In[6]:
#Displaying the Info about the Columns in the MetaData file
columns_pd
# In[7]:
# initializes SQLAlchemy engine for sqllite datasource specified in assignment
engine = create_engine("sqlite:///DataSets/belly_button_biodiversity.sqlite")
# In[8]:
#Initializes the Base and reflects data to notebook
Base = automap_base()                                                        
Base.prepare(engine, reflect=True)                                           
# In[9]:
#Displays the keys for the Base
Base.classes.keys()
# In[10]:
#Initializes the objects for the data
Otu = Base.classes.otu                                                      
Samples = Base.classes.samples
Samples_metadata = Base.classes.samples_metadata
# In[11]:
#Starts the session and acquires internal table object
session = Session(engine)                                               
samples = Samples.__table__.columns                                         
samples_list = [sample.key for sample in samples]                         
# In[12]:
#Inspect and clean up the list of sample names
#samples_list.remove("otu_id")
#samples_list
# In[13]:
#Inspect data and convert it into a dictionary 
otu_data = session.query(Otu).first() 
otu_data.__dict__
# In[14]:
#Check out the data and convert it into a dictionary
samples = session.query(Samples).first()                                    
samples.__dict__                                                             
# In[15]:
samples_metadata_ex = session.query(Samples_metadata).first() 
samples_metadata_ex.__dict__  
# In[26]:
otu_descriptions = session.query(Otu.lowest_taxonomic_unit_found).all() 
#otu_descriptions   
# In[28]:
#Using the list comprehension enables you to put it into a workable format
otu_descriptions_list = [x for (x), in otu_descriptions]  
#otu_descriptions_list 
# In[18]:
#Returns a dictionary of metadata for a given sample
def sample_query(sample):
    sample_name = sample.replace("BB_", "")
    result = session.query(Samples_metadata.AGE, Samples_metadata.BBTYPE, Samples_metadata.ETHNICITY, Samples_metadata.GENDER, Samples_metadata.LOCATION, Samples_metadata.SAMPLEID).filter_by(SAMPLEID = sample_name).all()
    record = result[0]
    record_dict = {
        "AGE": record[0],
        "BBTYPE": record[1],
        "ETHNICITY": record[2],
        "GENDER": record[3],
        "LOCATION": record[4],
        "SAMPLEID": record[5]
    }
    return (record_dict)
# In[19]:
sample_query("BB_940") 
# In[20]:
# queries metadata table
result = session.query(Samples_metadata.WFREQ).filter_by(SAMPLEID = "940").all()
# In[21]:
#Here we got an integer value for the weekly washing frequency 'WFREQ'
wash_freq = result[0][0] 
wash_freq  
# In[22]:
def otu_data(sample):
    sample_query = "Samples." + sample
    result = session.query(Samples.otu_id, sample_query).order_by(desc(sample_query)).all()
    otu_ids = [result[x][0] for x in range(len(result))]   
    sample_values = [result[x][1] for x in range(len(result))]
    dict_list = [{"otu_ids": otu_ids}, {"sample_values": sample_values}]
    return dict_list
# In[23]:
otu_data("BB_940") 
# In[24]:
#Creates queries for the otu table
otu_descriptions = session.query(Otu.otu_id, Otu.lowest_taxonomic_unit_found).all()
otu_dict = {}
for row in otu_descriptions:                                    
    otu_dict[row[0]] = row[1]
    
# In[57]:
#Now we have a dictionary of OTU data for use in our Flask app
otu_dict