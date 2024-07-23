import time
from graphviz import Digraph
from collections import deque


class Nodo:
    def __init__(self, estado, padre=None, accion=None):
        self.estado = estado
        self.padre = padre
        self.accion = accion
        self.hijos = []

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)


def imprimir_camino(nodo):
    camino = []
    while nodo:
        camino.append(nodo.estado)
        nodo = nodo.padre
    camino.reverse()
    for idx, estado in enumerate(camino):
        print(f"Paso {idx + 1}: {estado}")


def imprimir_arbolConsola(nodo, nivel=0):
    print("     " * nivel + str(nodo.estado))
    for hijo in nodo.hijos:
        imprimir_arbolConsola(hijo, nivel + 1)


def imprimir_arbol(nodo, nivel=0, dot=None):
    if dot is None:
        dot = Digraph(comment='Árbol de búsqueda')
    dot.node(str(nodo.estado))
    for hijo in nodo.hijos:
        dot.node(str(hijo.estado))  # Agregar el nodo hijo al grafo
        dot.edge(str(nodo.estado), str(hijo.estado))
        imprimir_arbol(hijo, nivel + 1, dot)
    return dot


def validar_estado(estado):
    # Verifica si el estado es válido según las reglas del juego
    m_izq, c_izq, b, m_der, c_der = estado
    if m_izq < 0 or c_izq < 0 or m_der < 0 or c_der < 0:
        return False
    if (m_izq != 0 and m_izq < c_izq) or (m_der != 0 and m_der < c_der):
        return False
    return True


def generar_acciones(estado):
    acciones = []
    m_izq, c_izq, b, m_der, c_der = estado
    # Todas las combinaciones de movimiento posibles
    movimientos = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
    for dm, dc in movimientos:
        if b == 1:
            nuevo_estado = (m_izq - dm, c_izq - dc, 0, m_der + dm, c_der + dc)
        else:
            nuevo_estado = (m_izq + dm, c_izq + dc, 1, m_der - dm, c_der - dc)
        if validar_estado(nuevo_estado):
            acciones.append((dm, dc))
    return acciones


def expandir_nodo(nodo):
    acciones = generar_acciones(nodo.estado)
    for accion in acciones:
        dm, dc = accion
        if nodo.estado[4] == 3 and nodo.estado[3] == 3:
            continue
        if nodo.estado[2] == 1:
            nuevo_estado = (nodo.estado[0] - dm, nodo.estado[1] - dc, 0,
                            nodo.estado[3] + dm, nodo.estado[4] + dc)
        else:
            nuevo_estado = (nodo.estado[0] + dm, nodo.estado[1] + dc, 1,
                            nodo.estado[3] - dm, nodo.estado[4] - dc)
        nuevo_nodo = Nodo(nuevo_estado, padre=nodo, accion=accion)
        nodo.agregar_hijo(nuevo_nodo)
    return nodo.hijos


def bfs(nodo):
    inicio_tiempo = time.time()
    frontera = deque([nodo])
    visitados = set()
    visitados.add(nodo.estado)
    nodos_visitados = 1

    while frontera:
        nodo_actual = frontera.popleft()

        if nodo_actual.estado == (0, 0, 0, 3, 3):
            """ for i in range(1000000):
                pass """
            fin_tiempo = time.time()
            tiempo_ejecucion = (fin_tiempo - inicio_tiempo) * \
                1000  # Convertir a milisegundos

            return nodo_actual, nodos_visitados, tiempo_ejecucion

        hijos = expandir_nodo(nodo_actual)
        nodos_visitados += len(hijos)

        for hijo in hijos:
            if hijo.estado not in visitados:
                frontera.append(hijo)
                visitados.add(hijo.estado)
    return None, nodos_visitados, None


def main():
    estado_inicial = (3, 3, 1, 0, 0)
    nodo_raiz = Nodo(estado_inicial)
    solucion, nodos_visitados, tiempo_ejecucion = bfs(nodo_raiz)

    if solucion:
        print("Árbol completo:")
        imprimir_arbolConsola(nodo_raiz, 0)
        print("Se encontró una solución:")
        imprimir_camino(solucion)

        dot = imprimir_arbol(nodo_raiz)
        dot.render('arbol_completo-BFS', format='png', cleanup=True)
        dot.view()

        print("\nMedidas de rendimiento:")
        print(f"\tNodos visitados: {nodos_visitados}")
        print(f" \tTiempo de ejecución: {tiempo_ejecucion:.2f} ms")
    else:
        print("No se encontró una solución.")


if __name__ == "__main__":
    main()
