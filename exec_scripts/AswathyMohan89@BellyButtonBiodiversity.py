#!/usr/bin/env python
# coding: utf-8
# In[1]:
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random
import os
# In[4]:
engine = create_engine(os.path.join("sqlite:///","DataSets","belly_button_biodiversity.sqlite"),echo=False)
conn = engine.connect()
# In[5]:
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)
# Print all of the classes mapped to the Base
Base.classes.keys()
# In[12]:
otu_db = Base.classes.otu
samples_db = Base.classes.samples
samples_meta_db = Base.classes.samples_metadata
session = Session(engine)
# In[13]:
first_row = session.query(samples_db).first()
first_row.__dict__
# In[86]:
samples_cols_list=Base.classes.samples.__table__.columns.keys()
samples_cols_list[1:]
# In[89]:
taxonomy_list=[]
result_taxonomy = session.query(otu_db.lowest_taxonomic_unit_found).all()
taxonomy_list.append(result_taxonomy)
taxonomy_list
# In[57]:
sample="BB_960"
sample=sample.split("_")[1]
result_sample = session.query(samples_meta_db.AGE,samples_meta_db.BBTYPE,samples_meta_db.ETHNICITY,samples_meta_db.GENDER,                       samples_meta_db.LOCATION,samples_meta_db.SAMPLEID).filter(samples_meta_db.SAMPLEID==sample).first()
result_sample
# In[58]:
sample_dict={}
#di{"Age":result[0],"BBTYPE":result[1],"ETHNICITY":result[2],"GENDER":result[3],"LOCATION":result[3],"SAMPLEID":result[4]}
# In[59]:
names = ["Age", "BBTYPE", "ETHNICITY","GENDER","LOCATION","SAMPLEID"]
for i in range(len(names)):
    sample_dict[names[i]]=result_sample[i]
# In[60]:
sample_dict
# In[62]:
sample="BB_960"
sample=sample.split("_")[1]
result_wfreq= session.query(samples_meta_db.WFREQ).filter(samples_meta_db.SAMPLEID==sample).first()
result_wfreq[0]
# In[70]:
s="BB_940"
result_samples_desc = session.query(samples_db.otu_id,getattr(samples_db, s)).order_by(getattr(samples_db, s).desc()).all()
result_samples_desc
# In[78]:
otu_list=[]
sample_list=[]
for i in result_samples_desc:
    otu_list.append(i[0])
    sample_list.append(i[1])
    
# In[80]:
sample_otu_dict={}
sample_otu_dict["otu_ids"]=otu_list
sample_otu_dict["sample_values"]=sample_list
# In[85]:
sample_otu_list=[]
sample_otu_list.append(sample_otu_dict)
sample_otu_list