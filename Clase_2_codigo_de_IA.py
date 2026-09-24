import tkinter as tk
from tkinter import messagebox

def validar_y_enviar():
    nombre = entrada_nombre.get().strip()
    edad = entrada_edad.get().strip()
    ciudad = entrada_ciudad.get().strip()
    calificacion = entrada_calificacion.get().strip().replace(",", ".")
    comentarios = area_comentarios.get("1.0", "end").strip()

    if not nombre or not edad or not ciudad or not calificacion or not comentarios:
        messagebox.showwarning("Formulario incompleto", "Por favor, completa todos los campos.")
        return

    try:
        edad_valor = int(edad)
        calificacion_valor = float(calificacion)
    except ValueError:
        messagebox.showerror(
            "Datos inválidos",
            "La edad debe ser un número entero y la calificación debe ser un número."
        )
        return

    resultado = (
        "Su review es la siguiente:\n"
        f"Nombre: {nombre}\n"
        f"Edad: {edad_valor}\n"
        f"Ciudad: {ciudad}\n"
        f"Calificación de la ciudad: {calificacion_valor}\n"
        f"Comentarios: {comentarios}"
    )

    # Mostrar el resultado en la pantalla
    texto_resultado.config(text=resultado)

    # También mostrarlo en un mensaje emergente
    messagebox.showinfo("Review enviada", resultado)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Formulario de ciudad")
ventana.geometry("500x700")
ventana.configure(bg="#f2f2f2")
ventana.resizable(False, False)

# Título
titulo = tk.Label(
    ventana,
    text="Hola, bienvenido a mi primer formulario en Python",
    font=("Arial", 16, "bold"),
    bg="#f2f2f2",
    fg="#1f1f1f"
)
titulo.pack(pady=(20, 10))

# Frame principal
frame = tk.Frame(ventana, bg="#f2f2f2")
frame.pack(padx=20, pady=10, fill="both", expand=True)

# Nombre
tk.Label(frame, text="Nombre completo:", bg="#f2f2f2", font=("Arial", 11)).pack(anchor="w", pady=(10, 2))
entrada_nombre = tk.Entry(frame, width=50, font=("Arial", 11))
entrada_nombre.pack(fill="x", pady=(0, 8))

# Edad
tk.Label(frame, text="Edad:", bg="#f2f2f2", font=("Arial", 11)).pack(anchor="w", pady=(10, 2))
entrada_edad = tk.Entry(frame, width=50, font=("Arial", 11))
entrada_edad.pack(fill="x", pady=(0, 8))

# Ciudad
tk.Label(frame, text="Ciudad:", bg="#f2f2f2", font=("Arial", 11)).pack(anchor="w", pady=(10, 2))
entrada_ciudad = tk.Entry(frame, width=50, font=("Arial", 11))
entrada_ciudad.pack(fill="x", pady=(0, 8))

# Calificación
tk.Label(frame, text="Calificación de la ciudad:", bg="#f2f2f2", font=("Arial", 11)).pack(anchor="w", pady=(10, 2))
entrada_calificacion = tk.Entry(frame, width=50, font=("Arial", 11))
entrada_calificacion.pack(fill="x", pady=(0, 8))

# Comentarios
tk.Label(frame, text="Comentarios:", bg="#f2f2f2", font=("Arial", 11)).pack(anchor="w", pady=(10, 2))
area_comentarios = tk.Text(frame, height=6, width=50, font=("Arial", 11))
area_comentarios.pack(fill="x", pady=(0, 10))

# Botón enviar
boton_enviar = tk.Button(
    frame,
    text="Enviar formulario",
    command=validar_y_enviar,
    width=20,
    height=2,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 11, "bold")
)
boton_enviar.pack(pady=(10, 10))

# Resultado
texto_resultado = tk.Label(
    frame,
    text="",
    justify="left",
    anchor="w",
    bg="#f2f2f2",
    fg="#222222",
    font=("Arial", 10),
    wraplength=430
)
texto_resultado.pack(fill="x", pady=(10, 0))

ventana.mainloop()