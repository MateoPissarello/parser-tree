#!/usr/bin/env python3
import argparse
import FileHandler
from Grammar import Grammar
from ParserLL1 import LL1_Parser


def leer_reglas_archivo(archivo):
    with open(archivo, "r") as f:
        contenido = f.read()
    return contenido


def print_ll1_table(table):
    # Extract the headers (terminals and end marker)
    headers = sorted(list(next(iter(table.values())).keys()))

    # Print header row
    header_row = f"{'Non-Terminals':<12} | " + " | ".join(f"{h:<5}" for h in headers)
    print(header_row)
    print("-" * len(header_row))

    # Print each row for the non-terminals
    for non_terminal, transitions in table.items():
        row = f"{non_terminal:<12} | " + " | ".join(
            f"{str(transitions[h]):<5}" for h in headers
        )
        print(row)


def process_grammar_v2(path) -> list:
    contenido = FileHandler.LineByLineReadStrategy().read(path)
    non_terminals = []
    terminals = []
    productions = {}
    for line in contenido:
        line = line.replace("\n", "")
        rule, production = line.split("->")
        print("Rule: ", rule)

        rule = list(rule.strip())[0]
        production = production.strip().split(" ")

        # Add rule to non_terminals
        if is_non_terminal(rule) and rule not in non_terminals:
            non_terminals.append(rule)
        for char in production:
            if is_terminal(char):
                if char not in terminals:
                    terminals.append(char)
            elif is_non_terminal(char):
                if char not in non_terminals:
                    non_terminals.append(char)

        if rule not in productions:
            productions[rule] = []
            productions[rule].append(production)
        else:
            productions[rule].append(production)

    return [non_terminals, terminals, productions]


def is_terminal(symbol):
    if not symbol.isupper() and symbol != "ε":
        return True


def is_non_terminal(symbol):
    return symbol.isupper()


def main():
    parser = argparse.ArgumentParser(description="Parser LL1")
    parser.add_argument("-f", type=str, required=True, help="Archivo de reglas")
    args = parser.parse_args()

    path = args.f.strip()

    non_terminals, terminals, productions = process_grammar_v2(path)

    print("Non-terminals: ", non_terminals)
    print("Terminals: ", terminals)
    print("Productions: ", productions)

    # Crear la gramática
    grammar = Grammar(non_terminals, terminals, productions, non_terminals[0])

    # Crear el parser
    ll1_parser = LL1_Parser(grammar)

    # Mostrando conjunto FIRST
    print("\nConjunto FIRST:")
    print("*" * 50)
    for key, value in ll1_parser.first.items():
        print(f"{key}: {value}")
    print("*" * 50)

    # Mostrando conjunto FOLLOW
    print("\nConjunto FOLLOW:")
    print("*" * 50)
    for key, value in ll1_parser.follow.items():
        print(f"{key}: {value}")
    print("*" * 50)

    # Mostrando tabla de parsing
    print("\nTabla de predicción:")
    print("*" * 50)
    print_ll1_table(ll1_parser.table)
    print("*" * 50)

    # # Crear un diccionario para almacenar las variables
    # variables = {}

    # # Ejecutar el código en el archivo de texto
    # exec(contenido, variables)

    # # Obtener las variables definidas en el archivo de texto
    # non_terminals = variables["non_terminals"]
    # terminals = variables["terminals"]
    # productions = variables["productions"]

    # # Crear la gramática
    # grammar = Grammar(non_terminals, terminals, productions, "S")

    # # Crear el parser
    # parser_ll1 = LL1_Parser(grammar)

    # # Imprimir la tabla de parsing
    # print("Tabla de parsing:")
    # print(parser_ll1.table)

    # # Imprimir el conjunto FIRST
    # print("\nConjunto FIRST:")
    # print(parser_ll1.first)

    # # Imprimir el conjunto FOLLOW
    # print("\nConjunto FOLLOW:")
    # print(parser_ll1.follow)

    # # Generar el árbol de parsing
    # try:
    #     tree = parser_ll1.generate_parse_tree(input("Ingrese la cadena de entrada: "))
    #     print("\nÁrbol de parsing:")
    #     print(tree)

    #     # Dibujar el árbol de parsing
    #     parser_ll1.draw_tree(tree)
    # except SyntaxError as e:
    #     print(f"Error de sintaxis: {e}")


if __name__ == "__main__":
    main()
