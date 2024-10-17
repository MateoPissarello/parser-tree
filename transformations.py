from first_follow_prediction import GrammarProcessor
from Grammar import Grammar

# Procesa la gramática desde el archivo de texto
non_terminals, terminals, productions = GrammarProcessor(
    "grammar/common_factor_1.txt"
).process_grammar()

test_grammar = Grammar(non_terminals, terminals, productions, non_terminals[0])


def delete_left_recursion(grammar: Grammar) -> Grammar:
    new_productions = {}
    for non_terminal in grammar.non_terminals:
        if grammar.productions.get(non_terminal):
            new_productions[non_terminal] = []
        non_recursive = []
        recursive = []

        # Separar las producciones recursivas y no recursivas
        for production in grammar.productions.get(non_terminal, []):
            if not production:
                continue
            if production[0] == non_terminal:
                recursive.append(production[1:])  # Producción recursiva
            else:
                non_recursive.append(production)  # Producción no recursiva

        # Si hay producciones recursivas
        if recursive:
            new_non_terminal = non_terminal + "'"
            # Asegurarse de que el nuevo no terminal no exista ya
            while new_non_terminal in grammar.non_terminals:
                new_non_terminal += "'"
            new_productions[new_non_terminal] = []

            # Procesar las producciones no recursivas
            for beta in non_recursive:
                # Evita añadir producciones duplicadas
                if [*beta, new_non_terminal] not in new_productions[non_terminal]:
                    new_productions[non_terminal].append([*beta, new_non_terminal])

            # Procesar las producciones recursivas
            for alpha in recursive:
                # Evita añadir producciones duplicadas
                if [*alpha, new_non_terminal] not in new_productions[new_non_terminal]:
                    new_productions[new_non_terminal].append([*alpha, new_non_terminal])

            # Añadir la producción epsilon (cadena vacía)
            new_productions[new_non_terminal].append(["ε"])
        else:
            # Si no hay recursión, simplemente copia las producciones no recursivas
            if non_terminal in new_productions:
                new_productions[non_terminal].extend(non_recursive)

    return Grammar(
        (
            new_productions[non_terminal].extend(non_recursive)
            if recursive
            else grammar.non_terminals
        ),
        grammar.terminals,
        new_productions,
        grammar.start_symbol,
    )


def factor_common_prefix(grammar: Grammar) -> Grammar:
    new_productions = {}
    for non_terminal in grammar.non_terminals:
        productions = grammar.productions.get(non_terminal, [])
        common_prefixes = {}
        if not productions:
            continue
        # Agrupar producciones por prefijo común
        for prod in productions:
            prefix = prod[0]
            if prefix not in common_prefixes:
                common_prefixes[prefix] = []
            common_prefixes[prefix].append(prod)

        # Crear nuevas reglas para manejar prefijos comunes
        new_productions[non_terminal] = []
        for prefix, prods in common_prefixes.items():
            if len(prods) == 1:
                # No hay prefijo común
                new_productions[non_terminal].append(prods[0])
            else:
                # Hay prefijo común, crear un nuevo no terminal
                new_non_terminal = non_terminal + "'"
                while new_non_terminal in grammar.non_terminals:
                    new_non_terminal += "'"

                new_productions[non_terminal].append([prefix] + [new_non_terminal])
                new_productions[new_non_terminal] = []

                for prod in prods:
                    if len(prod) > 1:
                        new_productions[new_non_terminal].append(prod[1:])
                    else:
                        new_productions[new_non_terminal].append(["ε"])

    return Grammar(
        grammar.non_terminals + [new_non_terminal],
        grammar.terminals,
        new_productions,
        grammar.start_symbol,
    )


new_grammar = factor_common_prefix(test_grammar)

# new_grammar = delete_left_recursion(test_grammar)

# # Imprimir las nuevas producciones sin duplicados
# print("Nueva Grammar:")
for non_terminal, prods in new_grammar.productions.items():
    # Eliminar duplicados antes de imprimir
    unique_prods = []
    for prod in prods:
        if prod not in unique_prods:
            unique_prods.append(prod)
    print(f"{non_terminal} -> {unique_prods}")
