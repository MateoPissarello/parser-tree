def parse_grammar(grammar_file):
    grammar_tree = {}

    with open(grammar_file, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                production = line.split("->")
                left_side = production[0].strip()
                right_side = production[1].strip()
                if left_side not in grammar_tree:
                    grammar_tree[left_side] = []
                if "," in right_side:
                    right_side = right_side.split(",")
                elif " " in right_side:
                    right_side = right_side.split(" ")
                else:
                    right_side = [right_side]
                grammar_tree[left_side].append(right_side)
    return grammar_tree


def parse_input(input_string, nodo_raiz, grammar_tree):
    def recursive_parse(remaining_input, current_rule):
        print(f"Remaining input: {remaining_input}, Current rule: {current_rule}")
        if not remaining_input and not current_rule:
            print("Matched entire input string")
            return True
        if not remaining_input or not current_rule:
            print("No more input or current rule")
            return False

        symbol = current_rule[0]

        # Matching terminal symbols
        if symbol.islower() and remaining_input and remaining_input[0] == symbol:
            print(f"Matching terminal symbol: {symbol}")
            return recursive_parse(remaining_input[1:], current_rule[1:])

        # Expanding non-terminal symbols
        if symbol.isupper():
            print(f"Expanding non-terminal symbol: {symbol}")
            for production in grammar_tree.get(symbol, []):
                print(f"Trying production: {production} for symbol {symbol}")
                if recursive_parse(remaining_input, production + current_rule[1:]):
                    print(f"Production {production} matched for symbol {symbol}")
                    return True
                print(f"Production {production} did not match for symbol {symbol}")
            print(f"No productions matched for symbol {symbol}")
            return False

        # If symbol is not a terminal or non-terminal
        print(f"Unrecognized symbol: {symbol}")
        return False

    return recursive_parse(list(input_string), [nodo_raiz])  # Convertir a lista


def generate_syntax_tree(input_string, nodo_raiz, grammar_tree):
    syntax_tree = {}

    def recursive_tree(remaining_input, current_rule, tree_node):
        if not remaining_input or not current_rule:
            return

        symbol = current_rule[0]

        if symbol.islower() and remaining_input[0] == symbol:
            tree_node[symbol] = {}
            recursive_tree(remaining_input[1:], current_rule[1:], tree_node[symbol])
        elif symbol.isupper():
            for production in grammar_tree.get(symbol, []):
                subtree = {}
                tree_node[symbol] = subtree
                recursive_tree(remaining_input, production + current_rule[1:], subtree)

    recursive_tree(input_string, [nodo_raiz], syntax_tree)
    return syntax_tree
