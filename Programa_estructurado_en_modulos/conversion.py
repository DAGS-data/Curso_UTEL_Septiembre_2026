

def mxn_a_usd(cantidad_mxn: float, tipo_cambio_: float = 18.0) -> float:
    if cantidad_mxn < 0:
        raise ValueError("La cantidad en MXN no puede ser negativa")
    else:
        return cantidad_mxn / tipo_cambio_  # Conversión de MXN a USD


if __name__ == "__main__":
    cantidad_mxn = float(input("Ingrese la cantidad en MXN: "))
    tipo_cambio = float(input("Ingrese el tipo de cambio (MXN a USD): "))
    cantidad_usd = mxn_a_usd(cantidad_mxn, tipo_cambio)
    print(f"{cantidad_mxn} MXN son equivalentes a {cantidad_usd:.2f} USD")