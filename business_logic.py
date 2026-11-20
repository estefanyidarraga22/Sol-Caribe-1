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