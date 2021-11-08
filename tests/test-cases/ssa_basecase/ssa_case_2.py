# Imports
import os
import random

htid = "wu.89079728994"
# Get HTEF data for this ID; specifically tokenlist
fr = FeatureReader(ids=[htid])
for vol in fr:
    tokens = vol.tokenlist()
