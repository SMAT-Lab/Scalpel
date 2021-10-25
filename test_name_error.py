import os
import re
import sys
import ast
import astor
import nbformat
from nbconvert import PythonExporter
from scalpel.core.mnode import MNode
from scalpel.SSA.ssa import SSA
from scalpel.util import  get_path_by_ext

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

def code_syntax_check(src_path):
    src = open(src_path).read()
    fn = os.path.basename(src_path)
    try:
        tree = ast.parse(src)
    except Exception as e:
        #print(e)
        os.system('2to3 '+ src_path + ' -n -W  --output-dir=tmp/')
        src = open('./tmp/'+fn).read()
    return src

def test_SSA(source):

    mnode = MNode("local")
    mnode.source = source
    mnode.gen_ast()
    ast_node = mnode.ast
    if ast_node is None: 
        #print('syntax')
        return []
    cfg = mnode.gen_cfg()
    graph_viz = cfg.build_visual('pdf')
    graph_viz.render("cfg1", view=False)
    m_ssa = SSA(source)
    #m_ssa.compute_SSA(cfg)
    #undefined_names = m_ssa.compute_SSA_new(cfg, def_names=def_names)
    undefined_names = m_ssa.compute_undefined_names(cfg)
    #print(undefined_names)
    return undefined_names
    #m_final_idents = m_ssa.compute_final_idents()
    #live_ident_table = [m_final_idents]

    #undefined_idents = m_ssa.test(def_names = def_names)

    #def_names = []

    #key_path = m_ssa.error_paths[undefined_idents[0]][0]
    #key_path = list(reversed(key_path))
    #m_ssa.retrieve_key_stmts(key_path)
    #return undefined_idents

    for fun_name, fun_cfg in cfg.functioncfgs.items():
        #graph_viz = fun_cfg.build_visual('pdf')
        #graph_viz.render("cfg1", view=False)
        args = cfg.function_args[fun_name]
        arg_idents = {arg_name:[2] for arg_name in args}
    #    print(fun_name, arg_idents)
        live_ident_table.append(arg_idents)
        fun_ssa = SSA(source)
        #fun_ssa.compute_SSA(fun_cfg)
        local_undefined_names = m_ssa.compute_SSA_new(cfg)
        #undefined_idents += fun_ssa.test(live_ident_table=live_ident_table, def_names = def_names)
        live_ident_table.pop()
        #def_names += [fun_name]

    #return undefined_idents
    cfg.class_cfgs = {}
    for class_name, class_cfg in cfg.class_cfgs.items():
        # class body ssa compute
        c_ssa = SSA(source)
        c_ssa.compute_SSA(class_cfg)
        c_final_idents = c_ssa.compute_final_idents()
        live_ident_table.append(c_final_idents)
        for inside_fun_name, inside_fun_cfg in class_cfg.functioncfgs.items(): 
            if len(inside_cfg.functioncfgs.items()) >1:
                exit(0)
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

    #print('--------------------------')
    #print(target_ident)
    #print(undefined_idents)
    #print('--------------------------')
    return undefined_idents
    #if target_ident is None:
    #    return len(undefined_idents)==0
    #
    #if target_ident in undefined_idents:
    #    return True
    #return False

def test_SSA_single():
    #fn = "TilakD@Time-Series-Prediction-and-Text-Generation---RNN.py" # case
    #passed
    #fn = "howl-anderson@q_learning_demo.py"  # lib issues
    #fn = "TermiNutZ@pills_online.py"
    #fn = "tamanyan@ml-baseball.py"  # wrong !!
    #fn = "pysal@geopyter.py" # syntax
    #fn = "KirstieJane@BrainsForPublication.py" # syntax
    #fn = "chrisjcc@DataInsight.py" # R script syntax
    #fn = "independent_example.py"
    # new cases

    #fn = "chingwenhsu@cme161.py"
    fn_path = sys.argv[1]
    fn = os.path.basename(fn_path)
    src_path = fn_path

    #src_path = os.path.join('test-cases', 'name-error', fn)
    #src_path = os.path.join('exec_scripts', fn)
    #src_path = os.path.join('nameerror-tests', fn)
    #exec_log_path = os.path.join("sniffer-dog-exp-data/base/exec_log/", fn.split('.py')[0])
    #msg = open(exec_log_path).read()
    #name = get_name_from_msg(msg)
    #name = "Activation"
    src = open(src_path).read()
    try:
        tree = ast.parse(src)
    except Exception as e:
        os.system('2to3 '+ src_path + ' -n -W  --output-dir=tmp/ > /dev/null')
        src = open('./tmp/'+fn).read()
    res = test_SSA(src)
    #print('--------------------')
    print(res)

def test_SSA_batch():
    #filename = sys.argv[1]
    #source = open(filename).read()
    #all_fns = os.listdir(os.path.join('test-cases', 'name-error'))
    folder = sys.argv[1]
    all_fns = get_path_by_ext(folder)

    for fn in all_fns:
     #   src_path = os.path.join('test-cases', 'name-error', fn) 
        #src_path = os.path.join('exec_scripts', fn) 
        #exec_log_path = os.path.join("sniffer-dog-exp-data/base/exec_log/", fn.split('.py')[0])
        #msg = open(exec_log_path).read()
        #name = get_name_from_msg(msg)
        #src_path ='tmp.py'
        #print(src_path)
        src_path = fn
        src = code_syntax_check(src_path)
        #src = open(src_path).read()
        if src.find("import *")>=0:
            continue
        if src.find("get_ipython()")>=0:
            continue
        #name = None
        try:
            undefined_idents = test_SSA(src)
            #if name not in undefined_idents:
     #           print(fn, name, "not-found")
            #continue
            if len(undefined_idents) > 0:
     #           print('---------------------')
                print(fn, set(undefined_idents))
        except:
            pass

def main():
    #all_rows = open("all.row").readlines()
    #all_rows = open("nameerror.row").readlines()
    all_rows = open("req3.subject.row").readlines()
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
        #notebook_path = os.path.join("test-cases/name-error-notebooks", repo_name+'-'+ filename)
        notebook_path = os.path.join("exec_notebooks/", repo_name+'-'+ filename)
        s = do_single_notebook(notebook_path)
        #f = open('nameerror-tests/'+repo_name+ '.py', 'w')
        f = open('exec_scripts/'+repo_name+ '.py', 'w')
        f.write(s)
        f.close() 
        #break
        #break
    return 0
if __name__ == '__main__':
    #main()
    test_SSA_batch()
    #test_SSA_single()
