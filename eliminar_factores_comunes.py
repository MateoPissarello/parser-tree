import argparse
from ParserLL1 import LL1_Parser
from Grammar import Grammar
from Node import Node

def leer_reglas_archivo(archivo):
    with open(archivo, "r") as f:
        contenido = f.read()
    return contenido

def eliminar_factores_comunes(productions):
    new_productions = {}
    new_non_terminals = set()
    for non_terminal, rules in productions.items():
        prefix_dict = {}
        for rule in rules:
            prefix = rule[0]
            if prefix not in prefix_dict:
                prefix_dict[prefix] = []
            prefix_dict[prefix].append(rule[1:])
        
        new_rules = []
        for prefix, sub_rules in prefix_dict.items():
            if len(sub_rules) > 1:
                new_non_terminal = f"{non_terminal}'"
                new_non_terminals.add(new_non_terminal)
                new_productions[new_non_terminal] = sub_rules
                new_rules.append([prefix, new_non_terminal])
            else:
                new_rules.append([prefix] + sub_rules[0])
        new_productions[non_terminal] = new_rules
    return new_productions, new_non_terminals

def main():
    parser = argparse.ArgumentParser(description="Parser LL1")
    parser.add_argument("-f", type=str, required=True, help="Archivo de reglas")
    args = parser.parse_args()
    contenido = leer_reglas_archivo(args.f)
    # Crear un diccionario para almacenar las variables
    variables = {}
    # Ejecutar el código en el archivo de texto
    exec(contenido, variables)
    # Obtener las variables definidas en el archivo de texto
    non_terminals = variables["non_terminals"]
    terminals = variables["terminals"]
    productions = variables["productions"]
    # Eliminar factores comunes
    productions, new_non_terminals = eliminar_factores_comunes(productions)
    non_terminals.update(new_non_terminals)
    # Crear la gramática
    grammar = Grammar(non_terminals, terminals, productions, "S")
    # Crear el parser
    parser_ll1 = LL1_Parser(grammar)
    # Imprimir la tabla de parsing
    print("Tabla de parsing:")
    print(parser_ll1.table)
    # Imprimir el conjunto FIRST
    print("\nConjunto FIRST:")
    print(parser_ll1.first)
    # Imprimir el conjunto FOLLOW
    print("\nConjunto FOLLOW:")
    print(parser_ll1.follow)
    # Generar el árbol de parsing
    try:
        tree = parser_ll1.generate_parse_tree(input("Ingrese la cadena de entrada: "))
        print("\nÁrbol de parsing:")
        print(tree)
        # Dibujar el árbol de parsing
        parser_ll1.draw_tree(tree)
    except SyntaxError as e:
        print(f"Error de sintaxis: {e}")

if __name__ == "__main__":
    main()
