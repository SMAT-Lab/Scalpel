#!/usr/bin/env python
# coding: utf-8
# In[2]:
import numpy as np
from plotly.offline import init_notebook_mode, iplot
import plotly.graph_objs as go
init_notebook_mode(connected=True)
# In[3]:
def theta_from_eta(eta):
    return 2*np.arctan(np.e**(-eta))
    
def show_jet(phi, eta, dR):
    
    # list of all primitives to draw
    data = []
    
    # ::: beampipe
    R = 1.0
    zs = np.linspace(-R, R, 2)
    b_xs = [0 for z in zs]
    b_ys = [0 for z in zs]
    beampipe = go.Scatter3d(x=zs,
                          y=b_ys,
                          z=b_xs,
                          mode='lines',
                          showlegend=False,
                          line=dict(color='rgb(0,33,71)', width=5))
    data.append(beampipe)
    
    # ::: barrel
    phis = np.linspace(-np.pi/2., np.pi/2., 10)
    xs = R*np.sin(phis)
    X, Z = np.meshgrid(xs, zs)
    Y = np.sqrt(R**2 - X**2)
    barrel_left = go.Surface(x=Z, y=Y, z=X, surfacecolor=[1,1], showscale=False, opacity=0.4)
    barrel_right = go.Surface(x=Z, y=-Y, z=X, surfacecolor=[1,1], showscale=False, opacity=0.4)
    data += [barrel_left, barrel_right]
    
    # ::: jet direction
    theta = theta_from_eta(eta)
    ts = np.linspace(0, R, 2)
    xs = ts*np.sin(theta)*np.cos(phi)
    ys = ts*np.sin(theta)*np.sin(phi)
    zs = ts*np.cos(theta)
    jet = go.Scatter3d(x=zs,
                       y=ys,
                       z=xs,
                       mode='lines',
                       showlegend=False,
                       line=dict(color='rgb(255, 105, 97)', width=7))
    data.append(jet)
    
    # ::: jet cone: compute the circle at the end first, then draw the cone
    T = 1.0
    dphis = np.sqrt(np.linspace(0, dR**2, 20))
    detas = np.sqrt(dR**2 - dphis**2)
    # compute circle coordinates (reverse parts for plotting reasons)
    phis = np.concatenate((phi+dphis, phi+dphis[::-1], phi-dphis, phi-dphis[::-1]))
    etas = np.concatenate((eta+detas, eta-detas[::-1], eta-detas, eta+detas[::-1]))
    # transform to x, y, z
    thetas = theta_from_eta(etas)
    cxs = T*np.sin(thetas)*np.cos(phis)
    cys = T*np.sin(thetas)*np.sin(phis)
    czs = T*np.cos(thetas)
    cone_edge = go.Scatter3d(x=czs,
                            y=cys,
                            z=cxs,
                            mode='lines',
                            showlegend=False,
                            line=dict(color='rgb(255, 105, 97)', width=5))
    data.append(cone_edge)
    
    # draw lines from the circle to the origin
    for x, y, z in zip(cxs, cys, czs):
        line = go.Scatter3d(x=(0,z),
                            y=(0,y),
                            z=(0,x),
                            opacity=0.3,
                            mode='lines',
                            showlegend=False,
                            line=dict(color='rgb(255, 105, 97)'))
        data.append(line)
    
    # cosmetics
    layout = go.Layout(margin=dict(l=0,r=0,b=0,t=0),
                       scene=dict(xaxis=dict(title='Z'),
                                  yaxis=dict(title='Y'),
                                  zaxis=dict(title='X')))
    fig = go.Figure(data=data, layout=layout)
    iplot(fig, filename='simple-3d-scatter')
# In[4]:
show_jet(0, 1, 1.0)
show_jet(0, 3, 1.0)
# In[5]:
import ipywidgets as widgets
widgets.interact(show_jet, phi=widgets.FloatSlider(value=0, min=-np.pi, max=np.pi, step=0.1, description='phi'),
                           eta=widgets.FloatSlider(value=2.0, min=0, max=3, step=0.1, description='eta'),
                           dR=widgets.FloatSlider(value=0.4, min=0.1, max=1.0, step=0.1, description='dR'))