#!/usr/bin/env python3
import argparse
from ParserLL1 import LL1_Parser
from Grammar import Grammar


def leer_reglas_archivo(archivo):
    with open(archivo, "r") as f:
        contenido = f.read()
    return contenido


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
