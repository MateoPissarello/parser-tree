class Node:
    def __init__(self, value, parent=None):
        self.value = value  # Símbolo del nodo (terminal o no terminal)
        self.parent = parent  # Nodo padre
        self.children = []  # Lista de hijos

    def add_child(self, child_node):
        self.children.append(child_node)

    def __repr__(self):
        return f"Node({self.value})"
