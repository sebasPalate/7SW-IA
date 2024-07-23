from graphviz import Digraph
import heapq
import random

# Clase para representar el estado del tablero


class EstadoPuzzle:
    # Estado objetivo del tablero
    estado_objetivo = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    posicion_objetivo = {}  # Posiciones del estado objetivo

    def __init__(self, estado, padre=None, movimiento="Inicial", profundidad=0):
        self.estado = estado  # Estado actual del tablero
        self.padre = padre  # Nodo padre
        self.movimiento = movimiento  # Movimiento que llevó al estado actual
        self.profundidad = profundidad  # Profundidad del nodo en el árbol

    # Método para generar los posibles movimientos
    def movimientos_posibles(self):
        movimientos = []
        indice = self.estado.index(0)  # Posición del espacio vacío
        if indice % 3 < 2:
            movimientos.append("Derecha")
        if indice % 3 > 0:
            movimientos.append("Izquierda")
        if indice < 6:
            movimientos.append("Abajo")
        if indice > 2:
            movimientos.append("Arriba")
        return movimientos

    # Método para realizar un movimiento en el tablero
    def mover_blanco(self, direccion):
        indice_blanco = self.estado.index(0)
        if direccion == "Arriba":
            nuevo_indice = indice_blanco - 3
        elif direccion == "Abajo":
            nuevo_indice = indice_blanco + 3
        elif direccion == "Izquierda":
            nuevo_indice = indice_blanco - 1
        elif direccion == "Derecha":
            nuevo_indice = indice_blanco + 1

        nuevo_estado = self.estado[:]
        nuevo_estado[indice_blanco], nuevo_estado[nuevo_indice] = nuevo_estado[nuevo_indice], nuevo_estado[indice_blanco]

        return nuevo_estado

    # Método para calcular la distancia de Manhattan
    def distancia_manhattan(self):
        distancia = 0
        for i in range(1, 9):
            posicion_actual = self.estado.index(i)
            posicion_objetivo = self.posicion_objetivo[i]
            distancia += abs(posicion_actual % 3 - posicion_objetivo %
                             3) + abs(posicion_actual // 3 - posicion_objetivo // 3)
        return distancia

    # Método para verificar si el estado es igual al estado objetivo
    def es_objetivo(self):
        return self.estado == self.estado_objetivo

    # Método para generar los hijos del nodo actual
    def generar_hijos(self):
        hijos = []
        for movimiento in self.movimientos_posibles():
            nuevo_estado = self.mover_blanco(movimiento)
            hijos.append(EstadoPuzzle(nuevo_estado, self,
                         movimiento, self.profundidad + 1))
        return hijos

    # Método para obtener el camino desde el nodo inicial hasta el nodo actual
    def obtener_camino(self):
        camino = []
        nodo_actual = self
        while nodo_actual is not None:
            camino.append(nodo_actual)
            nodo_actual = nodo_actual.padre
        camino.reverse()
        return camino

    # Método para imprimir el estado del tablero
    def imprimir_estado(self):
        for i in range(0, 9, 3):
            print(self.estado[i:i + 3])
        print()

    # Método para inicializar las posiciones del estado objetivo
    @staticmethod
    def inicializar_posicion_objetivo():
        for i, num in enumerate(EstadoPuzzle.estado_objetivo):
            EstadoPuzzle.posicion_objetivo[num] = i

    # Método para permitir la comparación de instancias de EstadoPuzzle
    def __lt__(self, other):
        return self.distancia_manhattan() + self.profundidad < other.distancia_manhattan() + other.profundidad

# Función para resolver el 8 puzzle utilizando el algoritmo A*


def resolver_puzzle(estado_inicial):
    # Inicializar las posiciones del estado objetivo
    EstadoPuzzle.inicializar_posicion_objetivo()
    lista_abierta = []
    lista_cerrada = set()
    heapq.heappush(lista_abierta, estado_inicial)
    # Almacenar todos los nodos generados
    nodos = {tuple(estado_inicial.estado): estado_inicial}

    while lista_abierta:
        estado_actual = heapq.heappop(lista_abierta)
        if estado_actual.es_objetivo():
            # Devolver el camino y los nodos generados
            return estado_actual.obtener_camino(), nodos

        lista_cerrada.add(tuple(estado_actual.estado))

        for hijo in estado_actual.generar_hijos():
            if tuple(hijo.estado) not in lista_cerrada:
                heapq.heappush(lista_abierta, hijo)
                nodos[tuple(hijo.estado)] = hijo

    return None, None


# Función para generar un tablero aleatorio


def generar_puzzle_aleatorio():
    puzzle = EstadoPuzzle([0, 1, 2, 3, 4, 5, 6, 7, 8])
    movimientos = 50  # Número de movimientos aleatorios para mezclar el tablero
    for _ in range(movimientos):
        movimientos_posibles = puzzle.movimientos_posibles()
        movimiento_aleatorio = random.choice(movimientos_posibles)
        puzzle.estado = puzzle.mover_blanco(movimiento_aleatorio)
    return puzzle

# Función para visualizar el árbol completo


def visualizar_arbol(nodos):
    dot = Digraph()

    for estado in nodos.values():
        # Convertir lista del estado del tablero a una cadena de texto con formato de tablero
        estado_str = "\n".join(
            [", ".join(map(str, estado.estado[i:i+3])) for i in range(0, 9, 3)])
        # Calcular h, g, y f
        h = estado.distancia_manhattan()
        g = estado.profundidad
        f = h + g
        # Agregar el tablero del rompecabezas y las métricas como etiqueta del nodo
        label = f"{estado_str}\nh={h}\ng={g}\nf={f}"
        dot.node(str(estado.estado), label=label, shape="plaintext")

    for estado in nodos.values():
        if estado.padre is not None:
            dot.edge(str(estado.padre.estado), str(
                estado.estado), label=estado.movimiento)

    dot.render('arbol_completo', format='png', cleanup=True)


if __name__ == "__main__":
    estado_inicial = generar_puzzle_aleatorio()
    print("Tablero inicial:")
    estado_inicial.imprimir_estado()

    solucion, nodos = resolver_puzzle(estado_inicial)

    if solucion:
        print("Se encontró una solución:")
        for paso, estado in enumerate(solucion):
            h = estado.distancia_manhattan()
            # Calcular f = h + g, donde g es la profundidad
            f = h + estado.profundidad
            print(f"Paso {paso}: Movimiento {estado.movimiento}")
            # Imprimir información sobre el movimiento
            print(f"h = {h}, g = {estado.profundidad}, f = {f}")
            estado.imprimir_estado()

        print("-->ÁRBOL<--")
        visualizar_arbol(nodos)

    else:
        print("No se encontró una solución.")
