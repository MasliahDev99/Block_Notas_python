#!/usr/bin/env python

import tkinter as tk
from tkinter import messagebox, filedialog
import sys
import os
import subprocess

class SimpleTextEditor:

    def __init__(self, root):
        self.root = root
        self.text_area = tk.Text(self.root, font=("Arial", 12))
        self.text_area.pack(fill=tk.BOTH, expand=1)
        self.current_open_file = ''

    def quit_confirm(self):
        if messagebox.askokcancel("Salir", "Está seguro que desea salir?"):
            self.root.destroy()

    def open_file(self):
        file_name = filedialog.askopenfilename()  # Abro el gestor de archivos
        if file_name:  # Si tiene contenido
            self.text_area.delete("1.0", tk.END)  # Limpio el texto anterior
            with open(file_name, 'r') as file:  # Abro el archivo con lectura
                self.text_area.insert("1.0", file.read())  # Y lo muestro
            self.current_open_file = file_name  # Actualizo el archivo actual

    def save_as_file(self):
        self.current_open_file = filedialog.asksaveasfilename()

    def new_file(self):
        self.text_area.delete("1.0", tk.END)
        self.current_open_file = ''

    def save_file(self):
        if not self.current_open_file:
            new_file_path = filedialog.asksaveasfilename()
            if new_file_path:
                self.current_open_file = new_file_path
            else:
                return
        with open(self.current_open_file, 'w') as file:
            file.write(self.text_area.get("1.0", tk.END))

    def tipo_archivo(self):
        archivo, extension = os.path.splitext(self.current_open_file)
        if extension == '.py':
            self.compile_command = ("python3", self.current_open_file)
        elif extension == '.c':
            exec_file = archivo
            self.compile_command = ("gcc", self.current_open_file, '-o', exec_file)
        elif extension == '.cpp':
            exec_file = archivo
            self.compile_command = ("g++", self.current_open_file, '-o', exec_file)
        elif extension == '' or extension == '.txt':
            self.compile_command = ("cat", self.current_open_file)
        else:
            messagebox.showinfo("Importante", f"\n[!] Error: el tipo de archivo '{extension}' no es compilable")

        self.compilar_archivo(*self.compile_command)

    def compilar_archivo(self, command, file, output_file=None):
        try:
            if command in ['gcc', 'g++']:
                subprocess.run([command, file, '-o', output_file], check=True)
                print("Compilación exitosa")
                subprocess.run(['./' + output_file], check=True)
                print("Ejecución exitosa")
            else:
                result = subprocess.run([command, file], check=True, text=True, capture_output=True)
                print("Salida del comando: ", result.stdout)
        except subprocess.CalledProcessError as er:
            print(f"\n[!]Error al compilar {er}")


root = tk.Tk()
root.title("Block de Notas")
root.geometry("800x600")

# Texto
editor = SimpleTextEditor(root)

# Menú de opciones
barra_menu = tk.Menu(root)
root.config(menu=barra_menu)

menu1 = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Archivo", menu=menu1)
menu1.add_command(label="Nuevo archivo", command=editor.new_file)
menu1.add_command(label="Abrir archivo", command=editor.open_file)
menu1.add_command(label="Guardar", command=editor.save_file)
menu1.add_command(label="Guardar como", command=editor.save_as_file)
menu1.add_command(label="Salir", command=editor.quit_confirm)

menu2 = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Editar", menu=menu2)
menu2.add_command(label="Formato")

menu3 = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Extras", menu=menu3)
menu3.add_command(label="Compilar", command=editor.tipo_archivo)

root.mainloop()

