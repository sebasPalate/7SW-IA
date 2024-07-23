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
    m_izq, c_izq, b, m_der, c_der = estado
    if m_izq < 0 or c_izq < 0 or m_der < 0 or c_der < 0:
        return False
    if (m_izq != 0 and m_izq < c_izq) or (m_der != 0 and m_der < c_der):
        return False
    return True


def generar_acciones(estado):
    acciones = []
    m_izq, c_izq, b, m_der, c_der = estado
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
            continue  # Evitar bucle infinito si ya hemos llegado al estado meta
        if nodo.estado[2] == 1:
            nuevo_estado = (nodo.estado[0] - dm, nodo.estado[1] - dc, 0,
                            nodo.estado[3] + dm, nodo.estado[4] + dc)
        else:
            nuevo_estado = (nodo.estado[0] + dm, nodo.estado[1] + dc, 1,
                            nodo.estado[3] - dm, nodo.estado[4] - dc)
        nuevo_nodo = Nodo(nuevo_estado, padre=nodo, accion=accion)
        nodo.agregar_hijo(nuevo_nodo)
    return nodo.hijos


def ids(nodo, profundidad_max):
    inicio_tiempo = time.time()
    nodos_visitados = 0

    for profundidad in range(profundidad_max):
        resultado, nodos_expandidos = dfs_limitado(nodo, profundidad)
        nodos_visitados += nodos_expandidos

        if resultado:
            for i in range(1000000):
                pass
            fin_tiempo = time.time()
            tiempo_ejecucion = (fin_tiempo - inicio_tiempo) * \
                1000  # Convertir a milisegundos
            return resultado, nodos_visitados, tiempo_ejecucion
        
    return None, nodos_visitados, None


def dfs_limitado(nodo, limite):
    frontera = [(nodo, 0)]
    visitados = set()
    visitados.add(nodo.estado)
    nodos_expandidos = 0

    while frontera:
        nodo_actual, profundidad_actual = frontera.pop()
        nodos_expandidos += 1

        if nodo_actual.estado == (0, 0, 0, 3, 3):
            return nodo_actual, nodos_expandidos
        
        if profundidad_actual < limite:
            hijos = expandir_nodo(nodo_actual)

            for hijo in hijos:
                if hijo.estado not in visitados:
                    frontera.append((hijo, profundidad_actual + 1))
                    visitados.add(hijo.estado)

    return None, nodos_expandidos


def main():
    estado_inicial = (3, 3, 1, 0, 0)
    nodo_raiz = Nodo(estado_inicial)
    profundidad_max = 100  # Profundidad máxima para IDS
    solucion, nodos_visitados, tiempo_ejecucion = ids(
        nodo_raiz, profundidad_max)
    if solucion:
        print("Árbol completo:")
        imprimir_arbolConsola(nodo_raiz, 0)
        print("Se encontró una solución:")
        imprimir_camino(solucion)

        dot = imprimir_arbol(nodo_raiz)
        dot.render('arbol_completo-IDS', format='png', cleanup=True)
        dot.view()

        print("\nMedidas de rendimiento:")
        print(f"\tNodos visitados: {nodos_visitados}")
        print(f"\tTiempo de ejecución: {tiempo_ejecucion:.2f} ms")
    else:
        print("No se encontró una solución.")


if __name__ == "__main__":
    main()
