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

    def draw(self):
        graph = pydot.Dot(graph_type='digraph', rankdir='LR')

        # Add nodes
        for state in self.states:
            node = pydot.Node(state)
            if state in self.accepting_states:
                node.set_shape('doublecircle')
            graph.add_node(node)

        # Add edges
        for (from_state, input_symbol), to_state in self.transitions.items():
            label = input_symbol if input_symbol else "ε"
            edge = pydot.Edge(from_state, to_state, label=label)
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

    def intersect(self, other):
        new_states = set((s1, s2) for s1 in self.states for s2 in other.states)
        new_alphabet = self.alphabet.intersection(other.alphabet)
        new_transitions = {}
        for ((s1, a), s1_dest) in self.transitions.items():
            for ((s2, b), s2_dest) in other.transitions.items():
                if a == b:
                    new_transitions[((s1, s2), a)] = (s1_dest, s2_dest)
        new_initial_state = (self.initial_state, other.initial_state)
        new_accepting_states = set((s1, s2) for s1 in self.accepting_states for s2 in other.accepting_states)
        return Automata(new_states, new_alphabet, new_transitions, new_initial_state, new_accepting_states)

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
