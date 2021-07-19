import nipype
# Comment the following section to increase verbosity of output
nipype.config.set('logging', 'workflow_level', 'CRITICAL')
nipype.config.set('logging', 'interface_level', 'CRITICAL')
nipype.logging.update_logging(nipype.config)
nipype.test(verbose=0) # Increase verbosity parameter for more info
nipype.get_info()
import os
import numpy as np
import matplotlib.pyplot as plt
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
import nipype.algorithms
from nipype.interfaces.fsl import DTIFit
from nipype.interfaces.spm import Realign
DTIFit.help()
Realign.help()
import os
library_dir = os.path.join(tutorial_dir, 'results')
if not os.path.exists(library_dir):
    os.mkdir(library_dir)
os.chdir(library_dir)
# pick a demo file
demo_file = required_files[0]
print(demo_file)
# check the current folder
print(op.abspath('.'))
from nipype.algorithms.misc import Gunzip
convert = Gunzip()
convert.inputs.in_file = demo_file
results = convert.run()
results.outputs
from nipype.algorithms.misc import Gunzip
convert = Gunzip()
convert.inputs.in_file = demo_file
results = convert.run()
uzip_bold = results.outputs.out_file
print(uzip_bold)
convert = Gunzip()
results = convert.run(in_file=demo_file)
print(results.outputs)
convert.inputs
results.inputs
from nipype.interfaces.spm import Realign
realign = Realign(in_files=uzip_bold, register_to_mean=False)
results1 = realign.run()
#print(os.listdir())
from nipype.interfaces.fsl import MCFLIRT
mcflirt = MCFLIRT(in_file=uzip_bold, ref_vol=0, save_plots=True)
results2 = mcflirt.run()
print('SPM realign execution time:', results1.runtime.duration)
print('Flirt execution time:', results2.runtime.duration)
import numpy as np
import matplotlib.pyplot as plt
fig, ax = plt.subplots(2)
ax[0].plot(np.genfromtxt('bold_mcf.nii.gz.par')[:, 3:])
ax[0].set_title('FSL')
ax[1].plot(np.genfromtxt('rp_bold.txt')[:, :3])
ax[1].set_title('SPM')
from nipype.caching import Memory
mem = Memory('.')
spm_realign = mem.cache(Realign)
fsl_realign = mem.cache(MCFLIRT)
spm_results = spm_realign(in_files='ds107.nii', register_to_mean=False)
fsl_results = fsl_realign(in_file='ds107.nii', ref_vol=0, save_plots=True)
fig, ax = plt.subplots(2)
ax[0].plot(np.genfromtxt(fsl_results.outputs.par_file)[:, 3:])
ax[1].plot(np.genfromtxt(spm_results.outputs.realignment_parameters)[:,:3])
files = required_files[0:2]
print(files)
converter = mem.cache(Gunzip)
newfiles = []
for idx, fname in enumerate(files):
    results = converter(in_file=fname)
    newfiles.append(results.outputs.out_file)
print(newfiles)
os.chdir(tutorial_dir)
from nipype.pipeline.engine import Node, MapNode, Workflow
realign_spm = Node(Realign(), name='motion_correct')
convert2nii = MapNode(Gunzip(), iterfield=['in_file'],
                      name='convert2nii')
realignflow = Workflow(name='realign_with_spm')
#realignflow.connect(convert2nii, 'out_file', realign_spm, 'in_files')
realignflow.connect([(convert2nii, realign_spm, [('out_file', 'in_files')]) ])
convert2nii.inputs.in_file = required_files
realign_spm.inputs.register_to_mean = False
realignflow.base_dir = '.'
realignflow.run()
realignflow.write_graph()
from IPython.core.display import Image
Image('realign_with_spm/graph.dot.png')
realignflow.write_graph(graph2use='orig')
Image('realign_with_spm/graph_detailed.dot.png')
from nipype.interfaces.io import DataGrabber, DataFinder
ds = Node(DataGrabber(infields=['subject_id'], 
                      outfields=['func']),
          name='datasource')
ds.inputs.base_directory = op.join(tutorial_dir, 'ds107')
ds.inputs.template = '%s/BOLD/task001*/bold.nii.gz'
ds.inputs.sort_filelist = True
ds.inputs.subject_id = 'sub001'
print(ds.run().outputs)
ds.inputs.subject_id = ['sub001', 'sub044']
print(ds.run().outputs)
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
convert2nii = MapNode(Gunzip(), iterfield=['in_file'],
                      name='convert2nii')
realign_spm = Node(Realign(), name='motion_correct')
realign_spm.inputs.register_to_mean = False
connectedworkflow = Workflow(name='connectedtogether')
connectedworkflow.base_dir = os.path.abspath('working_dir')
connectedworkflow.connect([(ds,          convert2nii, [('func',     'in_file')]),
                           (convert2nii, realign_spm, [('out_file', 'in_files')]),
                          ])
from nipype.interfaces import DataSink
sinker = Node(DataSink(), name='sinker')
sinker.inputs.base_directory = os.path.abspath('output')
connectedworkflow.connect([(realign_spm, sinker, [('realigned_files',        'realigned'),
                                                  ('realignment_parameters', 'realigned.@parameters'),
                                                 ]),
                          ])
connectedworkflow.run
ds.iterables = ('subject_id', ['sub001', 'sub044'])
connectedworkflow.run()
connectedworkflow.write_graph()
Image('working_dir/connectedtogether/graph.dot.png')
from nipype.interfaces.utility import Function
def myfunc(input1, input2):
    """Add and subtract two inputs."""
    return input1 + input2, input1 - input2
calcfunc = Node(Function(input_names=['input1', 'input2'],
                         output_names = ['sum', 'difference'],
                         function=myfunc),
                name='mycalc')
calcfunc.inputs.input1 = 1
calcfunc.inputs.input2 = 2
res = calcfunc.run()
print (res.outputs)
connectedworkflow.run()
connectedworkflow.run('MultiProc', plugin_args={'n_procs': 4})
from os.path import abspath as opap
from nipype.interfaces.io import XNATSource
from nipype.pipeline.engine import Node, Workflow
from nipype.interfaces.fsl import BET
subject_id = 'xnat_S00001'
dg = Node(XNATSource(infields=['subject_id'],
                     outfields=['struct'],
                     config='/Users/satra/xnat_configs/nitrc_ir_config'),
          name='xnatsource')
dg.inputs.query_template = ('/projects/fcon_1000/subjects/%s/experiments/xnat_E00001'
                            '/scans/%s/resources/NIfTI/files')
dg.inputs.query_template_args['struct'] = [['subject_id', 'anat_mprage_anonymized']]
dg.inputs.subject_id = subject_id
bet = Node(BET(), name='skull_stripper')
wf = Workflow(name='testxnat')
wf.base_dir = opap('xnattest')
wf.connect(dg, 'struct', bet, 'in_file')
from nipype.interfaces.io import XNATSink
ds = Node(XNATSink(config='/Users/satra/xnat_configs/central_config'),
          name='xnatsink')
ds.inputs.project_id = 'NPTEST'
ds.inputs.subject_id = 'NPTEST_xnat_S00001'
ds.inputs.experiment_id = 'test_xnat'
ds.inputs.reconstruction_id = 'bet'
ds.inputs.share = True
wf.connect(bet, 'out_file', ds, 'brain')
wf.run()
from nipype import config, logging
config.enable_debug_mode()
logging.update_logging(config)
config.set('execution', 'stop_on_first_crash', 'true')
wf.config['execution']['hash_method'] = 'content'
bet.config = {'execution': {'keep_unnecessary_outputs': 'true'}}
wf.run()
config.set_default_config()
logging.update_logging(config)
from nipype.workflows.fmri.fsl.preprocess import create_susan_smooth
smooth = create_susan_smooth()
smooth.inputs.inputnode.in_files = opap('output/realigned/_subject_id_sub044/rbold_out.nii')
smooth.inputs.inputnode.fwhm = 5
smooth.inputs.inputnode.mask_file = 'mask.nii'
smooth.run() # Will error because mask.nii does not exist
from nipype.interfaces.fsl import BET, MeanImage, ImageMaths
from nipype.pipeline.engine import Node
remove_nan = Node(ImageMaths(op_string= '-nan'), name='nanremove')
remove_nan.inputs.in_file = op.abspath('output/realigned/_subject_id_sub044/rbold_out.nii')
mi = Node(MeanImage(), name='mean')
mask = Node(BET(mask=True), name='mask')
wf = Workflow('reuse')
wf.base_dir = op.abspath(op.curdir)
wf.connect([(remove_nan, mi,     ['out_file', 'in_file']),
            (mi,         mask,   ['out_file', 'in_file']),
            (mask,       smooth, ['out_file', 'inputnode.mask_file']),
            (remove_nan, smooth, ['out_file', 'inputnode.in_files']),
           ])
wf.run()
print(smooth.list_node_names())
median = smooth.get_node('median')
median.inputs.op_string = '-k %s -p 60'
wf.run()
