import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from controladores.controladorExpresion import ControladorExpresion

class AutomataGUI:
    def __init__(self, master):
        self.master = master
        self.master.title('Visualizador de Autómatas')
        self.master.geometry("1920x1080")

        self.label1 = tk.Label(master, text="Ingrese la expresión regular para el primer autómata:")
        self.label1.pack()

        self.entry1 = tk.Entry(master)
        self.entry1.pack()

        self.generate_button1 = tk.Button(
            master, text="Generar y Mostrar Primer Autómata", command=lambda: self.generate_automaton(1))
        self.generate_button1.pack()

        self.select_button1 = tk.Button(
            master, text="Seleccionar Primer Autómata", command=lambda: self.seleccionar_automata(1))
        self.select_button1.pack()

        self.image_label1 = tk.Label(master)
        self.image_label1.pack()

        self.label2 = tk.Label(master, text="Ingrese la expresión regular para el segundo autómata:")
        self.label2.pack()

        self.entry2 = tk.Entry(master)
        self.entry2.pack()

        self.generate_button2 = tk.Button(
            master, text="Generar y Mostrar Segundo Autómata", command=lambda: self.generate_automaton(2))
        self.generate_button2.pack()

        self.select_button2 = tk.Button(
            master, text="Seleccionar Segundo Autómata", command=lambda: self.seleccionar_automata(2))
        self.select_button2.pack()

        self.image_label2 = tk.Label(master)
        self.image_label2.pack()

        self.intersection_button = tk.Button(
            master, text="Intersección", command=self.intersect_automata)
        self.intersection_button.pack()

        self.reverse_button1 = tk.Button(
            master, text="Inversión Primer Autómata", command=lambda: self.reverse_automaton(1))
        self.reverse_button1.pack()

        self.reverse_button2 = tk.Button(
            master, text="Inversión Segundo Autómata", command=lambda: self.reverse_automaton(2))
        self.reverse_button2.pack()

        self.image_label_result = tk.Label(master)
        self.image_label_result.pack()

        self.generated_data = []  # Almacenamos tuplas de (ruta_de_imagen, expresion_regular)
        self.register_file = "automata_register.txt"
        self.read_register()

    def generate_automaton(self, automaton_number):
        if automaton_number == 1:
            regex = self.entry1.get()
        else:
            regex = self.entry2.get()

        if regex:
            try:
                automaton = ControladorExpresion.build_automaton_from_regex(regex)
                image_path = automaton.draw()
                self.generated_data.append((image_path, regex))  # Guardar tupla
                self.display_image(image_path, automaton_number)
                self.write_register()
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al generar el autómata: {str(e)}")
        else:
            messagebox.showwarning("Advertencia", "Por favor, ingrese una expresión regular.")

    def display_image(self, image_path, automaton_number):
        try:
            image = Image.open(image_path)
            photo = ImageTk.PhotoImage(image)
            if automaton_number == 1:
                self.image_label1.config(image=photo)
                self.image_label1.image = photo
            elif automaton_number == 2:
                self.image_label2.config(image=photo)
                self.image_label2.image = photo
            else:
                self.image_label_result.config(image=photo)
                self.image_label_result.image = photo
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen del autómata: {str(e)}")

    def seleccionar_automata(self, automaton_number):
        selection_window = tk.Toplevel(self.master)
        selection_window.geometry("800x600")
        selection_window.title("Seleccione un Autómata")
        listbox = tk.Listbox(selection_window, width=70, height=70)
        listbox.pack()

        for idx, (img_path, _) in enumerate(self.generated_data):
            listbox.insert(tk.END, f"{idx + 1}. {img_path}")

        def on_select(event):
            if listbox.curselection():
                selected_index = listbox.curselection()[0]
                selected_image_path, selected_regex = self.generated_data[selected_index]
                self.display_image(selected_image_path, automaton_number)
                if automaton_number == 1:
                    self.entry1.delete(0, tk.END)
                    self.entry1.insert(0, selected_regex)
                else:
                    self.entry2.delete(0, tk.END)
                    self.entry2.insert(0, selected_regex)
                selection_window.destroy()

        listbox.bind('<<ListboxSelect>>', on_select)

    def read_register(self):
        try:
            with open(self.register_file, "r") as file:
                for line in file:
                    img_path, regex = line.strip().split(',', 1)
                    self.generated_data.append((img_path, regex))
        except FileNotFoundError:
            pass

    def write_register(self):
        with open(self.register_file, "w") as file:
            for img_path, regex in self.generated_data:
                file.write(f"{img_path},{regex}\n")

    def intersect_automata(self):
        try:
            regex1 = self.entry1.get()
            regex2 = self.entry2.get()
            if regex1 and regex2:
                automaton1 = ControladorExpresion.build_automaton_from_regex(regex1)
                automaton2 = ControladorExpresion.build_automaton_from_regex(regex2)
                result_automaton = automaton1.intersect(automaton2)
                image_path = result_automaton.draw()
                self.display_image(image_path, 'result')
            else:
                messagebox.showwarning("Advertencia", "Por favor, ingrese ambas expresiones regulares.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al realizar la intersección: {str(e)}")

    def reverse_automaton(self, automaton_number):
        try:
            if automaton_number == 1:
                regex = self.entry1.get()
            else:
                regex = self.entry2.get()

            if regex:
                automaton = ControladorExpresion.build_automaton_from_regex(regex)
                result_automaton = automaton.reverse()
                image_path = result_automaton.draw()
                self.display_image(image_path, 'result')
            else:
                messagebox.showwarning("Advertencia", "Por favor, ingrese una expresión regular.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al realizar el reverso: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    my_gui = AutomataGUI(root)
    root.mainloop()
