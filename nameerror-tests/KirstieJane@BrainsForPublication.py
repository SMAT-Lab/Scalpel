stats_file = '../test_data/ALL_N95_Mean_cope2_thresh_zstat1.nii.gz'
view =  'ortho'
colormap = 'RdBu_r'
threshold = '2.3'
black_bg
from IPython.display import Image, display
from glob import glob as gg
outputs = gg('../test_data/*ortho.png')
for o in outputs:
    a = Image(filename=o)
    display(a)
plotting.plot_glass_brain
