from graphviz import Digraph

class Estado:
    def __init__(self, nombre, aceptacion=False):
        self.nombre = nombre
        self.aceptacion = aceptacion
        self.transiciones = {}

    def agregar_transicion(self, simbolo, estado_destino):
        if simbolo in self.transiciones:
            self.transiciones[simbolo].append(estado_destino)
        else:
            self.transiciones[simbolo] = [estado_destino]

class Automata:
    def __init__(self, estado_inicial, estado_final):
        self.estado_inicial = estado_inicial
        self.estado_final = estado_final

def construir_automata(expresion_regular):
    pila = []

    for caracter in expresion_regular:
        if caracter == '*':
            automata = pila.pop()
            estado_final = Estado("F", True)
            estado_inicial = Estado("I")
            estado_inicial.agregar_transicion('ε', automata.estado_inicial)
            estado_inicial.agregar_transicion('ε', estado_final)
            automata.estado_final.agregar_transicion('ε', automata.estado_inicial)
            automata.estado_final.agregar_transicion('ε', estado_final)
            pila.append(Automata(estado_inicial, estado_final))
        elif caracter == '|':
            automata2 = pila.pop()
            automata1 = pila.pop()
            estado_final = Estado("F", True)
            estado_inicial = Estado("I")
            estado_inicial.agregar_transicion('ε', automata1.estado_inicial)
            estado_inicial.agregar_transicion('ε', automata2.estado_inicial)
            automata1.estado_final.agregar_transicion('ε', estado_final)
            automata2.estado_final.agregar_transicion('ε', estado_final)
            pila.append(Automata(estado_inicial, estado_final))
        else:
            estado_final = Estado("F", True)
            estado_inicial = Estado("I")
            estado_inicial.agregar_transicion(caracter, estado_final)
            pila.append(Automata(estado_inicial, estado_final))

    return pila.pop()

def dibujar_automata(automata):
    dot = Digraph()

    estados_visitados = set()

    def dfs(estado):
        if estado.nombre not in estados_visitados:
            estados_visitados.add(estado.nombre)
            dot.node(estado.nombre, estado.nombre, shape='circle', style='bold' if estado.aceptacion else '')
            for simbolo, destinos in estado.transiciones.items():
                for destino in destinos:
                    dot.edge(estado.nombre, destino.nombre, label=simbolo)
                    dfs(destino)

    dfs(automata.estado_inicial)
    dot.render('automata', format='png', cleanup=True)

# Ejemplo de uso
expresion_regular = "a*b|c*|a"
automata = construir_automata(expresion_regular)
dibujar_automata(automata)
