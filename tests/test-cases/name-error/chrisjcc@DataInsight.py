#!/usr/bin/env python
# coding: utf-8
# In[1]:
# Load required packages
library(survival)
library(survminer)
library(dplyr)
# In[2]:
# Import the ovarian cancer dataset and have a look at it
data(ovarian)
glimpse(ovarian)
# In[3]:
# Dichotomize age and change data labels
ovarian$rx <- factor(ovarian$rx, 
                     levels = c("1", "2"), 
                     labels = c("A", "B"))
ovarian$resid.ds <- factor(ovarian$resid.ds, 
                           levels = c("1", "2"), 
                           labels = c("no", "yes"))
ovarian$ecog.ps <- factor(ovarian$ecog.ps, 
                          levels = c("1", "2"), 
                          labels = c("good", "bad"))
# In[4]:
# Data seems to be bimodal
hist(ovarian$age) 
# In[5]:
# Set cutoff of 50 years.
ovarian <- ovarian %>% mutate(age_group = ifelse(age >=50, "old", "young"))
# Convert the future covariates into factors.
ovarian$age_group <- factor(ovarian$age_group)
# In[6]:
# Fit survival data using the Kaplan-Meier method
surv_object <- Surv(time = ovarian$futime, event = ovarian$fustat)
surv_object 
# In[7]:
fit1 <- survfit(surv_object ~ rx, data = ovarian)
summary(fit1)
# In[8]:
# Examine the corresponding survival curve
ggsurvplot(fit1, 
           data = ovarian, 
           pval = TRUE # it plots the p-value of a log-rank test as well.
          )
# In[9]:
# Examine prdictive value of residual disease status
fit2 <- survfit(surv_object ~ resid.ds, data = ovarian)
ggsurvplot(fit2, data = ovarian, pval = TRUE)
# In[10]:
# Fit a Cox proportional hazards model
fit.coxph <- coxph(surv_object ~ rx + resid.ds + age_group + ecog.ps, 
                   data = ovarian)
ggforest(fit.coxph, data = ovarian)