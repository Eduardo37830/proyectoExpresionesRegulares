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
            last_state_in_group = None  # Mantenemos el último estado del grupo

            def find_closing_parenthesis(substr, start_index):
                count = 0
                for i in range(start_index, len(substr)):
                    if substr[i] == '(':
                        count += 1
                    elif substr[i] == ')':
                        count -= 1
                        if count == 0:
                            return i
                return -1

            i = 0

            while i < len(substr):
                if i < len(substr) - 1 and substr[i + 1] == '*':
                    new_state = 'q' + str(len(states) + 1)
                    add_transition(current_state, current_state, substr[i])
                    i += 1
                elif i < len(substr) - 1 and substr[i + 1] == "+":
                    new_state = 'q' + str(len(states) + 1)
                    add_transition(current_state, new_state, substr[i])
                    add_transition(new_state, new_state, substr[i])
                    current_state = new_state
                    i += 1
                elif i < len(substr) - 1 and substr[i + 1] == '?':
                    new_state = 'q' + str(len(states) + 1)
                    accepting_states.add(current_state)
                    add_transition(current_state, new_state, substr[i])
                    current_state = new_state
                    i += 1  # Incrementamos i para saltar el operador '?'

                elif substr[i] == '|':
                    accepting_states.add(current_state)
                    current_state = start_state
                elif substr[i] == '(':

                    group_end = find_closing_parenthesis(substr, i)
                    if group_end != -1:
                        group_substr = substr[i + 1:group_end]
                        group_start_state = current_state

                        last_state_in_group = parse_regex(group_substr, group_start_state)
                        i = group_end
                        current_state = last_state_in_group  # Volvemos al último estado del grupo

                        # Si el próximo carácter después del grupo es '*', creamos una transición de vuelta al primer estado del grupo
                        if i < len(substr) - 1 and substr[i + 1] == '*':
                            add_transition(last_state_in_group, group_start_state, '')
                            accepting_states.add(group_start_state)
                        if i < len(substr) - 1 and substr[i + 1] == '+':
                            add_transition(last_state_in_group, last_state_in_group, substr[i - 2])
                            accepting_states.add(last_state_in_group)
                        elif substr[i] == '|':
                            accepting_states.add(current_state)
                            current_state = group_start_state
                        i += 1
                    elif substr[i] == ')':
                        break

                else:
                    new_state = 'q' + str(len(states) + 1)
                    add_transition(current_state, new_state, substr[i])
                    current_state = new_state
                i += 1
            accepting_states.add(current_state)
            # Devolvemos el último estado del grupo para referencia
            return last_state_in_group if last_state_in_group else current_state

        parse_regex(regex, initial_state)

        # Marcar el último estado como de aceptación fuera del grupo

        return Automata(states, alphabet, transitions, initial_state, accepting_states)


"""# Ejemplo de uso
regex = input("Ingrese la expresión regular: ")
automaton = ControladorExpresion.build_automaton_from_regex(regex)
print("Estados del autómata:", automaton.states)
automaton.draw()"""