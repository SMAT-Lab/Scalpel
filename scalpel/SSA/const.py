""" 
In this module, the single static assignment forms are implemented to allow
futher anaysis. The module contain a single class named SSA.
"""
import ast
import astor
from functools import reduce
from collections import OrderedDict
import networkx as nx
from ..core.vars_visitor import get_vars
from ..cfg.builder import CFGBuilder, Block, invert
from ..core.mnode import MNode
from ..core.vars_visitor  import get_vars

def parse_val(node):
   # does not return anything
   if isinstance(node, ast.Constant):
       return node.value
   if isinstance(node, ast.Str):
       if hasattr(node, "value"):
           return node.value
       else:
           return node.s
   return "other"

class SSA:
    """
    Build SSA graph from a given AST node based on the CFG.
    """
    def __init__ (self):
        """
        Args:
            src: the source code as input.
        """
        # the class SSA takes a module as the input 
        self.numbering = {}  # numbering variables
        self.var_values = {}  # numbering variables
        self.global_live_idents = []
        self.ssa_blocks = []
        self.error_paths = {}
        self.dom = {}

        self.block_ident_gen = {}
        self.block_ident_use = {}
        self.reachable_table = {}
        id2block = {}
        self.unreachable_names = {}
        self.undefined_names_from = {}
        self.global_names = []

    def get_global_live_vars(self):
        #import_dict = self.m_node.parse_import_stmts()
        #def_records = self.m_node.parse_func_defs()
        #def_idents = [r['name'] for r in def_records if r['scope'] == 'mod']
        #self.global_live_idents = def_idents + list(import_dict.keys())
        self.global_live_idents = []

    def flatten_tuple(ast_tuple):
        """
        input: ast tuple object
        return a list of elements in the given tuple
        """
        output =[]
        first = ast_tuple[0]
        second = ast_tuple[1]

    def get_attribute_stmts(self, stmts):
        call_stmts = []
        for stmt in stmts:
            if isinstance(stmt,ast.Call) and isinstance(stmt.func, ast.Attribute):
                call_stmts += [stmt]

    def get_identifiers(self, ast_node):
        """
        Extract all identifiers from the given AST node.
        Args:
            ast_node: AST node.
        """
        if ast_node is None:
            return []
        res = get_vars(ast_node)
        idents = [r['name'] for r in res if  r['name'] is not None and "." not in r['name']]
        return idents
    

    def compute_SSA(self, cfg):
        """
        Compute single static assignment form representations for a given CFG. 
        During the computing, constant value and alias pairs are generated.
        # step 1a: compute the dominance frontier
        # step 1b: use dominance frontier to place phi node
        # if node X contains assignment to a, put phi node for a in dominance frontier of X
        # adding phi function may require introducing additional phi function 
        # start from the entry node 
        # step2: rename variables so only one definition per name

        Args:
            cfg: a control flow graph.
        """
        # to count how many times a var is defined
        ident_name_counter = {}
        # constant assignment dict
        ident_const_dict = {}
        # step 1a: compute the dominance frontier
        all_blocks = cfg.get_all_blocks()
        id2blocks = {block.id:block for block in all_blocks}

        block_loaded_idents = {block.id:[] for block in all_blocks}
        block_stored_idents = {block.id:[] for block in all_blocks}

        block_const_dict = {block.id:[] for block in all_blocks}

        block_renamed_stored = {block.id:[] for block in all_blocks}
        block_renamed_loaded = {block.id:[] for block in all_blocks}
        
        DF = self.compute_DF(all_blocks)

        for block in all_blocks:
            df_nodes = DF[block.id]
            tmp_const_dict = {}

            for stmt in block.statements:
                stored_idents, loaded_idents, func_names = self.get_stmt_idents_ctx(stmt, const_dict=tmp_const_dict) 
                block_loaded_idents[block.id] += [loaded_idents]
                block_stored_idents[block.id] += [stored_idents]
                block_renamed_loaded[block.id] += [{ident:[] for ident in loaded_idents}]
            block_const_dict[block.id]  = tmp_const_dict
        
        for block in all_blocks:
            stored_idents = block_stored_idents[block.id]
            loaded_idents = block_loaded_idents[block.id]
            n_stmts = len(stored_idents)
            assert (n_stmts == len(loaded_idents))
            affected_idents = []
            tmp_const_dict = block_const_dict[block.id]
            for i in range(n_stmts):
                stmt_stored_idents = stored_idents[i]
                stmt_loaded_idents = loaded_idents[i]
                stmt_renamed_stored =  {}
                for ident in stmt_stored_idents:
                    affected_idents.append(ident)
                    if ident in ident_name_counter:
                        ident_name_counter[ident] += 1
                    else:
                        ident_name_counter[ident] = 0
                    # rename the var name as the number of assignments
                    if ident in tmp_const_dict:
                        ident_const_dict[(ident, ident_name_counter[ident])] = tmp_const_dict[ident]
                    stmt_renamed_stored[ident] = ident_name_counter[ident]
                block_renamed_stored[block.id] += [stmt_renamed_stored]
                

                #same block, number used identifiers
                for ident in stmt_loaded_idents:
                    # a list of dictions for each of idents used in this statement
                    phi_loaded_idents = block_renamed_loaded[block.id][i]
                    if ident in ident_name_counter:
                        phi_loaded_idents[ident].append(ident_name_counter[ident])
                    #if ident in affected_idents:
                    #    phi_loaded_idents = block_renamed_loaded[block.id][i]
                    #    if ident in phi_loaded_idents:  
                    #        phi_loaded_idents[ident].append(ident_name_counter[ident])
                    #else if ident in ident_name_counter:

                        
                        
    
            df_block_ids = DF[block.id]
            for df_block_id in df_block_ids:
                df_block = id2blocks[df_block_id] 
                for af_ident in affected_idents:
                    for phi_loaded_idents in block_renamed_loaded[df_block_id]:
                        # place phi function here
                        # this var used
                        if af_ident in phi_loaded_idents:  
                            phi_loaded_idents[af_ident].append(ident_name_counter[af_ident])
                                       
        #loaded_idents = block_loaded_idents[block.id]
        #print(block_renamed_stored[block.id])
        # now go to all ist DF nodes to rename loaded sets
 #      print(block_stored_idents[block.id])
        
        # TODO: rename those in the dominating nodes 
        # to refer to POST dominating relationships 
        #for b_id, phi_vals in block_renamed_loaded.items():
        #    print(b_id, phi_vals)
        #print('--------------------------')
        #for k, v in ident_const_dict.items():
        #    print(k, v.__dict__)
        return block_renamed_loaded, ident_const_dict

    def get_stmt_idents_ctx(self, stmt, del_set=[], const_dict = {}):
        # if this is a definition of class/function, ignore
        stored_idents = []
        loaded_idents = []
        func_names = []
        # assignment with only one target
        if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1:
            if hasattr(stmt.targets[0], "id"):
                left_name = stmt.targets[0].id
                const_dict[left_name] = stmt.value
            elif isinstance(stmt.targets[0], ast.Attribute):
                #TODO: resolve attributes
                pass
        # one target assignment with type annotations
        if isinstance(stmt, ast.AnnAssign):
            if hasattr(stmt.target, "id"):
                left_name = stmt.targets[0].id
                const_dict[left_name] = stmt.value
            elif isinstance(stmt.target, ast.Attribute):
                #TODO: resolve attributes
                pass
            

        if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
            stored_idents.append(stmt.name)
            func_names.append(stmt.name)
            #for arg in stmt.args.args: 
            #    if isinstance(arg.annotation, ast.Name):
            #        loaded_idents.append(arg.annotation.id)
            #    if isinstance(arg.annotation, ast.Attribute):
            #        if isinstance(arg.annotation.value, ast.Name):
            #            loaded_idents.append(arg.annotation.value.id)
            new_stmt = stmt
            new_stmt.body = []
            ident_info = get_vars(new_stmt)
            for r in ident_info:
                if r['name'] is None or "." in r['name'] or "_hidden_" in r['name']:
                    continue
                if r['usage'] == "load":
                    loaded_idents.append(r['name']) 
            return stored_idents, loaded_idents, func_names
        
        if isinstance(stmt, ast.ClassDef):
            stored_idents.append(stmt.name)
            func_names.append(stmt.name)
            return stored_idents, loaded_idents, func_names

        # if this is control flow statements, we should not visit its body to avoid duplicates
        # as they are already in the next blocks
        if isinstance(stmt, (ast.Import, ast.ImportFrom)):
            for alias in stmt.names:
                if alias.asname is None:
                    stored_idents += [alias.name.split('.')[0]]
                else:
                    stored_idents += [alias.asname.split('.')[0]]
            return stored_idents, loaded_idents, []

        if isinstance(stmt, (ast.Try)):
            for handler in stmt.handlers:
                if handler.name is not None:
                    stored_idents.append(handler.name)
                    
                if isinstance( handler.type, ast.Name):
                    loaded_idents.append(handler.type.id)
                elif isinstance( handler.type, ast.Attribute) and isinstance(handler.type.value, ast.Name):
                    loaded_idents.append(handler.type.value.id)
            return stored_idents, loaded_idents, []
        if isinstance(stmt, ast.Global):
            for name in stmt.names:
                self.global_names.append(name)
            return stored_idents, loaded_idents, []

        visit_node = stmt
        if isinstance(visit_node,(ast.If, ast.IfExp)):
            #visit_node.body = []
            #visit_node.orlse=[]
            visit_node = stmt.test

        if isinstance(visit_node,(ast.With)):
            visit_node.body = []
            visit_node.orlse=[]

        if isinstance(visit_node,(ast.While)):
            visit_node.body = []
        if isinstance(visit_node,(ast.For)):
            visit_node.body = []

        ident_info = get_vars(visit_node)
        for r in ident_info:
            if r['name'] is None or "." in r['name'] or "_hidden_" in r['name']:
                continue
            if r['usage'] == 'store':
                stored_idents.append(r['name'])
            else:
                loaded_idents.append(r['name'])
            if r['usage'] == 'del':
                del_set.append(r['name'])
        return stored_idents, loaded_idents, []


    def to_json(self):
        pass

    def print_block(self, block):
        #for stmt in block.statements:
        #print(block.get_source())
        return block.get_source()

    # compute the dominators 
    def compute_idom(self, ssa_blocks):
        # construct the Graph
        entry_block = ssa_blocks[0]
        G = nx.DiGraph()
        for block in ssa_blocks: 
            G.add_node(block.id)
            exits = block.exits
            preds =  block.predecessors
            for link in preds+exits:
                G.add_edge(link.source.id, link.target.id)
        #DF = nx.dominance_frontiers(G, entry_block.id)
        idom = nx.immediate_dominators(G, entry_block.id)
        return idom

    # compute dominance frontiers
    def compute_DF(self, ssa_blocks):
        # construct the Graph
        entry_block = ssa_blocks[0]
        G = nx.DiGraph()
        for block in ssa_blocks: 
            G.add_node(block.id)
            exits = block.exits
            preds =  block.predecessors
            for link in preds+exits:
                G.add_edge(link.source.id, link.target.id)
        DF = nx.dominance_frontiers(G, entry_block.id)
        #idom = nx.immediate_dominators(G, entry_block.id)
        return DF
