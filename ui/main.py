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

        # Crear y resolver nueva instancia
        instancia = Instance(solver, pl_model)
        instancia["N"] = N
        instancia["num_ciudades"] = num_ciudades
        instancia["ciudad_x"] = ciudad_x
        instancia["ciudad_y"] = ciudad_y
        instancia["radius_concierto"] = 1  # Valor por defecto, se puede ajustar

        result = instancia.solve()
        mznGeneratedCodeTemplate = f"""
        % ---- Params from .dzn -----
        % ---- Params from .dzn -----
        int: N = {N}; % Tamaño del plano NxN
        int: num_ciudades =  {num_ciudades}; % Cantidad de ciudades
        int: radius_concierto = 1; % Radio mínimo de distancia al concierto
        % Arrays for the locations (x,y) of each city
        array[1..num_ciudades] of int: ciudad_x = [{', '.join(map(str, ciudad_x))}];
        array[1..num_ciudades] of int: ciudad_y = [{', '.join(map(str, ciudad_y))}];

        % name the range [1 , num_ciudades] as CIUDADES to iterate easily over the cities
        set of int: CIUDADES = 1..num_ciudades;

        % ---- Variables de decisión ---
        var 0..N-1: x_concierto;
        var 0..N-1: y_concierto;

        % ---- Aux Variables -----
        % Arrays to hold the absolute distances in X and Y
        % dx[i]: Distancia absoluta en X entre el concierto y la ciudad i
        % dy[i]: Distancia absoluta en Y entre el concierto y la ciudad i
        % NOTE: range bound 0..2*N explained in the Report
        array[CIUDADES] of var 0..2*N: dx;
        array[CIUDADES] of var 0..2*N: dy;

        % ----- Constraints -----
        % used to fill the absolute distance arrays dx and dy
        % For each city i, the distance in X and Y is defined as:
        % |x_concierto - ciudad_x[i]| == dx[i]
        % |y_concierto - ciudad_y[i]| == dy[i]
        % restricción redudante
        constraint forall(i in CIUDADES)(
        dx[i] = abs(x_concierto - ciudad_x[i]) /\\
        dy[i] = abs(y_concierto - ciudad_y[i])
        );

        constraint forall(i in CIUDADES)(
        dx[i] + dy[i] > radius_concierto
        );

        constraint forall(i in CIUDADES)(
        % A city cannot be at the same location as the concert
        (x_concierto != ciudad_x[i]) /\\ (y_concierto != ciudad_y[i])
        );

        % ---- Objective Function -----
        % distancia total entre el concierto y todas las ciudades
        % suma de las distancias manhattan desde el concierto a cada ciudad, esto es justo lo que el problema pide minimizar.
        var int: total_distancia = sum(i in CIUDADES)(dx[i] + dy[i]);
        solve minimize total_distancia;

      
        output [
        "Concierto en: (", show(x_concierto), ", ", show(y_concierto), ")\\n",
        "Distancia total: ", show(total_distancia), "\\n\\n",
        ];
        """

        output_text.insert(tk.END, f"{mznGeneratedCodeTemplate}\n")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Botón para ejecutar
ejecutar_btn = tk.Button(root, text="Ejecutar Modelo", command=ejecutar_modelo)
ejecutar_btn.pack(pady=10)

# Iniciar la app
tk.mainloop()
