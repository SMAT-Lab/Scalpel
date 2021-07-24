import os
import re
import sys
import ast
import astor
import nbformat
from nbconvert import PythonExporter
from scalpel.core.mnode import MNode
from scalpel.SSA.ssa import SSA


# we need to define cretieras for variables
def filter_line(line):
    if len(line)==0:
        return False

    if line[0] in ['%', '!', '?']:
        return False

    if line.split(' ')[0]  in ["cat", "ls", "mkdir", "less", "sudo", "cd"]:
        return False
    return True

def do_single_notebook(filename):

    try:
        with open(filename) as f:
            nb = nbformat.read(f, as_version=4)
            cells = list(filter(lambda x:x['cell_type'] == 'code' and
                x['execution_count'] is not None, nb.cells))
            nb.cells = cells # assign new cells
            exporter = PythonExporter()
            (body, resources) = exporter.from_notebook_node(nb)
            #print(resources)

            #source_cells = [c['source'] for c in nb.cells]
            #source_all = "\n".join(source_cells)
            # get func_call and parameter type
            # how to deal with variable func def
            #source_all_lines = source_all.split('\n')
            
            source_all_lines = body.split('\n')
            
            # remove magic functions and linux commands
            source_all_lines = filter(lambda x:filter_line(x), source_all_lines)
            source_all = "\n".join(source_all_lines)
            return source_all
            #print(source_all)
            #print(source_all)
            #test_SSA(source_all)

    except Exception as e:
        print(e)
        return None

def get_name_from_msg(msg):
    patter = r"/'((?:''|[^'])*)'/"
    idx2 = msg.find("is not defined")
    groups = re.findall(r"\'(.+?)\'", msg[idx2-30:idx2])
    if len(groups)>0:
        return groups[-1]
    return None

def test_SSA(source, target_ident):

    mnode = MNode("local")
    mnode.source = source
    mnode.gen_ast()
    ast_node = mnode.ast
    if ast_node is None: 
        print('syntax')
        return False

    cfg = mnode.gen_cfg()
    m_ssa = SSA(source)
    m_ssa.compute_SSA(cfg)
    m_final_idents = m_ssa.compute_final_idents()
    live_ident_table = [m_final_idents]
    undefined_idents = m_ssa.test()
    graph_viz = cfg.build_visual('pdf')
    #graph_viz.render("cfg.pdf", view=True)
    def_names = []

    for fun_name, fun_cfg in cfg.functioncfgs.items():
        args = cfg.function_args[fun_name]
        arg_idents = {arg_name:[2] for arg_name in args}
        live_ident_table.append(arg_idents)
        fun_ssa = SSA(source)
        fun_ssa.compute_SSA(fun_cfg)
        undefined_idents += fun_ssa.test(live_ident_table=live_ident_table, def_names = def_names)
        live_ident_table.pop()
        def_names += [fun_name]

    cfg.class_cfgs = {}
    for class_name, class_cfg in cfg.class_cfgs.items():
        # class body ssa compute
        c_ssa = SSA(source)
        c_ssa.compute_SSA(class_cfg)
        c_final_idents = c_ssa.compute_final_idents()
        live_ident_table.append(c_final_idents)
        for inside_fun_name, inside_fun_cfg in class_cfg.functioncfgs.items():
            args = class_cfg.function_args[inside_fun_name]
            arg_idents = {arg_name:[2] for arg_name in args}
            live_ident_table.append(arg_idents)
            fun_ssa = SSA(source)
            fun_ssa.compute_SSA(inside_fun_cfg)
            undefined_idents += fun_ssa.test(live_ident_table=live_ident_table, def_names = def_names)
            live_ident_table.pop()
            def_names += [inside_fun_name]
        def_names = def_names[0:-len(class_cfg.functioncfgs.items())]

        live_ident_table.pop()

    print('--------------------------')
    print(target_ident)
    print(undefined_idents)
    print('--------------------------')

    if target_ident in undefined_idents:
        return True
    return False

def test_SSA_single():
    #fn = "TilakD@Time-Series-Prediction-and-Text-Generation---RNN.py" # case
    #passed
    #fn = "howl-anderson@q_learning_demo.py"  # lib issues
    fn = "TermiNutZ@pills_online.py"
    #fn = "tamanyan@ml-baseball.py"  # wrong !!
    #fn = "pysal@geopyter.py" # syntax
    #fn = "KirstieJane@BrainsForPublication.py" # syntax
    #fn = "chrisjcc@DataInsight.py" # R script syntax
    #fn = "independent_example.py"

    #src_path = os.path.join('test-cases', 'name-error', fn)
    src_path = os.path.join('nameerror-tests', fn)
    exec_log_path = os.path.join("sniffer-dog-exp-data/base/exec_log/", fn.split('.py')[0])
    msg = open(exec_log_path).read()
    name = get_name_from_msg(msg)
    #name = "Activation"
    src = open(src_path).read()
    try:
        tree = ast.parse(src)
    except Exception as e:
        print(e)
        os.system('2to3 '+ src_path + ' -n -W  --output-dir=tmp/')
        src = open('tmp/'+fn).read()
    res = test_SSA(src, name)
    print(res)

def test_SSA_batch():
    #filename = sys.argv[1]
    #source = open(filename).read()
    all_fns = os.listdir('name-error-cases')
    for fn in all_fns:
        #if fn!='djahng@sentiment-rnn.py':
        #    continue
        src_path = os.path.join('name-error-cases', fn) 
        exec_log_path = os.path.join("sniffer-dog-exp-data/base/exec_log/", fn.split('.py')[0])
        msg = open(exec_log_path).read()
        name = get_name_from_msg(msg)
        #src_path ='tmp.py'
        src = open(src_path).read()
        res = test_SSA(src, name)
        if  res:
           # print('Yes')
            pass
        else:
            print(fn)
           # print("No")
        #break

def main():
    #all_rows = open("all.row").readlines()
    all_rows = open("nameerror.row").readlines()
    for row in all_rows:
        line_parts = row.strip().split('|')
        filename = line_parts[-1]
        repo_name = line_parts[1]
        #log_dir = os.path.join("/data/sda/jiawei/sniffer-dog-exp-data/base/exec_log/", repo_name)
        #content = open(log_dir).read()
        #print(repo_name)
        #print(content[0:300])
        #print(filename)
        #filename = "/mnt/fit-Knowledgezoo/Github_repos_download/data/diyclassics@mapping-experiments/book-map-ner-htef.ipynb"
        filename = os.path.basename(filename)
        notebook_path = os.path.join("test-cases/name-error-notebooks", repo_name+'-'+ filename)
        s = do_single_notebook(notebook_path)
        f = open('nameerror-tests/'+repo_name+ '.py', 'w')
        f.write(s)
        f.close() 
        #break
        #break
    return 0
if __name__ == '__main__':
    #main()
    #test_SSA_batch()
    test_SSA_single()
