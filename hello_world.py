#!/usr/bin/env python3
"""Hello World llamativo: banner ASCII + colores + efecto de escritura.
Funciona sin dependencias; si `pyfiglet` está instalado lo usará para un banner aún más grande.
"""
import sys
import time


def get_banner(text="Hello, World!"):
    try:
        from pyfiglet import Figlet
        fig = Figlet(font="slant")
        return fig.renderText(text)
    except Exception:
        return (
            "  _   _      _ _        __        __         _     _ _ \n"
            " | | | | ___| | | ___   \ \      / /__  _ __| | __| | |\n"
            " | |_| |/ _ \ | |/ _ \   \ \ /\ / / _ \| '__| |/ _` | |\n"
            " |  _  |  __/ | | (_) |   \ V  V / (_) | |  | | (_| |_|\n"
            " |_| |_|\___|_|_|\___/     \_/\_/ \___/|_|  |_|\__,_(_)\n"
        )


def rainbow_print(text, delay=0.02):
    colors = [31, 33, 32, 36, 34, 35]
    for i, ch in enumerate(text):
        color = colors[i % len(colors)]
        sys.stdout.write(f"\033[1;{color}m{ch}\033[0m")
        sys.stdout.flush()
        time.sleep(delay)
    print()


def typewriter(text, delay=0.06):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def main():
    banner = get_banner('Hello, World!')
    for i, line in enumerate(banner.splitlines()):
        color = 31 + (i % 6)
        print(f"\033[1;{color}m{line}\033[0m")
        time.sleep(0.03)

    time.sleep(0.15)
    msg = "Impresionado? Vamos con un pequeño efecto..."
    rainbow_print(msg, delay=0.01)

    time.sleep(0.2)
    typewriter("Mostrando 'Hello, World!' con efecto de máquina de escribir...\n", delay=0.03)

    # Un saludo final con colores
    final = "¡Hola Mundo! — Desde tu asistente creativo 🚀"
    rainbow_print(final, delay=0.01)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nInterrumpido por el usuario.')
