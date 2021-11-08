#!/usr/bin/env python
# coding: utf-8
# In[13]:
import pandas as pd
import numpy as np
from numpy import linalg
from bokeh.models import LinearInterpolator, CategoricalColorMapper, HoverTool, ColumnDataSource, Title
from bokeh.palettes import Spectral6
from bokeh.io import output_notebook, show, push_notebook, output_file
from bokeh.plotting import figure, gridplot
from ipywidgets import interact
from bokeh.palettes import RdYlGn
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
output_notebook()
#output_file('example')
# In[48]:
#Define function here:
def matrixhit(a,b,c,d,x0,y0,steps):
    xvals = [0]
    yvals = [0]
    ind = [0]
    mat0 = np.array([(a,b),(c,d)])
    newmat = mat0
    if steps == 0:
        return [x0],[y0], ind
    elif steps == 1:
        xvals[0], yvals[0] = x0, y0
        xvals += [np.matmul(mat0, np.array([x0,y0]))[0]]
        yvals += [np.matmul(mat0, np.array([x0,y0]))[1]] 
        ind = [1]*2
        return xvals,yvals,ind
    else:
        xvals[0], yvals[0] = x0, y0
        xvals += [np.matmul(mat0, np.array([x0,y0]))[0]]
        yvals += [np.matmul(mat0, np.array([x0,y0]))[1]]
        newmat = np.matmul(mat0,mat0) 
        for i in range(steps-1):
            xvals += [np.matmul(newmat,np.array([x0,y0]))[0]]
            yvals += [np.matmul(newmat,np.array([x0,y0]))[1]]
            newmat = np.matmul(mat0,newmat)
        ind = [steps]*(steps+1)
        return xvals, yvals, ind
#Create dataframe
col1,col2, ind = list(),list(), list()
for i in range(steps):
    col1 += matrixhit(a,b,c,d,x0,y0,i)[0]
    col2 += matrixhit(a,b,c,d,x0,y0,i)[1]
    ind += matrixhit(a,b,c,d,x0,y0,i)[2]
data = pd.DataFrame({'xvals': col1, 'yvals': col2, 'ind': ind}).set_index('ind')
data['zvals'] = data['yvals'] / data['xvals']
#This changes the window to fit all data
#PLOT_OPTS = dict(height=400,
#                 x_axis_type='linear',
#                 x_range=(np.min(col1)-100,np.max(col1)+100),
#                 y_range=(np.min(col2)-100,np.max(col2)+100)
#)
PLOT_OPTS = dict(height=450,
                 width=600,
                 x_axis_type='linear',
                 x_range=(-100,100),
                 y_range=(-100,100)
)
source = ColumnDataSource(dict(
    x=data.loc[1].xvals,
    y=data.loc[1].yvals,
    z=data.loc[1].zvals,
))
hover = HoverTool(show_arrow=False,tooltips=[
    ("index", "$index"),
    ("(x,y)", "(@x, @y)"),
])
p1=figure(
    #title='Eigenvalues and Eigenvectors',
    title_location='above',
    toolbar_location='left',
    tools=[hover, 'pan','wheel_zoom', 'save'],
    active_scroll="wheel_zoom",
    #active_inspect = None,
    **PLOT_OPTS)
p1.circle(
    x='x',y='y',
    size=8,
    color='black',
    alpha=1,
    source=source,
)
#Function to format the complex eigenvalues
def complexformat(z, n):
    a_real = str(round(z.real, n))
    b_imag = str(round(z.imag, n))
    return a_real+' + '+b_imag+' i'
#Add text to display eigenpairs on the plot and Calculate Eigenvalues and Eigenvectors
eigs = linalg.eig(np.array([(a,b),(c,d)]))
eigval1,eigval2 = complexformat(eigs[0][0],3),complexformat(eigs[0][1],3)
eigvec1a,eigvec1b = complexformat(eigs[1][0][0],3),complexformat(eigs[1][1][0],3)
eigvec2a,eigvec2b = complexformat(eigs[1][0][1],3),complexformat(eigs[1][1][1],3)
eigenstring1 = 'Eigen-pair1: ('+eigval1+')   ['+eigvec1a+'   '+eigvec1b+']'
eigenstring2 = 'Eigen-pair2: ('+eigval2+')   ['+eigvec2a+'   '+eigvec2b+']'
p1.add_layout(Title(text=eigenstring1, align="center"), "below")
p1.add_layout(Title(text=eigenstring2, align='center'), 'below')
#Add Table
columns = [
        TableColumn(field="x", title="x"),
        TableColumn(field="y", title="y"),
        TableColumn(field="z", title='y/x')
    ]
p2 = DataTable(source=source, columns=columns, width=200, height=450)
p = gridplot([[p1,p2]], toolbar_location='left')
show(p, notebook_handle=True)
def update(ind=0):
    new_data = dict(
        x=data.loc[[ind]].xvals,
        y=data.loc[[ind]].yvals,
        z=data.loc[[ind]].zvals
    )
    source.data = new_data
#    p1.title.text='Eigenvalues and Eigenvectors'
    push_notebook()
interact(update, ind=(0,steps-1,1))
# In[39]:
a,b,c,d,x0,y0 = 1,1,2,0,0,1
steps = 51
# In[29]:
a,b,c,d,x0,y0 = 3,2,1,0,-1,-2
steps = 51
# In[31]:
a,b,c,d,x0,y0 = 1,1,-1,1,3,2
steps = 51