import os
import pydot


class Automata:
    counter = 0
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

        folder_path = 'imagenesGeneradas'
        # Verifica si la carpeta existe. Si no, la crea.
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Guardar y mostrar el diagrama
        Automata.counter += 1  # Incrementa el contador cada vez que se dibuja un nuevo autómata
        filename_png = f'{folder_path}/automata_{Automata.counter}.png'
        graph.write_png(filename_png, encoding='utf-8')
        return filename_png


