import os
import sys
import ast
import astor
import nbformat
from scalpel.core.module_graph import MNode, ModuleGraph
from scalpel.SSA.ssa import SSA

# we need to define cretieras for variables
def do_single_notebook(filename):
    try:
        with open(filename) as f:
            nb = nbformat.read(f, as_version=4)
            cells = list(filter(lambda x:x['cell_type'] == 'code' , nb.cells))
            nb.cells = cells # assign new cells
            source_cells = [c['source'] for c in nb.cells]
            source_all = "\n".join(source_cells)
            # get func_call and parameter type
            # how to deal with variable func def
            source_all_lines = source_all.split('\n')
            # remove magic functions and linux commands
            source_all_lines = filter(lambda x:len(x)>0 and x[0]!='%' and x[0]!='!', source_all_lines)
            source_all = "\n".join(source_all_lines)
            print(source_all)
            #print(source_all)
            #test_SSA(source_all)

    except Exception as e:
        print(e)
        return None

def test_SSA(source):

    #filename = sys.argv[1]
    #source = open(filename).read()
    mnode = MNode("local")
    mnode.source = source
    mnode.gen_ast()
    ast_node = mnode.ast
    m_ssa = SSA(source)
    m_ssa.gen()
    m_ssa.test()

def main():
    all_rows = open("all.row").readlines()
    for row in all_rows:
        filename = row.strip().split('|')[-1]
        #print(filename)
        filename = "/mnt/fit-Knowledgezoo/Github_repos_download/data/diyclassics@mapping-experiments/book-map-ner-htef.ipynb"
        do_single_notebook(filename)
        break
        #break
    return 0
if __name__ == '__main__':
    main()
