import hashlib
import os

import pydot


class Automata:
    counter = 0

    def __init__(self, states, alphabet, transitions, initial_state, accepting_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.current_state = initial_state
        self.accepting_states = accepting_states

    def transition(self, input_symbol):
        if input_symbol in self.alphabet and (self.current_state, input_symbol) in self.transitions:
            self.current_state = self.transitions[(self.current_state, input_symbol)]
        else:
            print("Invalid input or transition undefined.")

    def is_accepting(self):
        return self.current_state in self.accepting_states

    def intersect(self, other):
        # Definir nuevos estados, transiciones y estados de aceptación
        new_states = set()
        new_transitions = {}
        new_accepting_states = set()

        # Obtener todas las combinaciones de estados
        for state1 in self.states:
            for state2 in other.states:
                new_state = (state1, state2)
                new_states.add(new_state)

                # Si ambos estados son estados de aceptación en sus respectivos autómatas, entonces el nuevo estado también es de aceptación
                if state1 in self.accepting_states and state2 in other.accepting_states:
                    new_accepting_states.add(new_state)

                # Verificar todas las combinaciones de transiciones
                for symbol in self.alphabet:
                    if (state1, symbol) in self.transitions and (state2, symbol) in other.transitions:
                        new_transitions[(new_state, symbol)] = (
                            self.transitions[(state1, symbol)], other.transitions[(state2, symbol)]
                        )

        # Crear un nuevo autómata con los estados, transiciones y estados de aceptación calculados
        intersected_automaton = Automata(new_states, self.alphabet, new_transitions,
                                         (self.initial_state, other.initial_state), new_accepting_states)

        return intersected_automaton

    def draw(self):
        graph = pydot.Dot(graph_type='digraph', rankdir='LR')

        # Add nodes
        for state in self.states:
            state_name = '-'.join(state) if isinstance(state, tuple) else state
            node = pydot.Node(state_name)  # Convert state to a more readable string
            if state in self.accepting_states:
                node.set_shape('doublecircle')
            graph.add_node(node)

        # Add edges
        for (from_state, input_symbol), to_state in self.transitions.items():
            from_state_name = '-'.join(from_state) if isinstance(from_state, tuple) else from_state
            to_state_name = '-'.join(to_state) if isinstance(to_state, tuple) else to_state
            label = input_symbol if input_symbol else "ε"
            edge = pydot.Edge(from_state_name, to_state_name, label=label)
            graph.add_edge(edge)

        folder_path = 'imagenesGeneradas'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        Automata.counter += 1

        filename = f'{self.states}{self.alphabet}{self.transitions}{self.current_state}{self.accepting_states}'
        filename_hash = hashlib.md5(filename.encode()).hexdigest()
        filename_png = f'{folder_path}/automata_{filename_hash}_{Automata.counter}.png'
        graph.write_png(filename_png, encoding='utf-8')
        return filename_png

    def reverse(self):
        new_transitions = {}
        for (from_state, input_symbol), to_state in self.transitions.items():
            if (to_state, input_symbol) not in new_transitions:
                new_transitions[(to_state, input_symbol)] = from_state
            else:
                new_transitions[(to_state, input_symbol)].add(from_state)
        new_initial_state = tuple(self.accepting_states)
        new_accepting_states = {self.initial_state}
        return Automata(self.states, self.alphabet, new_transitions, new_initial_state, new_accepting_states)
