from modelos.expresionRegular import ModeloExpresionesRegulares

modelo = ModeloExpresionesRegulares()
modelo.generar_automata("(a)*(a+b)(b)*")
modelo.mostrar_automata()
