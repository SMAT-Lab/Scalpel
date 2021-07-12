import os
import numpy as np
import sys, unicodedata
tbl = dict.fromkeys(i for i in range(sys.maxunicode)
                    if unicodedata.category(chr(i)).startswith('P'))
for root,dirs, files in os.walk('tsv_files/'):
    tsv_list = [file for file in files if file[-3:]=="tsv"]
whole_class_info=[[],[],[]]
with open(root+"assess_pregnancy.tsv") as cur_tsv:
    separated_data = [line.split('\t') for line in cur_tsv.readlines()]
    separated_data = np.asarray(separated_data)
    data = separated_data[:,0]
    labels = separated_data[:,1]
    labels = [int(label) for label in labels]
    for idx,label in enumerate(labels):
        whole_class_info[label].append(data[idx].translate(tbl))
    for idx, item in enumerate(whole_class_info):
        with open("preg"+os.sep+str(idx)+".txt","w+") as write_f:
            write_f.write("\n".join(item))
whole_class_info[2][1]