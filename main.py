#!/usr/bin/env python3
import argparse
from utils import parse_grammar, parse_input, generate_syntax_tree
import pprint

def main():
    parser = argparse.ArgumentParser(description="Generate a parser tree")

    parser.add_argument("-f", "--file", type=str, help="El nombre del archivo")

    try:
        args = parser.parse_args()
    except SystemExit:
        parser.print_help()
        exit(0)

    if args.file:
        path = args.file.strip()
        grammar_tree = parse_grammar(path)
        nodo_raiz = 'S'

        # Parse the input string from the console
        input_string = input("Enter an input string: ")

        try:
            # Pasa nodo_raiz también
            if parse_input(input_string, nodo_raiz, grammar_tree):
                syntax_tree = generate_syntax_tree(input_string, nodo_raiz, grammar_tree)
                pp = pprint.PrettyPrinter(indent=4)
                pp.pprint(syntax_tree)
            else:
                print("Invalid input string")
        except SyntaxError as e:
            print("Syntax error:", e)

    else:
        print("No se proporcionó ningún archivo.")

if __name__ == "__main__":
    main()