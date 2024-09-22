def parse_grammar(file_path):
    tree = {}

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if "->" in line:
                lhs, rhs = line.split("->")
                lhs = lhs.strip()  # Lado izquierdo (no terminal)
                rhs = rhs.strip()

                for production in rhs:
                    production = production.strip()  # Cada producción
                    if lhs not in tree:
                        tree[lhs] = {}

                    # Crear nodos en el diccionario
                    node = create_node(production)
                    tree[lhs].update(node)

    return tree


def create_node(production):
    parts = []
    index = 1  # Para numerar ocurrencias

    # Separa la producción en partes
    for part in production:
        if part.isupper():  # Si es no terminal
            parts.append(f"{part}{index}")
            index += 1
        else:
            parts.append(part)

    # Crea un diccionario a partir de las partes
    node = {}
    for part in parts:
        if part not in node:
            node[part] = {}

    return node


