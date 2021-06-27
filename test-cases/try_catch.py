"""
IPython/Jupyter Notebook progressbar decorator for iterators.
Includes a default (x)range iterator printing to stderr.
Usage:
  >>> from tqdm_notebook import tnrange[, tqdm_notebook]
  >>> for i in tnrange(10): #same as: for i in tqdm_notebook(xrange(10))
  ...     ...
"""
# future division is important to divide integers and get as
# a result precise floating numbers (instead of truncated int)
from __future__ import division, absolute_import
# import compatibility functions and utilities
import sys
import os, ast, json
from ._utils import _range
# to inherit from the tqdm class
from ._tqdm import tqdm as t 

# import IPython/Jupyter base widget and display utilities
#try:  # IPython 4.x
#    import ipywidgets
#    IPY = 4
#except ImportError:  # IPython 3.x / 2.x
#    IPY = 32
#    import warnings
#    with warnings.catch_warnings():
#        ipy_deprecation_msg = "The `IPython.html` package" \
#                              " has been deprecated"
#        warnings.filterwarnings('error',
#                                message=".*" + ipy_deprecation_msg + ".*")
#        try:
#            import IPython.html.widgets as ipywidgets
#        except Warning as e:
#            if ipy_deprecation_msg not in str(e):
#                raise
#            warnings.simplefilter('ignore')
#            try:
#                import IPython.html.widgets as ipywidgets  # NOQA
#            except ImportError:
#                pass
#        except ImportError:
#            pass
try:  # IPython 4.x / 3.x
   # if IPY == 32:
   #     from IPython.html.widgets import IntProgress, HBox, HTML
   #     IPY = 3
   # else:
   #     from ipywidgets import IntProgress, HBox, HTML
   a = 9
   b = 10
except ImportError:
    #try:  # IPython 2.x
    #    from IPython.html.widgets import IntProgressWidget as IntProgress
    #    from IPython.html.widgets import ContainerWidget as HBox
    #    from IPython.html.widgets import HTML
    #    IPY = 2
    #except ImportError:
    #    IPY = 0
    a = 12
try:  # IPython 4.x / 3.x
   # if IPY == 32:
   #     from IPython.html.widgets import IntProgress, HBox, HTML
   #     IPY = 3
   # else:
   #     from ipywidgets import IntProgress, HBox, HTML
   a = 9
except ImportError:
    #try:  # IPython 2.x
    #    from IPython.html.widgets import IntProgressWidget as IntProgress
    #    from IPython.html.widgets import ContainerWidget as HBox
    #    from IPython.html.widgets import HTML
    #    IPY = 2
    #except ImportError:
    #    IPY = 0
    a = 12
except IOError:
    #try:  # IPython 2.x
    #    from IPython.html.widgets import IntProgressWidget as IntProgress
    #    from IPython.html.widgets import ContainerWidget as HBox
    #    from IPython.html.widgets import HTML
    #    IPY = 2
    #except ImportError:
    #    IPY = 0
    a = 13
except HTTPError:
    #try:  # IPython 2.x
    #    from IPython.html.widgets import IntProgressWidget as IntProgress
    #    from IPython.html.widgets import ContainerWidget as HBox
    #    from IPython.html.widgets import HTML
    #    IPY = 2
    #except ImportError:
    #    IPY = 0
    a = 13


