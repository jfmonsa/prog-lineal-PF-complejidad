import tkinter as tk
from tkinter import messagebox
from minizinc import Instance, Model, Solver

# Cargar el solver y el modelo MiniZinc
solver = Solver.lookup("gecode")
pl_model = Model("prog-lineal-model/model.mzn")
instance = Instance(solver, pl_model)

# Crear la ventana principal
root = tk.Tk()
root.title("Generador de Modelo MiniZinc")
root.geometry("700x600")

# Etiqueta y TextArea para entrada
input_label = tk.Label(root, text="Datos de entrada:")
input_label.pack(pady=(10, 0))

input_text = tk.Text(root, height=15, width=80)
input_text.pack(pady=(0, 10))

# TextArea para salida
output_label = tk.Label(root, text="Resultados:")
output_label.pack()

output_text = tk.Text(root, height=15, width=80)
output_text.pack()

# Función para ejecutar el modelo MiniZinc
def ejecutar_modelo():
    output_text.delete(1.0, tk.END)
    try:
        datos = input_text.get("1.0", tk.END).strip().splitlines()
        if len(datos) < 3:
            messagebox.showerror("Error", "Debes ingresar al menos 3 líneas de datos.")
            return

        N = int(datos[0])
        num_ciudades = int(datos[1])
        nombres = []
        ciudad_x = []
        ciudad_y = []

        for linea in datos[2:2 + num_ciudades]:
            partes = linea.strip().split()
            if len(partes) != 3:
                messagebox.showerror("Error", f"Línea mal formada: {linea}")
                return
            nombre, x, y = partes
            nombres.append(nombre)
            ciudad_x.append(int(x))
            ciudad_y.append(int(y))

        # Crea una nueva instancia cada vez
        solver = Solver.lookup("gecode")
        pl_model = Model("prog-lineal-model/model.mzn")
        instancia = Instance(solver, pl_model)

        instancia["N"] = N
        instancia["num_ciudades"] = num_ciudades
        instancia["ciudad_x"] = ciudad_x
        instancia["ciudad_y"] = ciudad_y

        result = instancia.solve()

        output_text.insert(tk.END, f"{result}\n")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Botón para ejecutar
ejecutar_btn = tk.Button(root, text="Ejecutar Modelo", command=ejecutar_modelo)
ejecutar_btn.pack(pady=10)

# Iniciar la app
tk.mainloop()
