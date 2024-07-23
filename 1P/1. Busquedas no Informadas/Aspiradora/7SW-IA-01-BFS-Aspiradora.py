from collections import deque
from enum import Enum
import copy
import time

# DEFINICION DEL PROBLEMA


class EstadoHabitacion(Enum):
    SUCIO = "SUCIO"
    LIMPIO = "LIMPIO"


class Habitacion:
    def __init__(self, nombre, estado):
        self.nombre = nombre
        self.estado = estado

    def __str__(self):
        return f"Habitación: {self.nombre} - Estado: {self.estado.value}"


class Estado:
    def __init__(self, habitacion_actual, habitaciones):
        self.habitacion_actual = habitaciones[habitacion_actual]
        self.habitaciones = habitaciones

    def get_estado(self):
        estado_actual = {
            "sprdr": self.habitacion_actual.nombre,
            "hbtcns": {habitacion.nombre: habitacion.estado.value for habitacion in self.habitaciones.values()}
        }
        return estado_actual

    def objetivo(self):
        return all(hab.estado == EstadoHabitacion.LIMPIO for hab in self.habitaciones.values())

    def acciones(self):
        acciones = ["mover_izquierda", "mover_derecha", "aspirar"]
        return acciones

    def aplicar_accion(self, accion):
        # Copiar el estado actual para evitar modificarlo directamente
        nuevo_estado = copy.deepcopy(self)

        # Obtener la habitación actual
        habitacion_actual_nombre = nuevo_estado.habitacion_actual.nombre

        # Aplicar la acción
        if accion == "mover_izquierda":
            habitacion_actual_nombre = "A" if habitacion_actual_nombre == "B" else habitacion_actual_nombre
        elif accion == "mover_derecha":
            habitacion_actual_nombre = "B" if habitacion_actual_nombre == "A" else habitacion_actual_nombre
        elif accion == "aspirar":
            nuevo_estado.habitaciones[habitacion_actual_nombre].estado = EstadoHabitacion.LIMPIO

        # Actualizar la habitación actual en el nuevo estado
        nuevo_estado.habitacion_actual = nuevo_estado.habitaciones[
            habitacion_actual_nombre]

        print("\tHijo", accion, ":", nuevo_estado.get_estado())
        return nuevo_estado

    def __eq__(self, otro_estado):
        if not isinstance(otro_estado, Estado):
            return False
        return self.get_estado() == otro_estado.get_estado()

    def __hash__(self):
        return hash(str(sorted(self.get_estado().items())))


# CONSTRUCCION DEL ARBOL
class Nodo:
    def __init__(self, info) -> None:
        self.padre = None
        self.hijos = []
        self.info = info

    def __str__(self) -> str:
        cadena = "Nodo " + str(self.info) + " --->"

        if self.padre is not None:
            cadena += "\tPadre: " + str(self.padre.info) + " "
        else:
            cadena += "\tPadre: None "

        if self.hijos:
            cadena += "\tHijos: " + \
                ", ".join([str(hijo.info) for hijo in self.hijos]) + " "
        else:
            cadena += "\tHijos: None "

        return cadena


class Arbol:
    def __init__(self) -> None:
        self.raiz = None

    def bfs(self):
        if self.raiz is None:
            return []

        visitados = []
        frontera = deque([self.raiz])
        start_time = time.time()

        while frontera:
            nodo_actual = frontera.popleft()
            estado_actual = nodo_actual.info

            # Verificar si llegamos al estado objetivo
            if estado_actual.objetivo():
                print("\n¡Estado Objetivo Encontrado!\n")
                visitados.append(estado_actual)
                break

            # Se añade el estado inicial a los visitados
            visitados.append(estado_actual)
            print("\nPadre:", estado_actual.get_estado())

            # Aplicar las acciones a los estados (añadir hijos)
            for accion in estado_actual.acciones():
                nuevo_estado = estado_actual.aplicar_accion(accion)

                nuevo_nodo = Nodo(nuevo_estado)
                nuevo_nodo.padre = nodo_actual
                nodo_actual.hijos.append(nuevo_nodo)

                if nuevo_estado not in visitados:
                    frontera.append(nuevo_nodo)

            print("\nFrontera: ")
            for frntr in frontera:
                print(frntr.info.get_estado())

            print("\nVisitados: ")
            for vsitd in visitados:
                print(vsitd.get_estado())

        return visitados

    def mostrar_arbol(self, sangria=5):
        if self.raiz is None:
            print("¡Árbol Vacío!")
            return

        def mostrar_arbol_rec(nodo, cadena):
            # print(str(nodo.info.get_estado()))
            estado = nodo.info
            estado_dict = estado.get_estado()
            objetivo_marker = "\t <-------" if estado.objetivo() else ""
            print(f"{estado_dict}{objetivo_marker}")

            for hijo in nodo.hijos:
                connector = "├" if nodo.hijos.index(
                    hijo) < len(nodo.hijos) - 1 else "└"
                print(f"{cadena}{connector}{'─' * sangria}", end="")
                mostrar_arbol_rec(hijo, f"{cadena}{'│':<{sangria}}")

        mostrar_arbol_rec(self.raiz, "")


# Ejemplo de uso corregido
habitaciones = {
    "A": Habitacion("A", EstadoHabitacion.SUCIO),
    "B": Habitacion("B", EstadoHabitacion.SUCIO),
}

habitacion_actual = "A"

# Pasar la lista de valores de las habitaciones
estado_inicial = Estado(habitacion_actual, habitaciones)
arbol = Arbol()
arbol.raiz = Nodo(estado_inicial)

# Realizar la búsqueda BFS
bfs_visitados = arbol.bfs()

# Mostrar el árbol antes de la búsqueda BFS
arbol.mostrar_arbol()

print("Recorrido BFS del árbol:")
for visitado in bfs_visitados:
    print(visitado.get_estado())
