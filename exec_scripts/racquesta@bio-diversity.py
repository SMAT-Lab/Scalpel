#!/usr/bin/env python
# coding: utf-8
# In[1]:
#dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, desc
# In[2]:
engine = create_engine("sqlite:///DataSets/belly_button_biodiversity.sqlite")
# In[3]:
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
# In[4]:
# store tables
# In[5]:
Otu = Base.classes.otu
Samples = Base.classes.samples
Samples_metadata = Base.classes.samples_metadata
# In[6]:
#create session 
session = Session(engine)
# In[7]:
sample_names = Samples.__table__.columns
sample_names_ls = [name.key for name in sample_names]
# for name in sample_names:
#     print(name.key)
sample_names_ls.remove("otu_id")
sample_names_ls
# In[8]:
otu_data = session.query(Otu).first()
otu_data.__dict__
# In[9]:
samples = session.query(Samples).first()
samples.__dict__
# In[10]:
samples_metadata_ex = session.query(Samples_metadata).first()
samples_metadata_ex.__dict__
# In[11]:
otu_descriptions = session.query(Otu.lowest_taxonomic_unit_found).all()
otu_descriptions
# In[12]:
otu_descriptions_list = [x for (x), in otu_descriptions]
# In[13]:
otu_descriptions_list
# In[14]:
# def sample_query(sample):
#     sample_input = sample.replace("BB_", "")
#     result = session.query(Samples_metadata).filter(Samples_metadata.SAMPLEID == sample_input).all()
# sample_input = sample.replace("BB_", "")
result = session.query(Samples_metadata.AGE, Samples_metadata.BBTYPE, Samples_metadata.ETHNICITY, Samples_metadata.GENDER, Samples_metadata.LOCATION, Samples_metadata.SAMPLEID).filter_by(SAMPLEID = "940").all()
record = result[0]
result_dict = {
    "AGE": record[0],
    "BBTYPE": record[1],
    "ETHNICITY": record[2],
    "GENDER": record[3],
    "LOCATION": record[4],
    "SAMPLEID": record[5]
}
# In[15]:
result_dict
# In[16]:
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
sample_query("BB_940")
# In[17]:
result = session.query(Samples_metadata.WFREQ).filter_by(SAMPLEID = "940").all()
wash_freq = result[0][0]
wash_freq
# In[18]:
def otu_data(sample):
    sample_query = "Samples." + sample
    result = session.query(Samples.otu_id, sample_query).order_by(desc(sample_query)).all()
    otu_ids = [result[x][0] for x in range(len(result))]   
    sample_values = [result[x][1] for x in range(len(result))]
    dict_list = [{"otu_ids": otu_ids}, {"sample_values": sample_values}]
    return dict_list
# In[19]:
otu_data("BB_940")
# In[21]:
otu_descriptions = session.query(Otu.otu_id, Otu.lowest_taxonomic_unit_found).all()
otu_dict = {}
for row in otu_descriptions:
    otu_dict[row[0]] = row[1]
otu_dict
# In[22]:
otu_dict