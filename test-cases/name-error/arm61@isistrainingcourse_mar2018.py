import numpy as np 
import nglview as nv
from falass import readwrite, job, sld, reflect, compare
files = readwrite.Files(datfile='example/example.dat')
files.read_dat()
expdata = files.plot_dat(rq4=False)
expdata.show()
mono_init = pt.load('example/monolayer.pdb')
view = nv.show_pytraj(mono_init)
view
files.pdbfile = 'example/example.pdb'
files.flip = True
files.read_pdb()
files.lgtfile = 'example/example.lgt'
files.read_lgt()
layer_thickness = 1.
cut_off = 5.
job = job.Job(files, layer_thickness, cut_off)
job.set_lgts()
sld = sld.SLD(job)
sld.get_sld_profile()
sld.average_sld_profile()
sld.plot_sld_profile()
reflect = reflect.Reflect(sld.sld_profile, files.expdata)
reflect.calc_ref()
reflect.average_ref() 
reflect.plot_ref(rq4=False)
compare = compare.Compare(files.expdata, reflect.averagereflect, 1e-1, 1e-6)
compare.fit()
compare.return_fitted()
compare.plot_compare()
