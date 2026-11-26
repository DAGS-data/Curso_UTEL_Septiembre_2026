


def calcular_iva(monto:float,tasa:float=0.16)-> float:
    if monto<0:
        raise ValueError("El monto no puede ser negativo")
    else:
        return monto * tasa

def total_con_iva(monto:float,tasa:float=0.16)-> float:
    if monto<0:
        raise ValueError("El monto no puede ser negativo")
    else:
        return monto+calcular_iva(monto,tasa) #Total con IVA incluido
    
    