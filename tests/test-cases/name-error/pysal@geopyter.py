#!/usr/bin/env python
# coding: utf-8
# In[1]:
import nbformat
import io
# In[27]:
import re
import os 
import requests
from urllib.parse import urlparse
def read_nb(nb_src, ext=True):
    """
    Read a notebook file and return a notebook object.
    Parameters
    ==========
    nb: String
        Path to the notebook file; if the path does not end
        in '.ipynb' then this will be appended unless you
        override this by setting the 'ext' to False.
    ext: boolean
        Defaults to True, meaning that the '.ipynb'
        extension will be automatically added. If you do not
        want this behaviour for some reason then set ext to False.
    Returns
    =======
    An object of class nbformat.notebooknode.NotebookNode
    """
    m = re.search('^(.+geopyter)', os.getcwd(), re.IGNORECASE)
    if m:
        base_dir = m.group(0)
    else:
        base_dir = '.'
    
    # Append file extension if missing and ext is True
    if not nb_src.endswith('.ipynb') and ext is True:
        nb_src += '.ipynb'
    
    path = ''
    loc = urlparse(nb_src)
    if loc.scheme in ('http','ftp','https'):
        # This doesn't support credentialed access at this time
        # -- partly because it's a pain, and partly because you
        # should be sharing... :-)
        
        nbd = requests.get(nb_src).text
        
        # Read-only in UTF-8, note NO_CONVERT.
        with io.StringIO(r) as f:
            nb = nbformat.read(f, nbformat.NO_CONVERT)
            
    elif loc.path is not None:
        if os.path.exists(nb_src):
            path = nb_src
        elif os.path.exists(os.path.join(base_dir,"atoms",nb_src)):
            path = os.path.join(base_dir,"atoms",nb_src)
        else:
            print("Doesn't look like there's a file at: " + nb_src)
        
        # Read-only in UTF-8, note NO_CONVERT.
        with open(nb, 'r', encoding='utf8') as f:
            nb = nbformat.read(f, nbformat.NO_CONVERT)
        
    else:
        print("Don't know what to do with this type of path: " + nb_src)
    
    nb.base_dir = nb_src
    
    return nb
nburl = 'https://raw.githubusercontent.com/kingsgeocomp/geocomputation/master/Practical-01-Code%20Camp%20Recap.ipynb'
t = read_nb(nburl)
print(t)
# In[16]:
r = requests.get(nburl).text
#r.text.split("\n")
f = io.StringIO(r)
print(f.readline())
print(f.readline())
print(f.readline())
# In[11]:
get_ipython().run_line_magic('pinfo', 'nbformat.read')
# In[265]:
from git import Repo
def gitter(path='.'):
    """
    Try to collect GitHub information to use in tracking 
    authorship contributions and allow specification of
    particular versions of notebooks.
    
    Parameters
    ==========
    path: String
        The path to a GitHub repository. Defaults to '.'
    
    Returns
    =======
    rp: dict
        A dictionary containing relevant git metadata
    """
    repo = Repo(path)
    
    rp = {}
    
    rp['active_branch'] = str(repo.active_branch)
    
    hc = repo.head.commit
    rp['author.name'] = hc.author.name
    rp['authored_date'] = datetime.datetime.fromtimestamp(hc.authored_date).strftime('%Y-%m-%d %H:%M:%S')
    rp['committer.name'] = hc.committer.name
    rp['committed_date'] = datetime.datetime.fromtimestamp(hc.committed_date).strftime('%Y-%m-%d %H:%M:%S')
    rp['sha'] = hc.hexsha
    
    return rp
# In[266]:
print(gitter())
# In[267]:
import re
import importlib
def find_libraries(nb):
    """
    Utility function to find libraries imported by notebooks 
    and assemble them into a group for reporting and testing
    purposes.
    
    Parameters
    ==========
    nb: nbformat.notebooknode.NotebookNode
        A notebook object to search for import statements
        
    Returns
    =======
    libs: Set
        A set containing the libraries imported by the notebook
    """
    
    # Find and classify the cells by type [code, markdown]
    cell_types = get_nb_structure(nb)
    
    libs  = set()
    vlibs = {}
    
    # Iterate over the code cell-types
    for c in cell_types['code']:
        try:
            #print("-" * 25)
            #print(nb.cells[c]['source'])
            
            # Convert the code into a block of lines
            block = nb.cells[c]['source'].splitlines()
            # Loop over the lines looking for import-type statements
            for l in block: 
                m = re.match("(?:from|import) (\S+)", l)
                if m:
                    libs.add(m.group(1))
        except IndexError: #Catch index error (not sure where this comes from)
            pass
    
    # Try to get the versions in use on the machine
    for l in libs: 
        l = l.split('.')[0]
        #print("Checking version of " + l)
        mod = importlib.import_module(l)
        ver = None
        try:
            ver = mod.__version__
        except AttributeError:
            try: 
                ver = mod.version
            except AttributeError:
                print("Unable to determine version for: " + l)
                print("Currently we check <module>.__version__ and <moduled>.version")
                pass
        vlibs[l] = ver
    return vlibs
# In[268]:
#source_nb = 'atoms/foundations/Dictionaries.ipynb'
source_nb = 'atoms/visualization/choropleth_classification.ipynb'
inb = read_nb(source_nb)
print(find_libraries(inb))
# In[315]:
def read_user_metadata(nb):
    src = nb.cells[0]['source']
    #print(src)
    
    meta = {}
    
    if not re.match("\# \w+", src):
        print("The first cell should be of level h1 and contain a bulleted list of metadata.")
    
    for l in src.splitlines():
        m = re.match("- ([^\:]+?)\: (.+)", l)
        if m is not None:
            val = m.group(2).split(';')
            if len(val)==1:
                val = val[0]
            meta[m.group(1)] = val
    return meta
# In[313]:
#source_nb = 'atoms/foundations/Dictionaries.ipynb'
source_nb = 'atoms/visualization/choropleth_classification.ipynb'
inb = read_nb(source_nb)
# In[317]:
for (key, val) in read_user_metadata(inb).iteritems():
    write_metadata(inb, key, val)
# In[319]:
write_metadata(inb, unicode('libraries'), find_libraries(inb))
write_metadata(inb, unicode('git'), gitter())
# In[5]:
inb.keys()
# In[320]:
inb.metadata
# In[67]:
write_nb(inb, 'test-metadata.ipynb')
# In[166]:
dump_nb(inb, cells=2)
# In[18]:
c0 = snb.cells[0]
# In[19]:
type(c0)
# In[20]:
c0.keys()
# In[21]:
c0['cell_type']
# In[22]:
c0['source']
# In[23]:
c0['metadata']
# In[24]:
from collections import defaultdict
def get_structure(cells):
    cell_types = defaultdict(list)
    for i, cell in enumerate(cells):
        cell_types[cell.cell_type].append(i)
    return cell_types
            
# In[25]:
cell_types = get_structure(snb.cells)
# In[26]:
cell_types.keys()
# In[27]:
for ct, cells in cell_types.items():
    print('Cell Type: %s\t %d cells'% (ct, len(cells)))
# In[28]:
code_cell_idx = cell_types['code'][0]
code_cell_idx
# In[29]:
snb.cells[code_cell_idx]
# In[30]:
mkd_cell_idx = cell_types['markdown'][0]
mkd_cell_idx
# In[31]:
snb.cells[mkd_cell_idx]
# In[32]:
def remove_outputs(nb):
    """Set output attribute of all code cells to be empty"""
    for cell in nb.cells:
        if cell.cell_type == 'code':
            cell.outputs = []
def clear_notebook(old_ipynb, new_ipynb):
    with io.open(old_ipynb, 'r') as f:
        nb = nbformat.read(f, nbformat.NO_CONVERT)
    remove_outputs(nb)
    
    with io.open(new_ipynb, 'w', encoding='utf8') as f:
        nbformat.write(nb, f, nbformat.NO_CONVERT)
source_nb = 'atoms/visualization/choropleth_classification.ipynb'
new_nb = 'nout.ipynb'
clear_notebook(source_nb, new_nb)
# In[174]:
source_nb = 'atoms/foundations/Dictionaries-Test.ipynb'
nb = read_nb(source_nb)
# In[225]:
source_nb = 'atoms/foundations/Dictionaries-Test.ipynb'
nb = read_nb(source_nb)
import re
import markdown
from bs4 import BeautifulSoup
md = markdown.Markdown()
cell_types = get_nb_structure(nb)    
# Iterate over the code cell-types
for c in cell_types['markdown']:
    
    # Delete code blocks -- this is a bit brutal 
    # and it might be better to escape them in some
    # way... but this at least works well enough
    src = re.sub(r'```.+?```', '', nb.cells[c]['source'], flags=re.S)
    
    print("-"*20 + "New Cell" + "-"*20)
    soup = BeautifulSoup(md.convert(src), 'html.parser')
    
    h1 = soup.findAll('h1')
    print( ", ".join([x.contents[0] for x in h1]))
    
    h2 = soup.findAll('h2')
    print( ", ".join([x.contents[0] for x in h2]))
    
    h3 = soup.findAll('h3')
    print( ", ".join([x.contents[0] for x in h3]))
# In[34]:
import re
rh1 = re.compile('^# ')
rh2 = re.compile('^## ')
rh3 = re.compile('^### ')
rh4 = re.compile('^#### ')
rh = re.compile('^#+')
class NoteBook(object):
    def __init__(self, ipynb):
        self.nb = read_nb(ipynb)
        self.structure = get_structure(self.nb.cells)
        
    def get_cells_by_type(self, cell_type=None):
        if cell_type:
            cell_type = cell_type.lower()
            return [self.nb.cells[i] for i in self.structure[cell_type]]
        else:
            return self.nb.cells
    
    def get_cells_by_id(self, ids=[]):
        return [self.nb.cells[i] for i in ids]
    
    def get_header_cells(self):
        hs = []
        if 'markdown' in self.structure:
            idxs = self.structure['markdown']
            pairs = zip(idxs, self.get_cells_by_type('markdown'))
            hs = [(idx, cell) for idx, cell in pairs if rh.match(cell['source'])]
        return hs
        
        
    
# In[35]:
nb = NoteBook(source_nb)
# In[36]:
cid = nb.get_cells_by_id()
# In[37]:
cid
# In[38]:
cid = nb.get_cells_by_id([7, 10, 2])
# In[39]:
cid
# In[40]:
nb.get_header_cells()
# In[41]:
hdict = defaultdict(list)
for idx, cell in nb.get_header_cells():
    level = cell['source'].count("#")
    hdict[level].append(idx)
    
# In[42]:
hdict
# In[43]:
# find the start and end cells for each H? block
keys = list(hdict.keys())
keys.sort(reverse=True)
all_keys = keys.copy()
start_end = []
last_stop = len(nb.nb.cells)
while keys:
    current = keys.pop(0)
    for element in hdict[current]:
        above = [k for k in all_keys.copy() if k <= current]
        stop = last_stop
        while above:
            key_above = above.pop()
            larger = [v for v in hdict[key_above] if v > element]
            if larger:
                if larger[0] < stop:
                    stop = larger[0]
        start_end.append([element, stop])
        
# In[59]:
start_end # for each H? cell report the start and end cells
# In[51]:
hdict
# In[60]:
len(start_end)
# In[61]:
len(nb.get_header_cells())
# In[68]:
# second h2 section with all children
se2 = [ v for v in start_end if v[0]==3][0]
block = nb.get_cells_by_id(range(*se2))
for cell in block:
    print(cell['source'])
# In[69]:
# first h3 section in second h2 section with all children
se3 = [ v for v in start_end if v[0]==9][0]
block = nb.get_cells_by_id(range(*se3))
for cell in block:
    print(cell['source'])