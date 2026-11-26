"""
Calculadora de Impuestos y Conversión de Moneda
Interfaz gráfica profesional construida con Tkinter / ttk.

Usa tus módulos existentes:
    ecom.conversion.mxn_a_usd(monto)
    ecom.impuestos.calcular_iva(monto)
    ecom.impuestos.total_con_iva(monto)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# --------------------------------------------------------------------------
# Lógica de negocio: se usan tus módulos. Si no se encuentran, se usa un
# respaldo para que la interfaz pueda probarse de forma independiente.
# --------------------------------------------------------------------------
try:
    import ecom.conversion as con
    from ecom.impuestos import calcular_iva, total_con_iva
    MODO = "Módulos ecom"
except ImportError:
    MODO = "Modo demostración (no se encontró el paquete ecom)"
    _TASA_IVA = 0.16
    _TIPO_CAMBIO = 18.50  # MXN por 1 USD

    def calcular_iva(monto):
        return monto * _TASA_IVA

    def total_con_iva(monto):
        return monto + calcular_iva(monto)

    class con:  # noqa: N801  (imita el módulo ecom.conversion)
        @staticmethod
        def mxn_a_usd(monto):
            return monto / _TIPO_CAMBIO


# --------------------------------------------------------------------------
# Paleta y tipografía
# --------------------------------------------------------------------------
COLORES = {
    "fondo": "#F3F5F9",
    "sidebar": "#1E2A3B",
    "sidebar_hover": "#2B3A50",
    "sidebar_activo": "#3B82F6",
    "texto_sidebar": "#C9D3E1",
    "tarjeta": "#FFFFFF",
    "borde": "#E2E7EF",
    "texto": "#1F2937",
    "texto_suave": "#6B7280",
    "primario": "#2563EB",
    "primario_hover": "#1D4ED8",
    "exito": "#059669",
    "error": "#DC2626",
}
FUENTE = "Segoe UI"


def formato_moneda(valor, divisa="MXN"):
    simbolo = "US$" if divisa == "USD" else "$"
    return f"{simbolo} {valor:,.2f} {divisa}"


# --------------------------------------------------------------------------
# Componentes
# --------------------------------------------------------------------------
class BotonMenu(tk.Label):
    """Botón de la barra lateral con estados hover / activo."""

    def __init__(self, master, texto, icono, comando):
        super().__init__(
            master, text=f"  {icono}   {texto}", anchor="w",
            bg=COLORES["sidebar"], fg=COLORES["texto_sidebar"],
            font=(FUENTE, 11), padx=18, pady=12, cursor="hand2",
        )
        self.comando = comando
        self.activo = False
        self.bind("<Button-1>", lambda e: self.comando())
        self.bind("<Enter>", lambda e: self._pintar(hover=True))
        self.bind("<Leave>", lambda e: self._pintar())

    def set_activo(self, activo):
        self.activo = activo
        self._pintar()

    def _pintar(self, hover=False):
        if self.activo:
            self.config(bg=COLORES["sidebar_activo"], fg="white")
        elif hover:
            self.config(bg=COLORES["sidebar_hover"], fg="white")
        else:
            self.config(bg=COLORES["sidebar"], fg=COLORES["texto_sidebar"])


class PanelCalculo(tk.Frame):
    """Panel genérico: título, campo de monto, botón y tarjeta de resultado."""

    def __init__(self, master, app, titulo, descripcion, etiqueta_entrada,
                 texto_boton, funcion, divisa_entrada, divisa_salida,
                 etiqueta_resultado, nombre_operacion):
        super().__init__(master, bg=COLORES["fondo"])
        self.app = app
        self.funcion = funcion
        self.divisa_entrada = divisa_entrada
        self.divisa_salida = divisa_salida
        self.nombre_operacion = nombre_operacion

        tk.Label(self, text=titulo, bg=COLORES["fondo"], fg=COLORES["texto"],
                 font=(FUENTE, 20, "bold")).pack(anchor="w")
        tk.Label(self, text=descripcion, bg=COLORES["fondo"],
                 fg=COLORES["texto_suave"], font=(FUENTE, 10)).pack(anchor="w", pady=(2, 18))

        # Tarjeta de entrada
        tarjeta = self._tarjeta(self)
        tarjeta.pack(fill="x")
        cuerpo = tk.Frame(tarjeta, bg=COLORES["tarjeta"])
        cuerpo.pack(fill="x", padx=24, pady=22)

        tk.Label(cuerpo, text=etiqueta_entrada, bg=COLORES["tarjeta"],
                 fg=COLORES["texto"], font=(FUENTE, 10, "bold")).pack(anchor="w")

        fila = tk.Frame(cuerpo, bg=COLORES["tarjeta"])
        fila.pack(fill="x", pady=(8, 4))

        caja = tk.Frame(fila, bg=COLORES["borde"], padx=1, pady=1)
        caja.pack(side="left", fill="x", expand=True)
        interior = tk.Frame(caja, bg="white")
        interior.pack(fill="both")
        tk.Label(interior, text="$", bg="white", fg=COLORES["texto_suave"],
                 font=(FUENTE, 13)).pack(side="left", padx=(12, 0))
        self.var_monto = tk.StringVar()
        self.entrada = tk.Entry(interior, textvariable=self.var_monto, bd=0,
                                font=(FUENTE, 14), fg=COLORES["texto"],
                                relief="flat", highlightthickness=0)
        self.entrada.pack(side="left", fill="x", expand=True, ipady=9, padx=6)
        tk.Label(interior, text=divisa_entrada, bg="white", fg=COLORES["texto_suave"],
                 font=(FUENTE, 10, "bold")).pack(side="right", padx=12)
        self.entrada.bind("<Return>", lambda e: self.calcular())
        self.entrada.bind("<FocusIn>", lambda e: caja.config(bg=COLORES["primario"]))
        self.entrada.bind("<FocusOut>", lambda e: caja.config(bg=COLORES["borde"]))

        self.boton = tk.Label(fila, text=texto_boton, bg=COLORES["primario"], fg="white",
                              font=(FUENTE, 11, "bold"), padx=22, pady=10, cursor="hand2")
        self.boton.pack(side="left", padx=(12, 0))
        self.boton.bind("<Button-1>", lambda e: self.calcular())
        self.boton.bind("<Enter>", lambda e: self.boton.config(bg=COLORES["primario_hover"]))
        self.boton.bind("<Leave>", lambda e: self.boton.config(bg=COLORES["primario"]))

        self.lbl_error = tk.Label(cuerpo, text="", bg=COLORES["tarjeta"],
                                  fg=COLORES["error"], font=(FUENTE, 9))
        self.lbl_error.pack(anchor="w")

        # Tarjeta de resultado
        resultado = self._tarjeta(self)
        resultado.pack(fill="x", pady=(16, 0))
        franja = tk.Frame(resultado, bg=COLORES["exito"], width=5)
        franja.pack(side="left", fill="y")
        cuerpo_r = tk.Frame(resultado, bg=COLORES["tarjeta"])
        cuerpo_r.pack(fill="x", padx=24, pady=20)
        tk.Label(cuerpo_r, text=etiqueta_resultado.upper(), bg=COLORES["tarjeta"],
                 fg=COLORES["texto_suave"], font=(FUENTE, 9, "bold")).pack(anchor="w")
        self.lbl_resultado = tk.Label(cuerpo_r, text="—", bg=COLORES["tarjeta"],
                                      fg=COLORES["texto"], font=(FUENTE, 26, "bold"))
        self.lbl_resultado.pack(anchor="w", pady=(4, 0))
        self.lbl_detalle = tk.Label(cuerpo_r, text="Ingresa un monto y presiona Enter",
                                    bg=COLORES["tarjeta"], fg=COLORES["texto_suave"],
                                    font=(FUENTE, 10))
        self.lbl_detalle.pack(anchor="w")

    @staticmethod
    def _tarjeta(master):
        return tk.Frame(master, bg=COLORES["tarjeta"],
                        highlightbackground=COLORES["borde"],
                        highlightcolor=COLORES["borde"], highlightthickness=1)

    def enfocar(self):
        self.entrada.focus_set()

    def calcular(self):
        texto = self.var_monto.get().replace(",", "").replace("$", "").strip()
        try:
            monto = float(texto)
            if monto < 0:
                raise ValueError
        except ValueError:
            self.lbl_error.config(text="⚠  Ingresa un número válido mayor o igual a 0.")
            self.lbl_resultado.config(text="—")
            self.app.set_estado("Entrada no válida", error=True)
            return

        self.lbl_error.config(text="")
        resultado = self.funcion(monto)
        self.lbl_resultado.config(text=formato_moneda(resultado, self.divisa_salida))
        self.lbl_detalle.config(
            text=f"Monto ingresado: {formato_moneda(monto, self.divisa_entrada)}")
        self.app.agregar_historial(self.nombre_operacion,
                                   formato_moneda(monto, self.divisa_entrada),
                                   formato_moneda(resultado, self.divisa_salida))
        self.app.set_estado(f"{self.nombre_operacion} calculado correctamente")


class PanelHistorial(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master, bg=COLORES["fondo"])
        self.app = app

        cab = tk.Frame(self, bg=COLORES["fondo"])
        cab.pack(fill="x")
        tk.Label(cab, text="Historial", bg=COLORES["fondo"], fg=COLORES["texto"],
                 font=(FUENTE, 20, "bold")).pack(side="left")
        limpiar = tk.Label(cab, text="Limpiar historial", bg=COLORES["fondo"],
                           fg=COLORES["error"], font=(FUENTE, 10, "underline"),
                           cursor="hand2")
        limpiar.pack(side="right")
        limpiar.bind("<Button-1>", lambda e: self.limpiar())
        tk.Label(self, text="Operaciones realizadas durante esta sesión",
                 bg=COLORES["fondo"], fg=COLORES["texto_suave"],
                 font=(FUENTE, 10)).pack(anchor="w", pady=(2, 18))

        marco = tk.Frame(self, bg=COLORES["tarjeta"], highlightcolor=COLORES["borde"],
                         highlightbackground=COLORES["borde"], highlightthickness=1)
        marco.pack(fill="both", expand=True)

        columnas = ("hora", "operacion", "entrada", "resultado")
        self.tabla = ttk.Treeview(marco, columns=columnas, show="headings",
                                  style="Historial.Treeview")
        for col, titulo, ancho in [("hora", "Hora", 80), ("operacion", "Operación", 160),
                                   ("entrada", "Monto", 170), ("resultado", "Resultado", 170)]:
            self.tabla.heading(col, text=titulo, anchor="w")
            self.tabla.column(col, width=ancho, anchor="w")
        barra = ttk.Scrollbar(marco, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=barra.set)
        self.tabla.pack(side="left", fill="both", expand=True, padx=(1, 0), pady=1)
        barra.pack(side="right", fill="y")

    def agregar(self, operacion, entrada, resultado):
        hora = datetime.now().strftime("%H:%M:%S")
        self.tabla.insert("", 0, values=(hora, operacion, entrada, resultado))

    def limpiar(self):
        if not self.tabla.get_children():
            return
        if messagebox.askyesno("Limpiar historial", "¿Deseas borrar todo el historial?"):
            self.tabla.delete(*self.tabla.get_children())
            self.app.set_estado("Historial limpiado")

    def enfocar(self):
        pass


# --------------------------------------------------------------------------
# Aplicación principal
# --------------------------------------------------------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora de Impuestos y Conversión de Moneda")
        self.geometry("980x620")
        self.minsize(860, 560)
        self.configure(bg=COLORES["fondo"])
        self._estilos()

        # Barra lateral
        sidebar = tk.Frame(self, bg=COLORES["sidebar"], width=240)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="💰 CalcuFiscal", bg=COLORES["sidebar"], fg="white",
                 font=(FUENTE, 16, "bold")).pack(anchor="w", padx=22, pady=(26, 0))
        tk.Label(sidebar, text="Impuestos y divisas", bg=COLORES["sidebar"],
                 fg=COLORES["texto_sidebar"], font=(FUENTE, 9)).pack(anchor="w", padx=24, pady=(0, 26))

        # Contenedor principal
        contenedor = tk.Frame(self, bg=COLORES["fondo"])
        contenedor.pack(side="left", fill="both", expand=True)
        self.area = tk.Frame(contenedor, bg=COLORES["fondo"])
        self.area.pack(fill="both", expand=True, padx=36, pady=30)

        self.estado = tk.Label(contenedor, text="Listo", anchor="w",
                               bg=COLORES["tarjeta"], fg=COLORES["texto_suave"],
                               font=(FUENTE, 9), padx=14, pady=6,
                               highlightbackground=COLORES["borde"], highlightthickness=1)
        self.estado.pack(fill="x", side="bottom")

        # Paneles (equivalentes a las opciones 1, 2 y 3 del menú original)
        self.paneles = {
            "iva": PanelCalculo(
                self.area, self, "Calcular impuesto",
                "Obtén el IVA correspondiente al monto de un producto.",
                "Monto del producto", "Calcular IVA", calcular_iva,
                "MXN", "MXN", "IVA del producto", "Cálculo de IVA"),
            "total": PanelCalculo(
                self.area, self, "Total con impuesto",
                "Calcula el precio final con el IVA incluido.",
                "Monto del producto", "Calcular total", total_con_iva,
                "MXN", "MXN", "Total con IVA incluido", "Total con IVA"),
            "conversion": PanelCalculo(
                self.area, self, "Convertir moneda",
                "Convierte pesos mexicanos (MXN) a dólares estadounidenses (USD).",
                "Monto en MXN", "Convertir", con.mxn_a_usd,
                "MXN", "USD", "Monto en USD", "Conversión MXN→USD"),
            "historial": PanelHistorial(self.area, self),
        }

        self.botones = {}
        for clave, texto, icono in [("iva", "Calcular impuesto", "🧾"),
                                    ("total", "Total con impuesto", "➕"),
                                    ("conversion", "Convertir moneda", "💱"),
                                    ("historial", "Historial", "🕘")]:
            b = BotonMenu(sidebar, texto, icono, lambda c=clave: self.mostrar(c))
            b.pack(fill="x", padx=12, pady=2)
            self.botones[clave] = b

        # Opción 4: Salir
        salir = BotonMenu(sidebar, "Salir", "⏻", self.salir)
        salir.pack(side="bottom", fill="x", padx=12, pady=(0, 8))
        tk.Label(sidebar, text=MODO, bg=COLORES["sidebar"], fg="#7B8BA3",
                 font=(FUENTE, 8), wraplength=190, justify="left", anchor="w").pack(
                     side="bottom", fill="x", padx=24, pady=(0, 10))

        # Atajos de teclado
        for i, clave in enumerate(["iva", "total", "conversion", "historial"], start=1):
            self.bind(f"<Control-Key-{i}>", lambda e, c=clave: self.mostrar(c))
        self.bind("<Escape>", lambda e: self.salir())
        self.protocol("WM_DELETE_WINDOW", self.salir)

        self.mostrar("iva")

    def _estilos(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure("Historial.Treeview", background="white", fieldbackground="white",
                         foreground=COLORES["texto"], rowheight=30, font=(FUENTE, 10),
                         borderwidth=0)
        estilo.configure("Historial.Treeview.Heading", background="#F8FAFC",
                         foreground=COLORES["texto_suave"], font=(FUENTE, 9, "bold"),
                         relief="flat", padding=(8, 8))
        estilo.map("Historial.Treeview", background=[("selected", "#DBEAFE")],
                   foreground=[("selected", COLORES["texto"])])

    def mostrar(self, clave):
        for panel in self.paneles.values():
            panel.pack_forget()
        self.paneles[clave].pack(fill="both", expand=True)
        self.paneles[clave].enfocar()
        for c, b in self.botones.items():
            b.set_activo(c == clave)

    def agregar_historial(self, operacion, entrada, resultado):
        self.paneles["historial"].agregar(operacion, entrada, resultado)

    def set_estado(self, texto, error=False):
        self.estado.config(text=texto, fg=COLORES["error"] if error else COLORES["texto_suave"])

    def salir(self):
        if messagebox.askokcancel("Salir", "¿Deseas salir del programa?"):
            self.destroy()


if __name__ == "__main__":
    App().mainloop()
