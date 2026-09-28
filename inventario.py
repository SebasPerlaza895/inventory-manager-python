import json
import csv
import os

CARPETA = os.path.dirname(os.path.abspath(__file__))
ARCHIVO = os.path.join(CARPETA, "inventario.json")
REPORTE = os.path.join(CARPETA, "reporte.csv")


class DatoInvalidoError(Exception):
    pass


def cargar():
    if not os.path.exists(ARCHIVO):
        return []

    with open(ARCHIVO, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar(data):
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(data, archivo, indent=4, ensure_ascii=False)


def registrar():
    nombre = input("Producto: ")

    try:

        if nombre.strip() == "":
            raise DatoInvalidoError("El nombre del producto no puede estar vacío.")

        cantidad = int(input("Cantidad: "))
        precio = float(input("Precio: "))

        if cantidad < 0:
            raise DatoInvalidoError("La cantidad no puede ser negativa.")
        if precio <= 0:
            raise DatoInvalidoError("El precio debe ser mayor que cero.")

        data = cargar()

        data.append({
            "nombre": nombre.strip(),
            "cantidad": cantidad,
            "precio": precio
        })

        guardar(data)

        print("Producto registrado correctamente.")

    except ValueError:
        print("Error: cantidad y precio deben ser numéricos.")
    except DatoInvalidoError as error:
        print("Error:", error)


def listar():
    data = cargar()

    if len(data) == 0:
        print("No hay productos registrados.")
        return

    print("\n--- INVENTARIO ---")

    for p in data:
        print(p["nombre"], "-", p["cantidad"], "-", p["precio"])


def analizar():
    data = cargar()

    if len(data) == 0:
        print("No hay datos para analizar.")
        return

    total = 0
    mayor = 0
    producto_mayor = ""

    for p in data:
        total += p["cantidad"] * p["precio"]

        if p["precio"] > mayor:
            mayor = p["precio"]
            producto_mayor = p["nombre"]

    print("\n--- ANÁLISIS ---")
    print(f"Valor total del inventario: ${total:,.0f}")
    print(f"Producto más costoso: {producto_mayor} (${mayor:,.0f})")


def exportar():
    data = cargar()

    if len(data) == 0:
        print("No hay datos para exportar.")
        return

    with open(REPORTE, "w", newline="", encoding="utf-8") as archivo:
        writer = csv.writer(archivo)

        writer.writerow(["nombre", "cantidad", "precio"])

        for p in data:
            writer.writerow([p["nombre"], p["cantidad"], p["precio"]])

    print("Reporte CSV generado correctamente.")


opcion = ""

while opcion != "5":
    print("\n===== SISTEMA DE INVENTARIO =====")
    print("1. Registrar producto")
    print("2. Listar productos")
    print("3. Analizar inventario")
    print("4. Exportar a CSV")
    print("5. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        registrar()
    elif opcion == "2":
        listar()
    elif opcion == "3":
        analizar()
    elif opcion == "4":
        exportar()
    elif opcion == "5":
        print("Saliendo del sistema...")
    else:
        print("Opción inválida.")