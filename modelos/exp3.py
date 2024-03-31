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
        graph.write_png('automata.png')
        graph.write_pdf('automata.pdf')

def build_automaton_from_regex(regex):
    states = set()  # Conjunto de estados
    alphabet = set()  # Alfabeto
    transitions = {}  # Transiciones representadas como un diccionario
    initial_state = 'q0'  # Estado inicial
    accepting_states = set()  # Conjunto de estados de aceptación

    # Función para agregar una transición
    def add_transition(from_state, to_state, input_symbol):
        nonlocal states, alphabet, transitions
        states.add(from_state)
        states.add(to_state)
        alphabet.add(input_symbol)
        transitions[(from_state, input_symbol)] = to_state
    current_state = initial_state
    
    for i in range(len(regex)):
        if i == 0:
            add_transition('q0', 'q1', regex[i])
        elif i == len(regex) - 1:
            if regex[i] == "*":
                add_transition('q1', 'q1', "")
            elif regex[i] == "+":
                add_transition('q1', 'q2', "")
                accepting_states.add('q2')
            else:
                add_transition('q1', 'q2', regex[i])
                accepting_states.add('q2')
        else:
            new_state = 'q' + str(i + 1)
            if regex[i] == "*":
                add_transition('q' + str(i), 'q' + str(i), "")
            else:
                add_transition('q' + str(i), new_state, regex[i])

    return Automata(states, alphabet, transitions, initial_state, accepting_states)

# Ejemplo de uso:
regex = input("Ingrese la expresión regular: ")
automaton = build_automaton_from_regex(regex)
automaton.draw()