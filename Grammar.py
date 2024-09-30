class Grammar:
    def __init__(
        self, non_terminals: list, terminals: list, productions: dict, start_symbol: str
    ):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions
        self.start_symbol = start_symbol


# # Definir los terminales y no terminales
# non_terminals = {"E", "T", "F"}
# terminals = {"+", "*", "(", ")", "id"}

# # Definir las producciones usando un diccionario
# productions = {
#     "E": [["E", "+", "T"], ["T"]],
#     "T": [["T", "*", "F"], ["F"]],
#     "F": [["(", "E", ")"], ["id"]],A
# }
