from scalpel.import_graph.import_graph import ImportGraph, Tree


def main():
    target_dir = "./import_graph_example_pkg"
    import_graph = ImportGraph(target_dir)
    import_graph.build_dir_tree()
    all_leaf_nodes = import_graph.get_leaf_nodes()
    for node in all_leaf_nodes:
        module_dict = import_graph.parse_import(node.ast)
        print(module_dict)


if __name__ == "__main__":
    main()
