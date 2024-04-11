import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from controladores.controladorExpresion import ControladorExpresion

class AutomataGUI:
    def __init__(self, master):
        self.master = master
        self.master.title('Visualizador de Autómatas')
        self.master.geometry("1920x1080")

        self.label = tk.Label(master, text="Ingrese la expresión regular:")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.generate_button = tk.Button(
            master, text="Generar y Mostrar Autómata", command=self.generate_automaton)
        self.generate_button.pack()

        self.select_button = tk.Button(
            master, text="Seleccionar Autómata", command=self.seleccionar_automata)
        self.select_button.pack()

        self.image_label = tk.Label(master)
        self.image_label.pack()

        self.generated_images = []
        self.register_file = "automata_register.txt"
        self.read_register()

    def generate_automaton(self):
        regex = self.entry.get()
        if regex:
            try:
                automaton = ControladorExpresion.build_automaton_from_regex(regex)
                image_path = automaton.draw()
                self.generated_images.append(image_path)
                self.display_image(image_path)
                self.write_register()
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al generar el autómata: {str(e)}")
        else:
            messagebox.showwarning("Advertencia", "Por favor, ingrese una expresión regular.")

    def display_image(self, image_path):
        try:
            image = Image.open(image_path)
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen del autómata: {str(e)}")

    def seleccionar_automata(self):
        selection_window = tk.Toplevel(self.master)
        selection_window.geometry("800x600")
        selection_window.title("Seleccione un Autómata")
        listbox = tk.Listbox(selection_window)
        listbox = tk.Listbox(selection_window, width=50, height=20)
        listbox.pack()

        for idx, img_path in enumerate(self.generated_images):
            listbox.insert(tk.END, f"{idx + 1}. {img_path}")

        def on_select(event):
            if listbox.curselection():
                selected_index = listbox.curselection()[0]
                selected_image_path = self.generated_images[selected_index]
                self.display_image(selected_image_path)
                selection_window.destroy()

        listbox.bind('<<ListboxSelect>>', on_select)

    def read_register(self):
        try:
            with open(self.register_file, "r") as file:
                for line in file:
                    self.generated_images.append(line.strip())
        except FileNotFoundError:
            pass

    def write_register(self):
        with open(self.register_file, "w") as file:
            for img_path in self.generated_images:
                file.write(f"{img_path}\n")

if __name__ == "__main__":
    root = tk.Tk()
    my_gui = AutomataGUI(root)
    root.mainloop()