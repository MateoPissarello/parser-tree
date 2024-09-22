#!/usr/bin/env python3

import argparse
from utils import parse_grammar
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
        pp = pprint.PrettyPrinter(indent=4)
        tree = parse_grammar(path)
        pp.pprint(tree)
        # parser = Parser(tree)

        # parser.draw_tree()

    else:
        print("No se proporcionó ningún archivo.")


if __name__ == "__main__":
    main()
