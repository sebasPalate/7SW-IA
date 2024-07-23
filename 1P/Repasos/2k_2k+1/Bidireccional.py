from collections import deque
from graphviz import Digraph

class Nodo:
    def __init__(self, info, padre=None, coste=0):
        self.info = info
        self.padre = padre
        self.coste = coste
        self.hijos = []

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

def imprimir_camino(nodo):
    camino = []
    while nodo:
        camino.append(nodo.info)
        nodo = nodo.padre
    camino.reverse()

    for i, info in enumerate(camino):
        print(f'Paso {i+1}: {info}')

def imprimir_arbol_consola(nodo, nivel=0):
    print(' ' * nivel * 4, nodo.info)
    for hijo in nodo.hijos:
        imprimir_arbol_consola(hijo, nivel + 1)

def imprimir_arbol(nodo, nivel=0, dot=None):
    if dot is None:
        dot = Digraph(comment='Árbol de búsqueda')
    dot.node(str(nodo.info))
    for hijo in nodo.hijos:
        dot.node(str(hijo.info))
        dot.edge(str(nodo.info), str(hijo.info))
        imprimir_arbol(hijo, nivel + 1, dot)
    return dot

def generar_sucesores(info):
    return [info * 2, info * 2 + 1]

def expandir_nodo(nodo):
    sucesores = generar_sucesores(nodo.info)
    for sucesor in sucesores:
        nuevo_nodo = Nodo(sucesor, nodo, nodo.coste + 1)
        nodo.agregar_hijo(nuevo_nodo)
    return nodo.hijos

def bidireccional(nodo_raiz, nodo_objetivo):
    frontera_inicial = deque([nodo_raiz])
    frontera_objetivo = deque([nodo_objetivo])
    visitados_inicial = set()
    visitados_objetivo = set()
    visitados = 0

    while frontera_inicial and frontera_objetivo:
        visitados += 2  # Visitamos un nodo de cada frontera en cada iteración
        # Búsqueda desde el nodo raíz
        nodo_actual_inicial = frontera_inicial.popleft()
        visitados_inicial.add(nodo_actual_inicial.info)
        if nodo_actual_inicial.info in visitados_objetivo:
            return nodo_actual_inicial, visitados
        expandir_nodo(nodo_actual_inicial)
        for hijo in nodo_actual_inicial.hijos:
            if hijo.info not in visitados_inicial:
                frontera_inicial.append(hijo)

        # Búsqueda desde el nodo objetivo
        nodo_actual_objetivo = frontera_objetivo.popleft()
        visitados_objetivo.add(nodo_actual_objetivo.info)
        if nodo_actual_objetivo.info in visitados_inicial:
            return nodo_actual_objetivo, visitados
        expandir_nodo(nodo_actual_objetivo)
        for hijo in nodo_actual_objetivo.hijos:
            if hijo.info not in visitados_objetivo:
                frontera_objetivo.append(hijo)

    return None, visitados

def main():
    nodo_raiz = Nodo(1)
    nodo_objetivo = Nodo(11) # Definir el objetivo deseado
    solucion, visitados = bidireccional(nodo_raiz, nodo_objetivo)

    if solucion:
        print('Camino a la Solución:')
        imprimir_camino(solucion)
        dot = imprimir_arbol(nodo_raiz)
        dot.render('arbol_completo-BIR', format='png', cleanup=True)
        dot.view()
        print(f"\nNodos visitados: {visitados}")
    else:
        print('No se encontró solución')

if __name__ == '__main__':
    main()
