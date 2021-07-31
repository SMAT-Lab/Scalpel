#!/usr/bin/env python
# coding: utf-8
# In[1]:
import pandas as pd
import numpy as np
# In[2]:
dg_links = pd.read_csv("dg_links/orpha_gene_dise_links.tsv", sep='\t')
# In[3]:
dg_links.head(2)
# In[4]:
genes = (pd
    .read_csv("data/hetnet_nodes.csv")
    .drop("identifier:string", axis=1)
    .rename(columns={
        ":ID": "entrez_id",
        "name:string": "gene_name",
        ":LABEL": "node_type"
    })
    .query("node_type == 'Gene'")
    .drop("node_type", axis=1)
    .astype({"entrez_id": np.int64})
)
# In[5]:
genes.shape
# In[6]:
genes.head()
# In[7]:
fin_links = (dg_links
    .merge(
        genes.drop("gene_name", axis=1), how="inner", on="entrez_id"
    )
)
# In[8]:
fin_links.shape
# In[9]:
fin_links.head()
# In[10]:
dg_links["entrez_id"].nunique()
# In[11]:
fin_links["entrez_id"].nunique()
# In[12]:
fin_links[["entrez_id", "dise_orpha_id"]].drop_duplicates().shape
# In[13]:
inds = (pd
    .read_csv("cd_links/rare_disease_indications.tsv", sep='\t')
    .query("relationship_name != 'contraindication'")
)
# In[14]:
inds.head(2)
# In[15]:
inds["struct_id"].nunique()
# In[16]:
drugs = (pd
    .read_csv("data/hetnet_nodes.csv")
    .drop("identifier:string", axis=1)
    .rename(columns={
        ":ID": "drugbank_id",
        "name:string": "drug_name",
        ":LABEL": "node_type"
    })
    .query("node_type == 'Compound'")
    .drop("node_type", axis=1)
)
# In[17]:
drugs.head()
# In[18]:
drugs["drugbank_id"].nunique()
# In[19]:
chem_ids = (pd
    .read_csv("data/drug_ids.csv")
    .drop(["id", "parent_match"], axis=1)
)
# In[20]:
chem_ids.head()
# In[21]:
chem_ids["id_type"].value_counts()
# In[22]:
chem_map = (chem_ids
    .query("id_type == 'DRUGBANK_ID'")
    .drop("id_type", axis=1)
    .rename(columns={"identifier": "drugbank_id"})
)
# In[23]:
drugs = drugs.merge(chem_map, how="inner", on="drugbank_id")
# In[24]:
drugs.shape
# In[25]:
drugs.head()
# In[26]:
drugs["drugbank_id"].nunique()
# In[27]:
drugs["struct_id"].nunique()
# In[28]:
fin_inds = (inds
    .drop("drug_name", axis=1)
    .merge(drugs, how="inner", on="struct_id")
    .drop("struct_id", axis=1)
    .drop_duplicates()
)
# In[29]:
common_dises = set(fin_links["dise_orpha_id"])
fin_inds = fin_inds.query("orphanet_id in @common_dises")
# In[30]:
fin_inds.shape
# In[31]:
fin_inds.head()
# In[32]:
fin_inds["orphanet_id"].nunique()
# In[33]:
fin_inds["drugbank_id"].nunique()
# In[34]:
fin_inds[["drugbank_id", "orphanet_id"]].drop_duplicates().shape
# In[35]:
fin_links["dise_orpha_id"].nunique()
# In[36]:
fin_links["entrez_id"].nunique()
# In[37]:
fin_links[["entrez_id", "dise_orpha_id"]].drop_duplicates().shape
# In[38]:
fin_links.head()
# In[39]:
len(set(fin_links["dise_orpha_id"]) & set(fin_inds["orphanet_id"]))
# In[40]:
fin_inds.to_csv("results/rare_dise_indications.tsv", sep='\t', index=False)
fin_links.to_csv("results/rare_dise_gene_links.tsv", sep='\t', index=False)