import networkx as nx
import matplotlib.pyplot as plt

# G = nx.petersen_graph()
# subax1 = plt.subplot(121)
# nx.draw(G, with_labels=True, font_weight='bold')
# subax2 = plt.subplot(122)
# nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')


test_tree = {
    "S": {
        "A1": {  # Primera ocurrencia de A
            "alias": "A",
            "a": {"alias": "a"},
            "A2": {"b": {"alias": "b"}, "alias": "A"},  # Segunda ocurrencia de A
        },
        "S1": {"d": {"alias": "d"}, "alias": "S"},  # Primera ocurrencia de S
        "B": {
            "alias": "B",
            "d1": {"alias": "d"},  # Primera ocurrencia de d
            "c": {"alias": "c"},
            "d2": {"alias": "d"},  # Segunda ocurrencia de d
        },
        "alias": "S",
    }
}


class Parser:
    def __init__(self, tree):
        self.tree = tree
        self.generate_tree()

    def generate_tree(self):
        self.aliases = {}
        generate_tree = nx.DiGraph()

        def add_edges(node, children):
            node_alias = children.pop("alias", node)
            self.aliases[node] = node_alias
            for child, grandchildren in children.items():
                generate_tree.add_edge(node, child)
                if grandchildren:
                    add_edges(child, grandchildren)

        for node, children in self.tree.items():
            add_edges(node, children)
        self.tree = generate_tree

    def draw_tree(self):
        pos = nx.nx_pydot.graphviz_layout(self.tree, prog="dot")
        labels = {node: self.aliases[node] for node in self.tree.nodes}
        # Dibujar el árbol
        nx.draw(
            self.tree,
            pos,
            labels=labels,
            node_color="lightblue",
            node_size=2000,
            font_size=10,
            font_weight="bold",
            with_labels=True,
            arrows=False,
        )
        plt.show()


if __name__ == "__main__":
    parser = Parser(test_tree)
    parser.draw_tree()
