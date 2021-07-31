#!/usr/bin/env python
# coding: utf-8
# In[10]:
import matplotlib as mpl
from matplotlib import rc
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
get_ipython().run_line_magic('pylab', 'inline')
# size
font_size = 8
params = {'mathtext.default' : 'regular', 'font.size' : font_size}
mpl.rcParams.update(params)
# font
font = {'fontname' : 'Calibri'}
rc('text', usetex=False)
# test plot
def test_plot():
    fig = Figure()
    FigureCanvasAgg(fig)
    ax = fig.add_subplot(111)
    ax.plot([1, 2, 5])
    ax.set_title('Title')
    ax.grid(True)
    ax.set_xlabel('X-label')
    ax.set_ylabel('Y-label')
    return fig
def test_plot_matrix():
    fig = Figure()
    FigureCanvasAgg(fig)
    for i in range(1,5):
        ax = fig.add_subplot(2, 2, i)
        ax.plot([1 + i, 2 + i, 5 + i])
        ax.set_title('Title')
        ax.grid(True)
        ax.set_xlabel('X-label')
        ax.set_ylabel('Y-label')
    fig.tight_layout()
    return fig
fig = test_plot()
display(fig)
fig2 = test_plot_matrix()
display(fig2)
# In[13]:
# min and max values on colorbar labels
cb_min, cb_max = 0, 100
def add_colorbar(fig, cb_min, cb_max):
    ax = fig.add_axes([1., 0.15, 0.025, 0.7])
    norm = mpl.colors.Normalize(vmin=cb_min, vmax=cb_max)
    cb = mpl.colorbar.ColorbarBase(ax, cmap=cm.jet, norm=norm,
                                  orientation='vertical')
    cb.set_label('Some parameter')
    return fig
# single plot
fig = test_plot()
fig = add_colorbar(fig, cb_min, cb_max)
display(fig)
# multiple plots, single colorbar
fig2 = test_plot_matrix()
fig2 = add_colorbar(fig2, cb_min, cb_max)
display(fig2)