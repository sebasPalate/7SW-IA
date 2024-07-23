# Busqueda Bidireccional
import time
from graphviz import Digraph


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
            acciones.append(nuevo_estado)
    return acciones


def expandir_nodo(nodo):
    acciones = generar_acciones(nodo.estado)
    for accion in acciones:
        hijo = Nodo(accion, padre=nodo)
        nodo.agregar_hijo(hijo)


def bidireccional(nodo_inicial, nodo_final):
    frontera_inicial = [nodo_inicial]
    frontera_final = [nodo_final]
    explorado_inicial = set()
    explorado_final = set()
    nodos_visitados = 0

    while frontera_inicial and frontera_final:
        # Expandir nodos desde el nodo inicial
        nodo_actual_inicial = frontera_inicial.pop()
        expandir_nodo(nodo_actual_inicial)
        explorado_inicial.add(nodo_actual_inicial.estado)
        nodos_visitados += 1

        # Verificar si el estado del nodo inicial está en la frontera final
        for nodo in frontera_final:
            if nodo.estado == nodo_actual_inicial.estado:
                return nodo_actual_inicial, nodo, nodos_visitados

        # Expandir nodos desde el nodo final
        nodo_actual_final = frontera_final.pop()
        expandir_nodo(nodo_actual_final)
        explorado_final.add(nodo_actual_final.estado)
        nodos_visitados += 1

        # Verificar si el estado del nodo final está en la frontera inicial
        for nodo in frontera_inicial:
            if nodo.estado == nodo_actual_final.estado:
                return nodo, nodo_actual_final, nodos_visitados

        # Agregar nuevos nodos a las fronteras
        for hijo in nodo_actual_inicial.hijos:
            if hijo.estado not in explorado_inicial:
                frontera_inicial.append(hijo)
        for hijo in nodo_actual_final.hijos:
            if hijo.estado not in explorado_final:
                frontera_final.append(hijo)

    return None


def main():
    estado_inicial = (3, 3, 1, 0, 0)
    nodo_raiz_inicial = Nodo(estado_inicial)

    estado_final = (0, 0, 0, 3, 3)
    nodo_raiz_final = Nodo(estado_final)

    inicio_tiempo = time.time()
    solucion, solucion_final, nodos_visitados = bidireccional(
        nodo_raiz_inicial, nodo_raiz_final)
    fin_tiempo = time.time()

    if solucion:
        print("Árbol completo:")
        imprimir_arbolConsola(nodo_raiz_inicial, 0)
        imprimir_arbolConsola(nodo_raiz_final, 0)
        print("Se encontro una solución")
        imprimir_camino(solucion_final)

        dot = imprimir_arbol(nodo_raiz_inicial)
        dot = imprimir_arbol(nodo_raiz_final, dot=dot)
        dot.render('arbol_completo_bidireccional', format='png', view=True)

        tiempo_ejecucion = (fin_tiempo - inicio_tiempo) * \
            1000  # Convertir a milisegundos

        print("\nMedidas de rendimiento:")
        print(f"\tNodos visitados: {nodos_visitados}")
        print(f"\tTiempo de ejecución: {tiempo_ejecucion:.2f} ms")
    else:
        print("No se encontró una solución.")


if __name__ == "__main__":
    main()
