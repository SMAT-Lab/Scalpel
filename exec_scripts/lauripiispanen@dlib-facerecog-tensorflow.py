#!/usr/bin/env python
# coding: utf-8
# In[4]:
import os
import shutil
import urllib.request
import tarfile
DATASET_URL = "http://vis-www.cs.umass.edu/lfw/lfw.tgz"
DESTINATION_DIR = "../data"
if not os.path.exists(os.path.join(DESTINATION_DIR, "lfw/George_W_Bush")):
    if not os.path.exists(DESTINATION_DIR):
        os.makedirs(DESTINATION_DIR)
        print("Created destination directory for LFW dataset")
    
    dest_file_name = os.path.join(DESTINATION_DIR, os.path.basename(DATASET_URL))
    if not os.path.exists(dest_file_name):
        print("Downloading dataset...", end='')
        with urllib.request.urlopen(DATASET_URL) as response, open(dest_file_name, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
            print(".", end='')
        print("done!")
    
    print("Extracting dataset...", end='')
    tarfile.open(dest_file_name, mode='r').extractall(path=DESTINATION_DIR)
    print("done!")