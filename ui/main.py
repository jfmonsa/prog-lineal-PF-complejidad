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
# Función para generar archivo .dzn
def generar_archivo_dzn(nombre_archivo, N, num_ciudades, ciudad_x, ciudad_y):
    with open(nombre_archivo, "w") as f:
        f.write(f"N = {N};\n")
        f.write(f"num_ciudades = {num_ciudades};\n")
        f.write(f"ciudad_x = [{', '.join(map(str, ciudad_x))}];\n")
        f.write(f"ciudad_y = [{', '.join(map(str, ciudad_y))}];\n")
        f.write("radius_concierto = 1;\n")

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

        # Generar archivo .dzn
        generar_archivo_dzn("entrada_generada.dzn", N, num_ciudades, ciudad_x, ciudad_y)

        # Mostrar el contenido del archivo .mzn
        with open("prog-lineal-model/model.mzn", "r") as f:
            mzn_content = f.read()
        output_text.insert(tk.END, "===== Modelo MiniZinc (.mzn) =====\n")
        output_text.insert(tk.END, mzn_content + "\n")

        # Mostrar el contenido del archivo .dzn
        with open("entrada_generada.dzn", "r") as f:
            dzn_content = f.read()
        output_text.insert(tk.END, "===== Datos (.dzn) =====\n")
        output_text.insert(tk.END, dzn_content + "\n")

        # Crear y resolver nueva instancia
        instancia = Instance(solver, pl_model)
        instancia["N"] = N
        instancia["num_ciudades"] = num_ciudades
        instancia["ciudad_x"] = ciudad_x
        instancia["ciudad_y"] = ciudad_y
        instancia["radius_concierto"] = 1  # Valor por defecto, se puede ajustar

        result = instancia.solve()
        output_text.insert(tk.END, "===== Resultado MiniZinc =====\n")
        output_text.insert(tk.END, f"{result}\n")
        output_text.insert(tk.END, "Archivo 'entrada_generada.dzn' creado con éxito.\n")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Botón para ejecutar
ejecutar_btn = tk.Button(root, text="Ejecutar Modelo", command=ejecutar_modelo)
ejecutar_btn.pack(pady=10)

# Iniciar la app
tk.mainloop()
