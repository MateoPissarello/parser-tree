from Grammar import Grammar
from pprint import pprint
from Node import Node
import networkx as nx
import matplotlib.pyplot as plt

EPSILON = "ε"  # Definir EPSILON como el símbolo de producción vacía


class LL1_Parser:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.first = {}
        self.follow = {}
        self.table = {}
        self.generate_first()
        self.generate_follow()
        self.generate_table()

    def generate_first(self):
        non_terminals = list(self.grammar.non_terminals)[::-1]
        for non_terminal in non_terminals:
            self.first[non_terminal] = self._first_of(non_terminal)

    def generate_follow(self):
        for non_terminal in self.grammar.non_terminals:
            self.follow[non_terminal] = set()
        self.follow[self.grammar.start_symbol].add("$")
        for non_terminal in self.grammar.non_terminals:
            #if non_terminal != self.grammar.start_symbol:
            self._follow_of(non_terminal)

    def generate_table(self):
        # self.grammar.terminals.append("$")
        terminal_symbols = self.grammar.terminals + ["$"]
        for non_terminal in self.grammar.non_terminals:
            self.table[non_terminal] = {}
            for terminal in terminal_symbols:
                self.table[non_terminal][terminal] = None
            if EPSILON in self.first[non_terminal]:
                follow_set = self.follow[non_terminal]
                for terminal in follow_set:
                    self.table[non_terminal][terminal] = EPSILON
            for terminal in terminal_symbols:
                if self.first[non_terminal].intersection({terminal}):
                    self.table[non_terminal][terminal] = self.grammar.productions[
                        non_terminal
                    ][0]

    def _follow_of(self, non_terminal):
        for non_term_symb, production_rules in self.grammar.productions.items():
            for rule in production_rules:
                if non_terminal in rule:
                    idx = rule.index(non_terminal)
                    if idx == len(rule) - 1:
                        if non_term_symb != non_terminal:
                            self.follow[non_terminal].update(self.follow[non_term_symb])
                    else:
                        self._calculate_follow(non_terminal, idx, 1, rule)

    def _calculate_follow(self, non_terminal, idx, n, rule):
        next_symbol = rule[idx + n]
        if next_symbol in self.grammar.terminals:
            self.follow[non_terminal].add(next_symbol)
        else:
            first = self.first[next_symbol]
            if EPSILON in first:
                first_copy = first.copy()
                first_copy.remove(EPSILON)
                self.follow[non_terminal].update(first_copy)
                self._calculate_follow(non_terminal, idx, n + 1, rule)
            else:
                self.follow[non_terminal].update(first)

    def _first_of(self, non_terminal):
        first = set()
        for production in self.grammar.productions[non_terminal]:
            if production[0] in self.grammar.terminals:
                first.add(production[0])
            elif production[0] == EPSILON:
                first.add(EPSILON)
            else:
                first.update(self.first[production[0]])
        return first

    def add_edges(self, G, node):
        for child in node.children:
            G.add_edge(node.value, child.value)
            self.add_edges(G, child)

    def draw_tree(self, root):
        G = nx.DiGraph()
        self.add_edges(G, root)  # Pasar el grafo y la raíz del árbol

        # Usar graphviz_layout para dibujar el árbol en forma jerárquica
        pos = nx.nx_agraph.graphviz_layout(G, prog="dot")

        nx.draw(
            G,
            pos,
            with_labels=True,
            arrows=False,
            node_size=3000,
            node_color="lightblue",
        )
        plt.show()

    def generate_parse_tree(self, string):
        i = 0  # Apuntador en la cadena de entrada
        root_production = self.grammar.productions[self.grammar.start_symbol][0]  # Obtener la producción inicial
        root_production.reverse()  # Revertir la producción para insertar en el stack

        stack = ["$"]+root_production  # Iniciar el stack con símbolo de fin y símbolo inicial
        root = Node(self.grammar.start_symbol)  # Nodo raíz del árbol
        current_node = root  # Apuntador al nodo actual en el árbol
        input_string = list(string) + ["$"]  # Cadena de entrada con símbolo de fin
        

        while stack:
            top = stack.pop()  # Obtener el elemento superior del stack
            current_input = input_string[i]

            # Manejar el símbolo epsilon
            if top == EPSILON:
                # Añadir un nodo epsilon al árbol como hijo del no terminal actual
                epsilon_node = Node(EPSILON, current_node)
                current_node.add_child(epsilon_node)
                current_node = current_node.parent  # Volver al nodo padre
                continue  # Saltar al siguiente símbolo

            # Si es terminal
            if top == "$":
                print("Análisis completado.")
                return root
            if top in self.grammar.terminals :
                if top == current_input:  # Si coinciden, avanzar en la cadena
                    i += 1
                    terminal_node = Node(top, current_node)  # Crear un nodo terminal
                    current_node.add_child(terminal_node)
                    current_node = root # Volver al nodo padre
                else:
                    raise SyntaxError(f"Error de análisis: Se esperaba {top} pero se encontró {current_input}.")

            else:  # Si es un no terminal
                rule = self.table[top].get(current_input)
                if not rule:
                    raise SyntaxError(f"Error de análisis: No hay regla para {top} con {current_input}.")

                # Crear un nodo para la producción
                production_node = Node(top, current_node)

                # Insertar los símbolos de la producción en el orden correcto
                for symbol in rule:
                    if symbol != EPSILON:
                        child_node = Node(symbol, production_node)
                        production_node.add_child(child_node)

                # Agregar el nodo de la producción al árbol
                current_node.add_child(production_node)

                # Insertar la producción al stack (en orden inverso para procesar en el orden correcto)
                for symbol in reversed(rule):
                    stack.append(symbol)

                current_node = production_node  # Moverse al nuevo nodo

        return root  # Retornar la raíz del árbol de análisis


if __name__ == "__main__":
   # Definir los terminales y no terminales
    non_terminals = ["S", "A", "B"]
    terminals = ["a", "b", "c", "d"]

    # Definir las producciones usando un diccionario
    productions = {
        "S": [["a", "A", "B", "b"]],
        "A": [["c"], ["ε"]],
        "B": [["d"], ["ε"]],
    }

#    terminals = ["(", ")"]
#    non_terminals = ["S"]
#    productions = {
#          "S": [["(", "S", ")"],
#             ["ε"]],

#      }


grammar = Grammar(non_terminals, terminals, productions, "S")
parser = LL1_Parser(grammar)
pprint(parser.table)
pprint(parser.first)
pprint(parser.follow)
tree = parser.generate_parse_tree("adb")
pprint(tree)
parser.draw_tree(tree)

    # pprint(parser.table)
    # pprint(parser.first)