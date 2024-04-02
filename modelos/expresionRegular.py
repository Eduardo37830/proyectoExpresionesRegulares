# NOTA:Este código fue tomado de exp3.py

import pydot


class Automata:
    def __init__(self, states, alphabet, transitions, initial_state, accepting_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.current_state = initial_state
        self.accepting_states = accepting_states

    def transition(self, input_symbol):
        if input_symbol in self.alphabet and (self.current_state, input_symbol) in self.transitions:
            self.current_state = self.transitions[(self.current_state, input_symbol)]
        else:
            print("Invalid input or transition undefined.")

    def is_accepting(self):
        return self.current_state in self.accepting_states

    def draw(self):
        graph = pydot.Dot(graph_type='digraph')

        # Agregar nodos
        for state in self.states:
            node = pydot.Node(state)
            if state in self.accepting_states:
                node.set_shape('doublecircle')
            graph.add_node(node)

        # Agregar arcos
        for (from_state, input_symbol), to_state in self.transitions.items():
            label = input_symbol
            if input_symbol == "":
                label = "ε"  # Para transiciones epsilon
            edge = pydot.Edge(from_state, to_state, label=label)
            graph.add_edge(edge)

        # Guardar y mostrar el diagrama
        graph.write_png('automata.png', encoding='utf-8')
        graph.write_pdf('automata.pdf', encoding='utf-8')


