def parse_grammar(file_path):
    tree = {}
    nodo_raiz = None  # Variable para almacenar el primer nodo (símbolo inicial)

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if "->" in line:
                lhs, rhs = line.split("->")
                lhs = lhs.strip()  # Lado izquierdo (no terminal)
                rhs = rhs.strip().split()  # Lado derecho separado por símbolos

                # Si aún no se ha definido el nodo raíz, lo asignamos al primer LHS encontrado
                if nodo_raiz is None:
                    nodo_raiz = lhs

                # Crear nodos en el diccionario basado en las producciones
                if lhs not in tree:
                    tree[lhs] = {}

                # Procesar cada producción de manera secuencial
                current_node = tree[lhs]
                for symbol in rhs:
                    for char in symbol:  # Procesar cada símbolo por separado
                        if char not in current_node:
                            current_node[char] = {}
                        current_node = current_node[char]  # Moverse al siguiente nivel del árbol

    return nodo_raiz , tree # Devolvemos el árbol y el nodo raíz

