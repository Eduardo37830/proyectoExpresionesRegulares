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
    i = 0
    
    while i < len(regex):
        if i == len(regex) - 1:
            if regex[i] == "*":
                add_transition(current_state, current_state, "")
            elif regex[i] == "+":
                add_transition(current_state, current_state, "")
                accepting_states.add(current_state)
            else:
                add_transition(current_state, 'q' + str(i + 1), regex[i])
                accepting_states.add('q' + str(i + 1))
        elif regex[i] == "|":

            new_state1='q'+ str(i)
            new_state2='q'+ str(i)
            accepting_states.add(new_state1)
            accepting_states.add(new_state2)
            current_state = initial_state
            i += 1
            continue
        elif regex[i + 1] == "*":
            new_state = 'q' + str(i + 1)
            add_transition(current_state, current_state, regex[i])
            accepting_states.add(current_state)
            current_state = new_state
            i += 1
        elif regex[i + 1] == "+":
            new_state = 'q' + str(i + 1)
            add_transition(current_state, new_state, regex[i])
            add_transition(new_state, new_state, regex[i])
            accepting_states.add(new_state)
            current_state = new_state
            i += 1
        else:
            new_state = 'q' + str(i + 1)
            add_transition(current_state, new_state, regex[i])
            current_state = new_state
        i += 1

    return Automata(states, alphabet, transitions, initial_state, accepting_states)

# Ejemplo de uso:
regex = input("Ingrese la expresión regular: ")
automaton = build_automaton_from_regex(regex)
print(automaton.states)
automaton.draw()
