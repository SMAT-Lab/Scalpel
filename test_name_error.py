import os
import re
import sys
import ast
import astor
import nbformat
from scalpel.core.mnode import MNode
from scalpel.SSA.ssa import SSA

# we need to define cretieras for variables
def do_single_notebook(filename):
    try:
        with open(filename) as f:
            nb = nbformat.read(f, as_version=4)
            cells = list(filter(lambda x:x['cell_type'] == 'code' and
                x['execution_count'] is not None, nb.cells))
            nb.cells = cells # assign new cells
            source_cells = [c['source'] for c in nb.cells]
            source_all = "\n".join(source_cells)
            # get func_call and parameter type
            # how to deal with variable func def
            source_all_lines = source_all.split('\n')
            # remove magic functions and linux commands
            source_all_lines = filter(lambda x:len(x)>0 and x[0]!='%' and x[0]!='!', source_all_lines)
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
    cfg = mnode.gen_cfg()
    m_ssa = SSA(source)
    m_ssa.compute_SSA(cfg)
    m_final_idents = m_ssa.compute_final_idents()
    live_ident_table = [m_final_idents]
    undefined_idents = m_ssa.test()
    #print(m_final_idents)
    graph_viz = cfg.build_visual('pdf')
    #graph_viz.render("cfg.pdf", view=True)
    for fun_name, fun_cfg in cfg.functioncfgs.items():
        fun_ssa = SSA(source)
        fun_ssa.compute_SSA(fun_cfg)
        fun_ssa.test(live_ident_table=live_ident_table)
        undefined_idents += fun_ssa.test(live_ident_table=live_ident_table)

    for class_name, class_cfg in cfg.class_cfgs.items():
        # class body ssa compute
        c_ssa = SSA(source)
        c_ssa.compute_SSA(class_cfg)
        c_final_idents = c_ssa.compute_final_idents()
        #print(c_final_idents)
        live_ident_table.append(c_final_idents)
        for inside_fun_name, inside_fun_cfg in class_cfg.functioncfgs.items():
            #if inside_fun_name == 'status_printer':
            #    inside_fun_cfg.build_visual('cfg', 'pdf')
            fun_ssa = SSA(source)
            fun_ssa.compute_SSA(inside_fun_cfg)
            undefined_idents += fun_ssa.test(live_ident_table=live_ident_table)
        live_ident_table.pop()
    print(target_ident)
    print(undefined_idents)
    if target_ident in undefined_idents:
        return True
    return False

def test_SSA_single():
    fn = "fminkin@ML.py" 
    src_path = os.path.join('nameerror-tests', fn)
    exec_log_path = os.path.join("sniffer-dog-exp-data/base/exec_log/", fn.split('.py')[0])
    msg = open(exec_log_path).read()
    name = get_name_from_msg(msg)
    src = open(src_path).read()
    res = test_SSA(src, name)

def test_SSA_batch():
    #filename = sys.argv[1]
    #source = open(filename).read()
    all_fns = os.listdir('nameerror-tests')
    for fn in all_fns:
        #if fn!='djahng@sentiment-rnn.py':
        #    continue
        src_path = os.path.join('nameerror-tests', fn)
        exec_log_path = os.path.join("sniffer-dog-exp-data/base/exec_log/", fn.split('.py')[0])
        msg = open(exec_log_path).read()
        name = get_name_from_msg(msg)
        #src_path ='tmp.py'
        src = open(src_path).read()
        #print(src)
        #print(fn)
        res = test_SSA(src, name)
        if not res:
            print(fn)
        #break

def main():
    #all_rows = open("all.row").readlines()
    all_rows = open("nameerror.row").readlines()
    for row in all_rows:
        line_parts = row.strip().split('|')
        filename = line_parts[-1]
        repo_name = line_parts[1]
        log_dir = os.path.join("/data/sda/jiawei/sniffer-dog-exp-data/base/exec_log/", repo_name)
        content = open(log_dir).read()
        print(repo_name)
        print(content[0:300])
        #print(filename)
        #filename = "/mnt/fit-Knowledgezoo/Github_repos_download/data/diyclassics@mapping-experiments/book-map-ner-htef.ipynb"
        #s = do_single_notebook(filename)
        #f = open('tmp/'+line_parts[1]+ '.py', 'w')
        #f.write(s)
        #f.close() 
        #break
        #break
    return 0
if __name__ == '__main__':
    #main()
    #test_SSA_batch()
    test_SSA_single()
