#!/usr/bin/env python
# coding: utf-8
# In[1]:
import pandas as pd
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, distinct
from flask import(
    Flask,
    render_template,
    jsonify
)
# In[2]:
# Database Setup
engine = create_engine("sqlite:///db/winter_olympics.sqlite")
# reflect existing database into new model
Base = automap_base()
# reflect tables
Base.prepare(engine, reflect=True)
# save reference to tables
medals = Base.classes.medals
# create session to query tables
session = Session(engine)
# create inspector to get column names
inspector = inspect(engine)
# In[3]:
#set filters
gender = 'Women'
medal_type = 'gold'
# In[4]:
# get medal info
#filter by medal type and gender
if gender!='both' and medal_type!='all':
    number_of_events_with_medal_wins = session.query(medals.year,medals.country,func.count(distinct(medals.sport))).filter(medals.gender==gender).filter(medals.medal==medal_type).group_by(medals.year).group_by(medals.country).all() 
    number_of_medal_wins = session.query(medals.year,medals.country,func.count(medals.sport)).group_by(medals.year).filter(medals.gender==gender).filter(medals.medal==medal_type).group_by(medals.country).all()
#just filter by type of medal
elif gender=='both' and medal_type!='all':
    number_of_events_with_medal_wins = session.query(medals.year,medals.country,func.count(distinct(medals.sport))).filter(medals.medal==medal_type).group_by(medals.year).group_by(medals.country).all() 
    number_of_medal_wins = session.query(medals.year,medals.country,func.count(medals.sport)).group_by(medals.year).filter(medals.medal==medal_type).group_by(medals.country).all()
#just filter by gender
elif gender!='both' and medal_type=='all':
    number_of_events_with_medal_wins = session.query(medals.year,medals.country,func.count(distinct(medals.sport))).filter(medals.gender==gender).group_by(medals.year).group_by(medals.country).all() 
    number_of_medal_wins = session.query(medals.year,medals.country,func.count(medals.sport)).group_by(medals.year).filter(medals.gender==gender).group_by(medals.country).all() 
#no filter
else:
    number_of_events_with_medal_wins = session.query(medals.year,medals.country,func.count(distinct(medals.sport))).group_by(medals.year).group_by(medals.country).all() 
    number_of_medal_wins = session.query(medals.year,medals.country,func.count(medals.sport)).group_by(medals.year).group_by(medals.country).all() 
# In[5]:
number_of_events_with_medal_wins
# In[6]:
number_of_medal_wins
# In[7]:
genders = session.query(distinct(medals.gender)).all()
genders