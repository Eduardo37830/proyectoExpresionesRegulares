from modelos.expresionRegular import Automata

class ControladorExpresion:
    @staticmethod
    def build_automaton_from_regex(regex):
        states = set()
        alphabet = set()
        transitions = {}
        initial_state = 'q0'
        accepting_states = set()

        def add_transition(from_state, to_state, input_symbol):
            nonlocal states, alphabet, transitions
            states.add(from_state)
            states.add(to_state)
            alphabet.add(input_symbol)
            transitions[(from_state, input_symbol)] = to_state

        def parse_regex(substr, start_state):
            nonlocal accepting_states

            current_state = start_state
            i = 0

            while i < len(substr):
                if i < len(substr) - 1 and substr[i + 1] == '*':
                    new_state = 'q' + str(len(states) + 1)
                    add_transition(current_state, new_state, substr[i])
                    add_transition(new_state, new_state, '')
                    current_state = new_state
                    i += 1
                elif i < len(substr) - 1 and substr[i + 1] == '+':
                    new_state = 'q' + str(len(states) + 1)
                    add_transition(current_state, new_state, substr[i])
                    add_transition(new_state, new_state, substr[i])
                    current_state = new_state
                    i += 1
                elif substr[i] == '?':
                    new_state = 'q' + str(len(states) + 1)
                    add_transition(current_state, new_state, '')
                    current_state = new_state
                elif substr[i] == '|':
                    accepting_states.add(current_state)
                    current_state = start_state
                elif substr[i] == '(':
                    group_end = substr.find(')', i + 1)
                    if group_end != -1:
                        group_substr = substr[i + 1:group_end]
                        group_start_state = current_state
                        parse_regex(group_substr, group_start_state)
                        i = group_end
                else:
                    new_state = 'q' + str(len(states) + 1)
                    add_transition(current_state, new_state, substr[i])
                    current_state = new_state
                i += 1

            accepting_states.add(current_state)

        parse_regex(regex, initial_state)

        return Automata(states, alphabet, transitions, initial_state, accepting_states)


# Ejemplo de uso
regex = input("Ingrese la expresión regular: ")
automaton = ControladorExpresion.build_automaton_from_regex(regex)
print("Estados del autómata:", automaton.states)
automaton.draw()