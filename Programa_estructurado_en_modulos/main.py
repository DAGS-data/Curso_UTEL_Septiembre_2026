
import conversion as con
from impuestos import calcular_iva, total_con_iva


print("""
**********************************************************************
**********************************************************************
+      CALCULADORA DE IMPUESTOS Y CONVERSION DE MONEDA               +                              
+                                                                    +
+      

1. Calcular impuesto
2. Calcular total con impuesto
3. Convertir moneda
4. Salir
**********************************************************************
**********************************************************************

""")

opc = 0
while opc != 4:
    opc = input("Ingrese la opción deseada (1, 2, 3 o 4): ")

    if opc == "1":
        monto = float(input("Ingresa el monto del producto: "))
        iva = calcular_iva(monto)
        print("El IVA del producto es: ", iva)

    elif opc == "2":
        monto = float(input("Ingresa el monto del producto: "))
        total = total_con_iva(monto)
        print("El total con IVA incluido es: ", total)
    elif opc == "3":
        monto = float(input("Ingresa el monto en MXN: "))
        cambio = con.mxn_a_usd(monto)
        print("El monto en USD es: ", cambio)
    elif opc == "4":
        print("Saliendo del programa...")
        break
    else:
        print("Opción no válida. Por favor, ingrese 1, 2, 3 o 4.")