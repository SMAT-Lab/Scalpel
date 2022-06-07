from scalpel.import_graph.import_graph import Tree,ImportGraph


def main():

    target_dir = "./import_graph_example_pkg"
    import_graph = ImportGraph(target_dir)
    import_graph.build_dir_tree()
    all_leaf_ndoes = import_graph.get_leaf_nodes()
    for node in all_leaf_ndoes:
        module_dict = import_graph.parse_import(node.ast)
        print(module_dict)


if __name__ == "__main__":
    main() 
