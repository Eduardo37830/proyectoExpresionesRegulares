import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk  # Importamos PIL para manejo de imágenes
from controladores.controladorExpresion import ControladorExpresion


class AutomataGUI:
    def __init__(self, master):
        self.master = master
        master.title('Visualizador de Autómatas')
        self.master.geometry("1920x1080")

        # Etiqueta de instrucción
        self.label = tk.Label(master, text="Ingrese la expresión regular:")
        self.label.pack()

        # Campo de entrada para la expresión regular
        self.entry = tk.Entry(master)
        self.entry.pack()

        # Botón para generar el autómata
        self.generate_button = tk.Button(master, text="Generar y Mostrar Autómata", command=self.generate_automaton)
        self.generate_button.pack()

        # Área de imagen (inicialmente vacía)
        self.image_label = tk.Label(master)
        self.image_label.pack()

    def generate_automaton(self):
        regex = self.entry.get()
        if regex:
            try:
                # Aquí llamarías a la función para generar el autómata y luego dibujarlo
                # Por ejemplo: automaton = ControladorExpresion.build_automaton_from_regex(regex)
                # automaton.draw()  # Asumiendo que esta función guarda una imagen llamada 'automata.png'
                automaton = ControladorExpresion.build_automaton_from_regex(regex)

                # Por simplicidad, asumiremos que la imagen se guarda como 'automata.png'
                image_path = automaton.draw()
                self.display_image(image_path)

            except Exception as e:
                messagebox.showerror("Error", "Ocurrió un error al generar el autómata: " + str(e))
        else:
            messagebox.showwarning("Advertencia", "Por favor, ingrese una expresión regular.")

    def display_image(self, image_path):
        # Carga y muestra la imagen del autómata
        try:
            image = Image.open(image_path) # Redimensionar si es necesario
            photo = ImageTk.PhotoImage(image)
            self.image_label.configure(image=photo)
            self.image_label.image = photo  # Mantener referencia
        except Exception as e:
            messagebox.showerror("Error", "No se pudo cargar la imagen del autómata: " + str(e))


if __name__ == "__main__":
    root = tk.Tk()
    my_gui = AutomataGUI(root)
    root.mainloop()
