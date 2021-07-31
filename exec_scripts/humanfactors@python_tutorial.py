#!/usr/bin/env python
# coding: utf-8
# In[3]:
# Method 1: os.listdir()
import os
data_dir = "data/"
for file in os.listdir(data_dir):
    if file.endswith(".txt"):
#         print(file)
        full_file_location = os.path.join(data_dir, file)
        print(full_file_location)
# In[4]:
# Method 2: glob
import glob
for file in glob.glob("./data/*.txt"):
    print(file)
# In[5]:
import glob
import os
for file in glob.glob("./data/*.txt"):
        # print the filename without folder
        print(os.path.basename(file))
        # Open file
        opened_file = open(file, 'r')
        # Read the file
        read_file = opened_file.readlines()
        for line in read_file:
            print(line)
# In[10]:
import glob
import os
full_results_list = []
for file in sorted(glob.glob("./data/*.txt")):
        opened_file = open(file, 'r')
        read_file = opened_file.readlines()
        participant_id = os.path.basename(file)
        
        for line in read_file:
            if "1." in line:
                response_q1 = line
            if "2." in line:
                response_q2 = line
        results = [participant_id, response_q1, response_q2]
        full_results_list.append(results)
        
print(full_results_list[0])
# In[11]:
import glob
import os
full_results_list = []
for file in sorted(glob.glob("./data/*.txt")):
        opened_file = open(file, 'r')
        read_file = opened_file.readlines()
        results = [os.path.basename(file)]
        
        # Notice here it's treating each new line as a new result!
        # Obviously you need to know what you data looks like to know if this is safe!
        for line in read_file:
            results.append(line)
        full_results_list.append(results)
for item in full_results_list:
    print(item)
## We can also apply formatting at this point to inspect what's going on
#     print(item[0])
#     print(item[1])
#     print(item[2])
# In[12]:
import glob
import os
full_results_list = []
for file in sorted(glob.glob("./data/*.txt")):
        opened_file = open(file, 'r')
        read_file = opened_file.readlines()
        # Here we use another function from OS to get just the base, and we tell it to strip the file name
        results = [os.path.splitext(os.path.basename(file))[0].strip()]
        
        for line in read_file:
            # Here we use square brackets to say only read from the third character onwards
            # Then we tell it to strip, which by default removes \n from the string
            line = line[2:].strip()
            results.append(line)
            
        full_results_list.append(results)
print(full_results_list)
# In[13]:
import glob
import os
import csv
full_results_list = []
for file in sorted(glob.glob("./data/*.txt")):
        opened_file = open(file, 'r')
        read_file = opened_file.readlines()
        results = [os.path.splitext(os.path.basename(file))[0]]
        for line in read_file:
            line = line[2:].strip()
            results.append(line)
        full_results_list.append(results)
        
with open('final_results.csv', 'w') as csvfile:
    my_writer = csv.writer(csvfile)
    my_writer.writerows(full_results_list)
        
    