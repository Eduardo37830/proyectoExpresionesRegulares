import re


class ModeloExpresionesRegulares:
    def __init__(self):
        self.alfabeto = set()
        self.estados = set()
        self.estado_inicial = None
        self.estados_aceptacion = set()
        self.transiciones = {}

    def generar_automata(self, expresion_regular):
        self.alfabeto = set(re.findall(r'[a-zA-Z]', expresion_regular))  # Obtener el alfabeto de la expresión regular
        self.estados = set()  # Los estados se generarán dinámicamente durante el proceso
        self.estado_inicial = 'q0'
        self.estados_aceptacion = set()
        self.transiciones = {}

        # Iniciar el proceso de conversión de expresión regular a autómata
        # Aquí debes implementar un algoritmo para convertir la expresión regular en un autómata
        # Puedes utilizar métodos como Thompson's Construction o convertir la expresión en un árbol de sintaxis y luego en un autómata

        # Ejemplo: creación de un autómata de ejemplo
        self.estados.add(self.estado_inicial)
        estado_final = 'q1'
        self.estados.add(estado_final)
        self.estados_aceptacion.add(estado_final)
        self.transiciones[self.estado_inicial] = {'ε': [estado_final]}  # Transición epsilon al estado final

    def mostrar_automata(self):
        print("Alfabeto:", self.alfabeto)
        print("Estados:", self.estados)
        print("Estado inicial:", self.estado_inicial)
        print("Estados de aceptación:", self.estados_aceptacion)
        print("Transiciones:")
        for estado, transiciones in self.transiciones.items():
            for simbolo, estados_siguientes in transiciones.items():
                for estado_siguiente in estados_siguientes:
                    print(f"{estado} --({simbolo})--> {estado_siguiente}")


# Ejemplo de uso
modelo = ModeloExpresionesRegulares()
modelo.generar_automata("abc*")
modelo.mostrar_automata()
