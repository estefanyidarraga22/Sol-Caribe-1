import os
from datetime import date, timedelta

from business_logic import CadenaHotelera, Hotel, validar_dias_a_simular


def limpiar_consola() -> None:
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def mostrar_menu() -> None:
    print("========== CADENA SOL CARIBE ==========")
    print("1. Crear un hotel")
    print("2. Registrar las habitaciones ocupadas del día siguiente")
    print("3. Simular días")
    print("4. Ver el informe de un hotel")
    print("5. Ver el hotel con el porcentaje de ocupación más alto y el más bajo")
    print("6. Cargar los hoteles y la ocupación desde archivos")
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


def opcion_registrar_dia(cadena: CadenaHotelera) -> None:
    hotel = pedir_hotel(cadena)
    if hotel is not None:
        fecha = hotel.fecha_siguiente()
        print(f"Día siguiente del registro: {fecha}")
        registrado = False
        while not registrado:
            try:
                cantidad = int(input(f"Habitaciones ocupadas del {fecha}: "))
                mensaje = hotel.validar_ocupadas(cantidad)
                if mensaje == "":
                    hotel.registrar_dia(cantidad)
                    registrado = True
                    print(f"Se registró el día {fecha}.")
                else:
                    print(mensaje)
            except ValueError:
                print("Las habitaciones ocupadas deben ser un número entero.")


def opcion_simular_dias(cadena: CadenaHotelera) -> None:
    hotel = pedir_hotel(cadena)
    if hotel is not None:
        seguir = True
        dias = 0
        minimo = 0
        maximo = 0

        try:
            dias = int(input("Número de días a simular: "))
            mensaje = validar_dias_a_simular(dias)
        except ValueError:
            mensaje = "El número de días debe ser un número entero."
        if mensaje != "":
            print(mensaje)
            seguir = False

        if seguir:
            try:
                minimo = int(input("Habitaciones ocupadas mínimas: "))
                mensaje = hotel.validar_ocupadas(minimo)
            except ValueError:
                mensaje = "Las habitaciones ocupadas deben ser un número entero."
            if mensaje != "":
                print(mensaje)
                seguir = False

        if seguir:
            try:
                maximo = int(input("Habitaciones ocupadas máximas: "))
                mensaje = hotel.validar_ocupadas(maximo)
            except ValueError:
                mensaje = "Las habitaciones ocupadas deben ser un número entero."
            if mensaje != "":
                print(mensaje)
                seguir = False

        if seguir:
            mensaje = hotel.simular_dias(dias, minimo, maximo)
            if mensaje == "":
                print(f"Se simularon {dias} día(s).")
                print(f"Habitaciones ocupadas simuladas: {hotel.ultimos_dias(dias)}")
            else:
                print(mensaje)


def opcion_ver_informe(cadena: CadenaHotelera, hoy: date) -> None:
    hotel = pedir_hotel(cadena)
    if hotel is not None:
        print()
        print(f"Hotel: {hotel.nombre}")
        print(f"Habitaciones habilitadas: {hotel.habitaciones}")
        if hotel.dias_registrados() == 0:
            print("El hotel no tiene días registrados.")
        else:
            print(f"Días registrados: {hotel.dias_registrados()}")
            print(f"Noches vendidas: {hotel.noches_vendidas()}")
            print(f"Promedio de habitaciones ocupadas por día: {round(hotel.promedio(), 2)}")
            print(f"Porcentaje de ocupación: {round(hotel.porcentaje_ocupacion(), 2)} %")
            print(f"Desviación estándar: {round(hotel.desviacion_estandar(), 2)}")
            print(f"Día con más habitaciones ocupadas: {hotel.dia_mas_ocupado()}")
            print(f"Día con menos habitaciones ocupadas: {hotel.dia_menos_ocupado()}")

            niveles = hotel.contar_niveles()
            print("Días en cada nivel de ocupación:")
            print(f"  Crítica: {niveles['crítica']}")
            print(f"  Baja: {niveles['baja']}")
            print(f"  Media: {niveles['media']}")
            print(f"  Alta: {niveles['alta']}")

            dias_racha, inicio_racha = hotel.racha_critica_mas_larga()
            if dias_racha == 0:
                print("El hotel no tuvo ningún día en ocupación crítica.")
            else:
                print(f"Racha más larga en ocupación crítica: {dias_racha} día(s), desde el {inicio_racha}")

            print(f"Último día registrado: {hotel.ultimo_dia()}")
            faltan = hotel.dias_sin_registrar(hoy)
            if faltan == 0:
                print("El registro está al día.")
            else:
                ayer = hoy - timedelta(days=1)
                print(f"Días que faltan por registrar: {faltan}, del {hotel.fecha_siguiente()} al {ayer}")


def opcion_comparar_hoteles(cadena: CadenaHotelera) -> None:
    mayor = cadena.hotel_mas_ocupado()
    menor = cadena.hotel_menos_ocupado()
    if mayor is None or menor is None:
        print("Ningún hotel tiene días registrados.")
    else:
        print(f"Porcentaje de ocupación más alto: {mayor.nombre}, con {round(mayor.porcentaje_ocupacion(), 2)} %")
        print(f"Porcentaje de ocupación más bajo: {menor.nombre}, con {round(menor.porcentaje_ocupacion(), 2)} %")


def opcion_cargar_archivos(cadena: CadenaHotelera) -> None:
    if len(cadena.hoteles) > 0:
        print("La carga solo se hace con el programa sin hoteles.")
    else:
        hoteles_cargados = False
        ruta = input("Ruta del archivo de hoteles: ").strip()
        try:
            cargados, descartadas = cadena.cargar_hoteles(ruta)
            for mensaje in descartadas:
                print(mensaje)
            print(f"Hoteles cargados: {cargados}")
            hoteles_cargados = True
        except FileNotFoundError:
            print("El archivo no existe.")
        except (OSError, UnicodeDecodeError):
            # Decisión: por si la ruta es una carpeta o el archivo no está guardado en UTF-8.
            print("No se pudo leer el archivo.")

        if hoteles_cargados:
            ruta = input("Ruta del archivo de ocupación: ").strip()
            try:
                cargados, descartadas = cadena.cargar_ocupacion(ruta)
                for mensaje in descartadas:
                    print(mensaje)
                print(f"Días cargados: {cargados}")
            except FileNotFoundError:
                print("El archivo no existe. Los hoteles quedan cargados, sin días registrados.")
            except (OSError, UnicodeDecodeError):
                print("No se pudo leer el archivo. Los hoteles quedan cargados, sin días registrados.")


def opcion_salir(cadena: CadenaHotelera) -> None:
    if len(cadena.hoteles) > 0:
        respuesta = input("¿Desea guardar los datos antes de salir? (s/n): ").strip().lower()
        if respuesta == "s":
            try:
                cadena.guardar("hoteles_guardados.csv", "ocupacion_guardada.csv")
                print("Datos guardados en hoteles_guardados.csv y ocupacion_guardada.csv.")
                print("La próxima vez se pueden cargar con la opción 6.")
            except OSError:
                print("No se pudieron guardar los datos.")
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
        elif opcion == "2":
            opcion_registrar_dia(cadena)
        elif opcion == "3":
            opcion_simular_dias(cadena)
        elif opcion == "4":
            opcion_ver_informe(cadena, date.today())
        elif opcion == "5":
            opcion_comparar_hoteles(cadena)
        elif opcion == "6":
            opcion_cargar_archivos(cadena)
        elif opcion == "7":
            opcion_salir(cadena)
            salir = True
        else:
            print("La opción no es válida.")
        if not salir:
            input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    main()