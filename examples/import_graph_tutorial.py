import os
from scalpel.import_graph.import_graph import Tree,ImportGraph


path_to_current_file = os.path.realpath(__file__)
current_directory = os.path.split(path_to_current_file)[0]
root_node = Tree("import_graph_example_pkg")
import_graph = ImportGraph(os.path.join(current_directory,"import_graph_example_pkg"))
import_graph.build_dir_tree()
module_dict = import_graph.parse_import(root_node)


