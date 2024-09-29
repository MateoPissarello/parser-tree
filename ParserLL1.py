from Grammar import Grammar

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
            if non_terminal != self.grammar.start_symbol:
                self._follow_of(non_terminal)

    def generate_table(self):
        self.grammar.terminals.append("$")
        for non_terminal in self.grammar.non_terminals:
            self.table[non_terminal] = {}
            for terminal in self.grammar.terminals:
                self.table[non_terminal][terminal] = None
            if EPSILON in self.first[non_terminal]:
                follow_set = self.follow[non_terminal]
                for terminal in follow_set:
                    self.table[non_terminal][terminal] = EPSILON
            for terminal in self.grammar.terminals:
                if self.first[non_terminal].intersection({terminal}):
                    self.table[non_terminal][terminal] = self.grammar.productions[
                        non_terminal
                    ][0]

    def _follow_of(self, non_terminal):
        for non_term_symb, production_rules in productions.items():
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

    def generate_parse_tree(self, string):
        # TODO: CHECK GENERATE PARSE TREE METHOD
        string = string + "$"
        parsing_tree = {}
        stack = ["$", self.grammar.start_symbol]
        current_node = self.grammar.start_symbol
        parsing_tree[current_node] = {}
        idx = 0
        while stack:
            top = stack[-1]

            # Si el top es un terminal
            if top in self.grammar.terminals:
                if top == string[idx]:
                    # Agregar terminal al árbol de parseo
                    parsing_tree[current_node][top] = {}
                    stack.pop()
                    idx += 1
                else:
                    return False
            elif top == "$" and string[idx] == "$":
                print("Success")
                break
            elif top == EPSILON:
                parsing_tree[current_node][EPSILON] = {}
                stack.pop()
            elif top in self.grammar.non_terminals:
                # Sacar el no terminal del stack y agregar al árbol de parseo
                node = stack.pop()
                current_node = node
                if current_node not in parsing_tree:
                    parsing_tree[current_node] = {}

                production = self.table[top][string[idx]]
                if production:
                    # Agregar la producción al árbol en orden
                    for symbol in production[::-1]:
                        stack.append(symbol)
                else:
                    return False
            else:
                return False

        return parsing_tree


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

    grammar = Grammar(non_terminals, terminals, productions, "S")
    parser = LL1_Parser(grammar)
    tree = parser.generate_parse_tree("adb")
    print(tree)
