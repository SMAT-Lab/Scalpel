#!/usr/bin/env python
# coding: utf-8
# In[4]:
nipype.get_info()
# In[28]:
get_ipython().run_line_magic('matplotlib', 'inline')
import os
import numpy as np
import matplotlib.pyplot as plt
# In[30]:
# download the files from: https://github.com/Neurita/nipype-tutorial-data/archive/master.zip
import os.path as op
tutorial_dir = '/Users/alexandre/nipype-tutorial'
data_dir = op.join(tutorial_dir, 'ds107')
required_files = [op.join(data_dir, 'sub001', 'BOLD',    'task001_run001', 'bold.nii.gz'),
                  op.join(data_dir, 'sub001', 'BOLD',    'task001_run002', 'bold.nii.gz'),
                  op.join(data_dir, 'sub044', 'BOLD',    'task001_run001', 'bold.nii.gz'),
                  op.join(data_dir, 'sub044', 'BOLD',    'task001_run002', 'bold.nii.gz'),
                  op.join(data_dir, 'sub001', 'anatomy', 'highres001.nii.gz'),
                  op.join(data_dir, 'sub044', 'anatomy', 'highres001.nii.gz'),
                 ]
print(required_files)
# In[31]:
import nipype.algorithms
# In[32]:
from nipype.interfaces.fsl import DTIFit
from nipype.interfaces.spm import Realign
# In[33]:
DTIFit.help()
# In[34]:
import os
library_dir = os.path.join(tutorial_dir, 'results')
if not os.path.exists(library_dir):
    os.mkdir(library_dir)
os.chdir(library_dir)
# In[35]:
# pick a demo file
demo_file = required_files[0]
print(demo_file)
# In[37]:
# check the current folder
print(op.abspath('.'))
# In[38]:
from nipype.algorithms.misc import Gunzip
convert = Gunzip()
convert.inputs.in_file = demo_file
results = convert.run()
# In[39]:
results.outputs
# In[40]:
from nipype.algorithms.misc import Gunzip
convert = Gunzip()
convert.inputs.in_file = demo_file
results = convert.run()
uzip_bold = results.outputs.out_file
print(uzip_bold)
# In[41]:
convert = Gunzip()
results = convert.run(in_file=demo_file)
print(results.outputs)
# In[13]:
convert.inputs
# In[14]:
results.inputs
# In[43]:
from nipype.interfaces.spm import Realign
realign = Realign(in_files=uzip_bold, register_to_mean=False)
results1 = realign.run()
#print(os.listdir())
# In[44]:
from nipype.interfaces.fsl import MCFLIRT
mcflirt = MCFLIRT(in_file=uzip_bold, ref_vol=0, save_plots=True)
results2 = mcflirt.run()
# In[36]:
print('SPM realign execution time:', results1.runtime.duration)
print('Flirt execution time:', results2.runtime.duration)
# In[48]:
get_ipython().system('ls')
get_ipython().system('fslinfo bold.nii')
get_ipython().system('cat bold_mcf.nii.gz.par')
get_ipython().system('wc -l bold_mcf.nii.gz.par')
get_ipython().system('cat rp_bold.txt')
get_ipython().system('wc -l rp_bold.txt')
# In[45]:
import numpy as np
import matplotlib.pyplot as plt
fig, ax = plt.subplots(2)
ax[0].plot(np.genfromtxt('bold_mcf.nii.gz.par')[:, 3:])
ax[0].set_title('FSL')
ax[1].plot(np.genfromtxt('rp_bold.txt')[:, :3])
ax[1].set_title('SPM')
# In[18]:
from nipype.caching import Memory
mem = Memory('.')
# In[48]:
spm_realign = mem.cache(Realign)
fsl_realign = mem.cache(MCFLIRT)
# In[51]:
spm_results = spm_realign(in_files='ds107.nii', register_to_mean=False)
fsl_results = fsl_realign(in_file='ds107.nii', ref_vol=0, save_plots=True)
# In[50]:
fig, ax = plt.subplots(2)
ax[0].plot(np.genfromtxt(fsl_results.outputs.par_file)[:, 3:])
ax[1].plot(np.genfromtxt(spm_results.outputs.realignment_parameters)[:,:3])
# In[19]:
files = required_files[0:2]
print(files)
# In[26]:
converter = mem.cache(Gunzip)
newfiles = []
for idx, fname in enumerate(files):
    results = converter(in_file=fname)
    newfiles.append(results.outputs.out_file)
print(newfiles)
# In[50]:
from nipype.pipeline.engine import Node, MapNode, Workflow
# In[51]:
realign_spm = Node(Realign(), name='motion_correct')
# In[53]:
convert2nii = MapNode(Gunzip(), iterfield=['in_file'],
                      name='convert2nii')
# In[59]:
realignflow = Workflow(name='realign_with_spm')
#realignflow.connect(convert2nii, 'out_file', realign_spm, 'in_files')
realignflow.connect([(convert2nii, realign_spm, [('out_file', 'in_files')]) ])
# In[60]:
convert2nii.inputs.in_file = required_files
realign_spm.inputs.register_to_mean = False
realignflow.base_dir = '.'
realignflow.run()
# In[64]:
realignflow.write_graph()
# In[69]:
from IPython.core.display import Image
Image('realign_with_spm/graph.dot.png')
# In[68]:
realignflow.write_graph(graph2use='orig')
Image('realign_with_spm/graph_detailed.dot.png')
# In[81]:
# In[65]:
from nipype.interfaces.io import DataGrabber, DataFinder
ds = Node(DataGrabber(infields=['subject_id'], 
                      outfields=['func']),
          name='datasource')
ds.inputs.base_directory = op.join(tutorial_dir, 'ds107')
ds.inputs.template = '%s/BOLD/task001*/bold.nii.gz'
ds.inputs.sort_filelist = True
ds.inputs.subject_id = 'sub001'
print(ds.run().outputs)
# In[85]:
ds.inputs.subject_id = ['sub001', 'sub044']
print(ds.run().outputs)
# In[63]:
ds = Node(DataGrabber(infields=['subject_id', 'task_id'],
                      outfields=['func', 'anat']),
          name='datasource')
ds.inputs.base_directory = os.path.abspath('ds107')
ds.inputs.template = '*'
ds.inputs.template_args = {'func': [['subject_id', 'task_id']],
                           'anat': [['subject_id']]}
ds.inputs.field_template = {'func': '%s/BOLD/task%03d*/bold.nii.gz',
                            'anat': '%s/anatomy/highres001.nii.gz'}
ds.inputs.sort_filelist = True
ds.inputs.subject_id = ['sub001', 'sub044']
ds.inputs.task_id = 1
ds_out = ds.run()
print(ds_out.outputs)
# In[66]:
convert2nii = MapNode(Gunzip(), iterfield=['in_file'],
                      name='convert2nii')
realign_spm = Node(Realign(), name='motion_correct')
realign_spm.inputs.register_to_mean = False
connectedworkflow = Workflow(name='connectedtogether')
connectedworkflow.base_dir = os.path.abspath('working_dir')
connectedworkflow.connect([(ds,          convert2nii, [('func',     'in_file')]),
                           (convert2nii, realign_spm, [('out_file', 'in_files')]),
                          ])
# In[67]:
from nipype.interfaces import DataSink
sinker = Node(DataSink(), name='sinker')
sinker.inputs.base_directory = os.path.abspath('output')
connectedworkflow.connect([(realign_spm, sinker, [('realigned_files',        'realigned'),
                                                  ('realignment_parameters', 'realigned.@parameters'),
                                                 ]),
                          ])
# In[92]:
get_ipython().run_line_magic('pinfo', 'connectedworkflow.run')
# In[70]:
connectedworkflow.write_graph()
Image('working_dir/connectedtogether/graph.dot.png')