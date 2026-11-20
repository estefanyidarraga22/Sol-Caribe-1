import os

from business_logic import CadenaHotelera, Hotel


def limpiar_consola() -> None:
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def mostrar_menu() -> None:
    print("========== CADENA SOL CARIBE ==========")
    print("1. Crear un hotel")
    print("7. Salir")


def pedir_hotel(cadena: CadenaHotelera) -> Hotel | None:
    nombre = input("Nombre del hotel: ")
    hotel = cadena.buscar_hotel(nombre)
    if hotel is None:
        print("No hay un hotel con ese nombre.")
    return hotel


def opcion_crear_hotel(cadena: CadenaHotelera) -> None:
    nombre = input("Nombre del hotel: ")
    habitaciones = input("Habitaciones habilitadas: ")
    anio = input("Año de inicio del registro: ")
    mes = input("Mes de inicio: ")
    dia = input("Día de inicio: ")
    mensaje = cadena.crear_hotel(nombre, habitaciones, anio, mes, dia)
    if mensaje == "":
        print(f"Se creó el hotel {nombre.strip()}, sin días registrados.")
    else:
        print(mensaje)


def opcion_salir() -> None:
    print("Fin del programa.")


def main() -> None:
    cadena = CadenaHotelera()
    salir = False
    while not salir:
        limpiar_consola()
        mostrar_menu()
        opcion = input("Elija una opción: ").strip()
        if opcion == "1":
            opcion_crear_hotel(cadena)
        elif opcion == "7":
            opcion_salir()
            salir = True
        else:
            print("La opción no es válida.")
        if not salir:
            input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    main()