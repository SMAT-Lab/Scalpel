import nbformat
import io
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
r = requests.get(nburl).text
#r.text.split("\n")
f = io.StringIO(r)
print(f.readline())
print(f.readline())
print(f.readline())
#?nbformat.read
def write_nb(nb, fn):
    """
    Write a notebook to the path specified.
    
    Parameters
    ==========
    nb: nbformat.notebooknode.NotebookNode
        A notebook object to write to disk.
    fn: String
        Path to which you want the notebook written. _Note:_ 
        for simplicity's sake this will automatically append 
        '.ipynb' to the filename; however we recommend that 
        you not get lazy and rely on this feature since it may
        go away in the future.
    
    Returns
    =======
    Void.
    """
    
    m = re.search('^(.+geopyter)', os.getcwd(), re.IGNORECASE)
    if m:
        self.base_dir = m.group(0)
    else:
        self.base_dir = '.'
    path = ''
    loc = urlparse(ipynb)
    if loc.scheme in ('http','ftp','https'):
        print("Haven't implemented remote files yet")
        #path = requests.get(loc)
    elif loc.path is not None:
        if os.path.exists(ipynb):
            path = ipynb
        elif os.path.exists(os.path.join(self.base_dir,"atoms",ipynb)):
            path = os.path.join(self.base_dir,"atoms",ipynb)
        else:
            print("Doesn't look like there's a file at: " + ipynb)
    else:
        print("Don't know what to do with this type of path info: " + ipynb)
    
    # Append file extension
    if not fn.endswith('.ipynb'):
        fn += '.ipynb'
    
    # Write raw notebook content
    with io.open(fn, 'w', encoding='utf8') as f:
        nbformat.write(nb, f, nbformat.NO_CONVERT)
from collections import defaultdict
def get_nb_structure(nb):
    cell_types = defaultdict(list)
    for i, cell in enumerate(nb['cells']):
        cell_types[cell.cell_type].append(i)
    return cell_types
def dump_nb(nb, cells=5, lines=5):
    """
    Dump content of a notebook to STDOUT to aid in debugging.
    
    Parameters
    ==========
    nb: nbformat.notebooknode.NotebookNode
        A notebook object from which to dump content.
    cells: int
        Select an arbitrary number of cells to output. Defaults to 5.
    lines: int
        Select an arbitrary number of lines from each cell to output. Defaults to 5.
    
    Returns
    =======
    Void.
    """
    
    # For the cell-range specified
    for c in xrange(0, cells):
        
        # Check we still have cells to read
        if c < len(nb.cells):
            
            # And dump the contents to STDOUT
            print("====== " + nb.cells[c]['cell_type'] + " ======")
            src = nb.cells[c]['source'].splitlines()
            if len(src) > lines:
                print('\n'.join(src[0:lines]))
                print("...")
            else:
                print(nb.cells[c]['source'])
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
print(gitter())
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
#source_nb = 'atoms/foundations/Dictionaries.ipynb'
source_nb = 'atoms/visualization/choropleth_classification.ipynb'
inb = read_nb(source_nb)
print(find_libraries(inb))
def write_metadata(nb, nm, val, namespace=unicode('geopyter')):
    """
    Add or append metadata values to the geopyter parameter.
    
    Parameters
    ==========
    nb: nbformat.notebooknode.NotebookNode
        A notebook object to which to add Geopyter metadata.
    nm: String
        The name of the key within the Geopyter dictionary that we want to update.
    val: String, List, Dictionary
        The value to associate with the key.
    
    Returns
    =======
    Void.
    """
    
    # Check for the namespace in the notebook metadata
    if not namespace in nb.metadata:
        nb.metadata[namespace] = {}
    
    # And write it
    nb.metadata[namespace][nm] = val
def get_metadata(nb, nm, namespace=unicode('geopyter')):
    """
    Retrieve metadata values from the geopyter parameter.
    
    Parameters
    ==========
    nb: nbformat.notebooknode.NotebookNode
        A notebook object to which to add Geopyter metadata.
    nm: String
        The name of the key within the Geopyter dictionary that we want to retrieve.
    
    Returns
    =======
    Void.
    """
    
    # Check for the namespace in the notebook metadata
    if not nb.metadata.has_key(namespace):
        nb.metadata[namespace] = {}
    
    # And write it
    nb.metadata[namespace][nm] = val
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
#source_nb = 'atoms/foundations/Dictionaries.ipynb'
source_nb = 'atoms/visualization/choropleth_classification.ipynb'
inb = read_nb(source_nb)
for (key, val) in read_user_metadata(inb).iteritems():
    write_metadata(inb, key, val)
write_metadata(inb, unicode('libraries'), find_libraries(inb))
write_metadata(inb, unicode('git'), gitter())
inb.keys()
inb.metadata
write_nb(inb, 'test-metadata.ipynb')
dump_nb(inb, cells=2)
c0 = snb.cells[0]
type(c0)
c0.keys()
c0['cell_type']
c0['source']
c0['metadata']
from collections import defaultdict
def get_structure(cells):
    cell_types = defaultdict(list)
    for i, cell in enumerate(cells):
        cell_types[cell.cell_type].append(i)
    return cell_types
            
cell_types = get_structure(snb.cells)
cell_types.keys()
for ct, cells in cell_types.items():
    print('Cell Type: %s\t %d cells'% (ct, len(cells)))
code_cell_idx = cell_types['code'][0]
code_cell_idx
snb.cells[code_cell_idx]
mkd_cell_idx = cell_types['markdown'][0]
mkd_cell_idx
snb.cells[mkd_cell_idx]
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
source_nb = 'atoms/foundations/Dictionaries-Test.ipynb'
nb = read_nb(source_nb)
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
        
        
    
nb = NoteBook(source_nb)
cid = nb.get_cells_by_id()
cid
cid = nb.get_cells_by_id([7, 10, 2])
cid
nb.get_header_cells()
hdict = defaultdict(list)
for idx, cell in nb.get_header_cells():
    level = cell['source'].count("#")
    hdict[level].append(idx)
    
hdict
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
        
start_end # for each H? cell report the start and end cells
hdict
len(start_end)
len(nb.get_header_cells())
# second h2 section with all children
se2 = [ v for v in start_end if v[0]==3][0]
block = nb.get_cells_by_id(range(*se2))
for cell in block:
    print(cell['source'])
# first h3 section in second h2 section with all children
se3 = [ v for v in start_end if v[0]==9][0]
block = nb.get_cells_by_id(range(*se3))
for cell in block:
    print(cell['source'])
