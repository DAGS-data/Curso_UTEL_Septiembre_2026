import tkinter as tk 
from tkinter import messagebox

def validar():
    name = nombre.get().strip().upper()
    gen = genero.get().strip()
    phone = telefono.get().strip()
    date = int(fecha_nacimiento.get().strip())
    email = correo.get().strip()


    resultado = (
        "Su registro es el siguiente:\n"
        f"Nombre: {name}\n"
        f"Género: {gen}\n"
        f"Teléfono: {phone}\n"
        f"Fecha de nacimiento: {date}\n"
        f"Correo: {email}"
    )

    # Mostrar el resultado en la pantalla
    mensaje.config(text=resultado)

    # También mostrarlo en un mensaje emergente
    messagebox.showinfo("Registro enviado", resultado)



window = tk.Tk()
window.title("Registro de cuenta")
window.geometry("700x1300")
window.configure(bg="#1264E9")
window.resizable(True, True)

titulo = tk.Label(
    window, 
    text="Bienvenido a FreeMarket - Signup",
    font=("Arial", 25),
    bg="#1f1f1f",
    fg="white"
)

titulo.pack(pady=(20, 10))

frame = tk.Frame(window)
frame.pack(padx=20, pady=10, fill="both", expand=True)

#Nombre completo
tk.Label(frame, text="Introduzca su Nombre completo:", bg="#f2f2f2", font=("Arial", 11)).pack(anchor="w", pady=(10, 2))
nombre = tk.Entry(frame, width=50, font=("Arial", 18))
nombre.pack(pady=5)


#Genero
tk.Label(frame, text="Introduzca su Genero:", bg="#f2f2f2", font=("Arial", 11)).pack(anchor="w", pady=(10, 2))
genero = tk.Entry(frame, width=50, font=("Arial", 18))
genero.pack(pady=5)

#telefono
tk.Label(frame, text="Introduzca su telefono:", bg="#f2f2f2", font=("Arial", 11)).pack(anchor="w", pady=(10, 2))
telefono = tk.Entry(frame, width=50, font=("Arial", 18))
telefono.pack(pady=5)


#fecha de nacimiento
tk.Label(frame, text="Introduzca su fecha de nacimiento:", bg="#f2f2f2", font=("Arial", 11)).pack(anchor="w", pady=(10, 2))
fecha_nacimiento = tk.Entry(frame, width=50, font=("Arial", 18))
fecha_nacimiento.pack(pady=5)

#correo
tk.Label(frame, text="Introduzca su correo:", bg="#f2f2f2", font=("Arial", 11)).pack(anchor="w", pady=(10, 2))
correo = tk.Entry(frame, width=50, font=("Arial", 18))
correo.pack(pady=5)

#mensaje 
mensaje = tk.Label(frame, text="", bg="#f2f2f2", font=("Arial", 11))    
mensaje.pack(pady=5)

boton_de_carga = tk.Button(
    frame,
    text="Enviar",
    command=validar,
    width=20,
    height=2,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 20, "bold")
)
boton_de_carga.pack(pady=10)

window.mainloop()