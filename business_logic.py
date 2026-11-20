import math
import random
from datetime import date, timedelta


def es_entero(texto: str) -> bool:
    resultado = True
    try:
        int(texto)
    except ValueError:
        resultado = False
    return resultado


def crear_fecha(anio: str, mes: str, dia: str) -> date | None:
    fecha = None
    try:
        fecha = date(int(anio), int(mes), int(dia))
    except ValueError:
        fecha = None
    except OverflowError:
        # Decisión: con un año gigante Python lanza OverflowError en vez de ValueError.
        fecha = None
    return fecha


def validar_dias_a_simular(dias: int) -> str:
    mensaje = ""
    if dias < 1:
        mensaje = "Se debe simular al menos un día."
    elif dias > 365:
        # Decisión: máximo 365 días por simulación para que el programa no se quede pegado.
        mensaje = "Se pueden simular máximo 365 días cada vez."
    return mensaje


class Hotel:
    def __init__(self, nombre: str, habitaciones: int, fecha_inicio: date) -> None:
        self.nombre = nombre
        self.habitaciones = habitaciones
        self.fecha_inicio = fecha_inicio
        self.ocupadas: list[int] = []

    def dias_registrados(self) -> int:
        return len(self.ocupadas)

    def fecha_del_dia(self, posicion: int) -> date:
        return self.fecha_inicio + timedelta(days=posicion)

    def fecha_siguiente(self) -> date:
        return self.fecha_del_dia(len(self.ocupadas))

    def ultimo_dia(self) -> date | None:
        ultimo = None
        # Decisión: si la lista está vacía no hay último día.
        if len(self.ocupadas) > 0:
            ultimo = self.fecha_del_dia(len(self.ocupadas) - 1)
        return ultimo

    def validar_ocupadas(self, cantidad: int) -> str:
        mensaje = ""
        if cantidad < 0 or cantidad > self.habitaciones:
            mensaje = f"Las habitaciones ocupadas de {self.nombre} van de 0 a {self.habitaciones}."
        return mensaje

    def registrar_dia(self, cantidad: int) -> None:
        self.ocupadas.append(cantidad)

    def simular_dias(self, dias: int, minimo: int, maximo: int) -> str:
        mensaje = ""
        if minimo > maximo:
            mensaje = "El mínimo no puede ser mayor que el máximo."
        else:
            for i in range(dias):
                self.ocupadas.append(random.randint(minimo, maximo))
        return mensaje

    def ultimos_dias(self, dias: int) -> list[int]:
        inicio = len(self.ocupadas) - dias
        # Decisión: si piden más días de los que hay, se devuelven todos los que hay.
        if inicio < 0:
            inicio = 0
        ultimos = []
        for i in range(inicio, len(self.ocupadas)):
            ultimos.append(self.ocupadas[i])
        return ultimos

    def noches_vendidas(self) -> int:
        total = 0
        for cantidad in self.ocupadas:
            total = total + cantidad
        return total

    def promedio(self) -> float:
        resultado = 0.0
        # Decisión: sin días registrados se devuelve 0 para no dividir entre cero.
        if len(self.ocupadas) > 0:
            resultado = self.noches_vendidas() / len(self.ocupadas)
        return resultado

    def porcentaje_ocupacion(self) -> float:
        resultado = 0.0
        if len(self.ocupadas) > 0:
            # Decisión: se divide una sola vez porque promedio / habitaciones * 100 da 48.0 en un
            # hotel y 48.00000000000001 en otro con el mismo 48 %, y el empate saldría mal.
            resultado = self.noches_vendidas() * 100 / (len(self.ocupadas) * self.habitaciones)
        return resultado

    def desviacion_estandar(self) -> float:
        resultado = 0.0
        if len(self.ocupadas) > 0:
            promedio = self.promedio()
            suma = 0.0
            for cantidad in self.ocupadas:
                suma = suma + (cantidad - promedio) ** 2
            resultado = math.sqrt(suma / len(self.ocupadas))
        return resultado

    def dia_mas_ocupado(self) -> date | None:
        dia = None
        if len(self.ocupadas) > 0:
            posicion_mayor = 0
            for i in range(len(self.ocupadas)):
                # Decisión: con > (y no >=) en un empate se queda el primer día.
                if self.ocupadas[i] > self.ocupadas[posicion_mayor]:
                    posicion_mayor = i
            dia = self.fecha_del_dia(posicion_mayor)
        return dia

    def dia_menos_ocupado(self) -> date | None:
        dia = None
        if len(self.ocupadas) > 0:
            posicion_menor = 0
            for i in range(len(self.ocupadas)):
                if self.ocupadas[i] < self.ocupadas[posicion_menor]:
                    posicion_menor = i
            dia = self.fecha_del_dia(posicion_menor)
        return dia

    def nivel_del_dia(self, cantidad: int) -> str:
        porcentaje = cantidad / self.habitaciones * 100
        if porcentaje < 40:
            nivel = "crítica"
        elif porcentaje < 60:
            nivel = "baja"
        elif porcentaje < 80:
            nivel = "media"
        else:
            nivel = "alta"
        return nivel

    def contar_niveles(self) -> dict[str, int]:
        niveles = {"crítica": 0, "baja": 0, "media": 0, "alta": 0}
        for cantidad in self.ocupadas:
            nivel = self.nivel_del_dia(cantidad)
            niveles[nivel] = niveles[nivel] + 1
        return niveles

    def racha_critica_mas_larga(self) -> tuple[int, date | None]:
        racha_actual = 0
        racha_mayor = 0
        inicio_mayor = 0
        for i in range(len(self.ocupadas)):
            if self.nivel_del_dia(self.ocupadas[i]) == "crítica":
                racha_actual = racha_actual + 1
                if racha_actual > racha_mayor:
                    racha_mayor = racha_actual
                    inicio_mayor = i - racha_actual + 1
            else:
                racha_actual = 0
        inicio = None
        if racha_mayor > 0:
            inicio = self.fecha_del_dia(inicio_mayor)
        return racha_mayor, inicio

    def dias_sin_registrar(self, hoy: date) -> int:
        faltan = (hoy - self.fecha_siguiente()).days
        # Decisión: si da negativo es porque se simularon días hasta después de hoy.
        if faltan < 0:
            faltan = 0
        return faltan


class CadenaHotelera:
    def __init__(self) -> None:
        self.hoteles: list[Hotel] = []

    def buscar_hotel(self, nombre: str) -> Hotel | None:
        nombre = nombre.strip()
        encontrado = None
        i = 0
        while i < len(self.hoteles) and encontrado is None:
            if self.hoteles[i].nombre == nombre:
                encontrado = self.hoteles[i]
            i = i + 1
        return encontrado

    def crear_hotel(self, nombre: str, habitaciones: str, anio: str, mes: str, dia: str) -> str:
        nombre = nombre.strip()
        fecha = crear_fecha(anio, mes, dia)
        mensaje = ""
        if nombre == "":
            mensaje = "El nombre no puede estar vacío."
        elif self.buscar_hotel(nombre) is not None:
            mensaje = f"Ya existe un hotel llamado {nombre}."
        elif not es_entero(habitaciones):
            mensaje = "Las habitaciones habilitadas deben ser un número entero."
        elif int(habitaciones) < 1:
            mensaje = "El hotel debe tener al menos una habitación habilitada."
        elif fecha is None:
            mensaje = "La fecha no es válida."
        elif fecha.year < 2000 or fecha.year > 2100:
            # Decisión: con un año como 9999 el registro se pasaría del 31-12-9999,
            # la última fecha que maneja Python, y el programa se caería.
            mensaje = "El año de inicio debe estar entre 2000 y 2100."
        else:
            self.hoteles.append(Hotel(nombre, int(habitaciones), fecha))
        return mensaje

    def hotel_mas_ocupado(self) -> Hotel | None:
        mayor = None
        for hotel in self.hoteles:
            if hotel.dias_registrados() > 0:
                if mayor is None or hotel.porcentaje_ocupacion() > mayor.porcentaje_ocupacion():
                    mayor = hotel
        return mayor

    def hotel_menos_ocupado(self) -> Hotel | None:
        menor = None
        for hotel in self.hoteles:
            if hotel.dias_registrados() > 0:
                if menor is None or hotel.porcentaje_ocupacion() < menor.porcentaje_ocupacion():
                    menor = hotel
        return menor

    def cargar_hoteles(self, ruta: str) -> tuple[int, list[str]]:
        with open(ruta, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
        cargados = 0
        descartadas = []
        # Decisión: se empieza en 1 para saltar el encabezado; el número de línea es i + 1.
        for i in range(1, len(lineas)):
            linea = lineas[i].strip()
            if linea != "":
                campos = linea.split(";")
                if len(campos) != 5:
                    mensaje = "No tiene cinco campos."
                else:
                    mensaje = self.crear_hotel(campos[0], campos[1], campos[2], campos[3], campos[4])
                if mensaje == "":
                    cargados = cargados + 1
                else:
                    descartadas.append(f"Línea {i + 1} descartada: {mensaje}")
        return cargados, descartadas

    def cargar_ocupacion(self, ruta: str) -> tuple[int, list[str]]:
        with open(ruta, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
        cargados = 0
        descartadas = []
        for i in range(1, len(lineas)):
            linea = lineas[i].strip()
            if linea != "":
                campos = linea.split(";")
                if len(campos) != 2:
                    mensaje = "No tiene dos campos."
                else:
                    hotel = self.buscar_hotel(campos[0])
                    if hotel is None:
                        mensaje = f"No hay un hotel llamado {campos[0].strip()}."
                    elif not es_entero(campos[1]):
                        mensaje = "Las habitaciones ocupadas deben ser un número entero."
                    else:
                        mensaje = hotel.validar_ocupadas(int(campos[1]))
                        if mensaje == "":
                            hotel.registrar_dia(int(campos[1]))
                if mensaje == "":
                    cargados = cargados + 1
                else:
                    descartadas.append(f"Línea {i + 1} descartada: {mensaje}")
        return cargados, descartadas

    def guardar(self, ruta_hoteles: str, ruta_ocupacion: str) -> None:
        # Decisión: requisito que agregamos para no perder los datos al cerrar el programa.
        with open(ruta_hoteles, "w", encoding="utf-8") as archivo:
            archivo.write("hotel;habitaciones_habilitadas;año;mes;día\n")
            for hotel in self.hoteles:
                fecha = hotel.fecha_inicio
                archivo.write(f"{hotel.nombre};{hotel.habitaciones};{fecha.year};{fecha.month};{fecha.day}\n")
        with open(ruta_ocupacion, "w", encoding="utf-8") as archivo:
            archivo.write("hotel;habitaciones_ocupadas\n")
            for hotel in self.hoteles:
                for cantidad in hotel.ocupadas:
                    archivo.write(f"{hotel.nombre};{cantidad}\n")