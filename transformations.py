from first_follow_prediction import GrammarProcessor

non_terminals, terminals, productions = GrammarProcessor("rules.txt").process_grammar()