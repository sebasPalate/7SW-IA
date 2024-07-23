""" PROFUNDIDAD """
from graphviz import Digraph


class Nodo:
    def __init__(self, estado, padre=None):
        self.estado = estado
        self.padre = padre
        self.hijos = []

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

    def __str__(self) -> str:
        resultado = ""
        for fila in self.estado:
            resultado += '  '.join(map(str, fila)) + "\n"
        return resultado

    def __eq__(self, otro):
        return self.estado == otro.estado

    def __hash__(self):
        return hash(str(self.estado))

    def es_solucion(self, solucion):
        return self.estado == solucion


def imprimir_camino(nodo):
    camino = []
    while nodo:
        camino.append(nodo.estado)
        nodo = nodo.padre
    camino.reverse()

    for i, estado in enumerate(camino):
        print(f'Paso {i+1}:', "\n")
        imprimir_tablero(estado)


def imprimir_tablero(tablero):
    for fila in tablero:
        print('  '.join(map(str, fila)))


def imprimir_arbol(nodo, nivel=0, dot=None):
    if dot is None:
        dot = Digraph(comment='Árbol de búsqueda')

    tablero_str = '\n'.join(['  '.join(map(str, fila))
                            for fila in nodo.estado])
    dot.node(str(nodo.estado), label=tablero_str)

    for hijo in nodo.hijos:
        hijo_tablero_str = '\n'.join(
            ['  '.join(map(str, fila)) for fila in hijo.estado])
        dot.node(str(hijo.estado), label=hijo_tablero_str)
        # Conectar nodo padre con nodo hijo
        dot.edge(str(nodo.estado), str(hijo.estado))
        imprimir_arbol(hijo, nivel + 1, dot)

    return dot


def imprimir_arbol_consola(nodo, nivel=0):
    print(f"{' ' * nivel * 4} Nodo: {nodo.estado}")
    for hijo in nodo.hijos:
        imprimir_arbol_consola(hijo, nivel + 1)

# Considere un espacio de estados donde el estado inicial es el siguiente tablero de 8-puzzle:


def obtener_movimientos_validos(estado):
    movimientos = []
    fila_espacio, columna_espacio = encontrar_espacio(estado)
    if fila_espacio > 0:
        movimientos.append((fila_espacio - 1, columna_espacio))
    if fila_espacio < 2:
        movimientos.append((fila_espacio + 1, columna_espacio))
    if columna_espacio > 0:
        movimientos.append((fila_espacio, columna_espacio - 1))
    if columna_espacio < 2:
        movimientos.append((fila_espacio, columna_espacio + 1))
    return movimientos


def encontrar_espacio(tablero):
    for i in range(3):
        for j in range(3):
            if tablero[i][j] == 0:
                return i, j


def generar_sucesores(estado):
    movimientos_validos = obtener_movimientos_validos(estado)
    return [mover(estado, movimiento) for movimiento in movimientos_validos]


def expandir_nodo(nodo):
    sucesores = generar_sucesores(nodo.estado)
    for sucesor in sucesores:
        nuevo_nodo = Nodo(sucesor, nodo)
        nodo.hijos.append(nuevo_nodo)

    return nodo.hijos


def mover(estado, accion):
    fila_espacio, columna_espacio = encontrar_espacio(estado)
    nueva_fila, nueva_columna = accion
    nuevo_estado = [fila[:] for fila in estado]
    nuevo_estado[fila_espacio][columna_espacio], nuevo_estado[nueva_fila][nueva_columna] = \
        nuevo_estado[nueva_fila][nueva_columna], nuevo_estado[fila_espacio][columna_espacio]
    return nuevo_estado


def bfs(estado_inicial, solucion):
    frontera = [estado_inicial]
    visitados = set()

    while frontera:
        nodo_actual = frontera.pop()
        print("Nodo Actual:")
        print(nodo_actual.__str__(), "\n")

        if nodo_actual.es_solucion(solucion):
            return nodo_actual, visitados

        if nodo_actual not in visitados:
            visitados.add(nodo_actual)

            hijos = expandir_nodo(nodo_actual)
            print("Hijos:")
            for hijo in hijos:
                print(hijo.__str__())
                frontera.append(hijo)
    return None, visitados


if __name__ == "__main__":
    tablero_inicial = [
        [1, 2, 0],
        [3, 4, 5],
        [6, 7, 8]
    ]

    tablero_objetivo = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]
    ]

    estado_inicial = Nodo(tablero_inicial)
    solucion, visitados = bfs(estado_inicial, tablero_objetivo)

    if solucion:
        print("Solución encontrada:")
        imprimir_camino(solucion)

        dot = imprimir_arbol(estado_inicial)
        imprimir_arbol_consola(estado_inicial)
        dot.render('arbol_completo', format='png', cleanup=True)
        dot.view()
        print(f"\nNodos visitados:")
        for visitado in visitados:
            print(visitado.__str__(), "\n")
    else:
        print("No se encontró solución.")
