from collections import deque

from graphviz import Digraph


class Nodo:
    def __init__(self, info, padre, coste):
        self.info = info
        self.padre = padre
        self.coste = coste
        self.hijos = []

    def agregar_hijo(self, hijo):
        self.hijo = hijo


def imprimir_camino(nodo):
    camino = []
    while nodo:
        camino.append(nodo.info)
        nodo = nodo.padre
    camino.reverse()

    for i, info in enumerate(camino):
        print(f'Paso {i+1}: {info}')


def imprimir_arbol_consola(nodo, nivel=0):
    print(f"{' ' * nivel * 4} Nodo: {nodo.info}")
    for hijo in nodo.hijos:
        imprimir_arbol_consola(hijo, nivel + 1)


def imprimir_arbol(nodo, nivel=0, dot=None):
    if dot is None:
        dot = Digraph(comment='Árbol de búsqueda')
    dot.node(str(nodo.info))
    for hijo in nodo.hijos:
        dot.node(str(hijo.info))  # Agregar el nodo hijo al grafo
        dot.edge(str(nodo.info), str(hijo.info))
        imprimir_arbol(hijo, nivel + 1, dot)
    return dot

# Considere un espacio de estados donde el estado inicial es el número 1 y cada estado k tiene dos sucesores: los números 2k y 2k + 1


def generar_sucesores(info):
    return [info * 2, info * 2 + 1]


def expandir_nodo(nodo):
    sucesores = generar_sucesores(nodo.info)
    print(f'Nodo actual: {nodo.info}, Sucesores: {sucesores}')
    for sucesor in sucesores:
        nuevo_nodo = Nodo(sucesor, nodo, nodo.coste + 1)
        nodo.hijos.append(nuevo_nodo)

    return nodo.hijos


def ids(nodo, profundidad_maxima):
    nodos_visitados = 0

    for profundidad in range(profundidad_maxima):
        resultado, nodos_expandidos = dsf_limitado(nodo, profundidad)
        nodos_visitados += nodos_expandidos
        if resultado:
            return resultado, nodos_visitados
    return None, nodos_visitados


def dsf_limitado(nodo, limite):
    frontera = [(nodo, 0)]
    visitados = set()
    nodos_expandidos = 0

    while frontera:
        nodo_actual, profundidad_actual = frontera.pop()
        nodos_expandidos += 1

        if nodo_actual.info == 11:
            return nodo_actual, nodos_expandidos

        if nodo_actual.coste < limite:
            if nodo_actual.info not in visitados:
                visitados.add(nodo_actual.info)
                hijos = expandir_nodo(nodo_actual)

                for hijo in hijos:
                    frontera.append((hijo, profundidad_actual + 1))

    return None, nodos_expandidos


def main():
    nodo_raiz = Nodo(1, None, 0)
    profundidad_maxima = 5  # Cambiar según el límite de profundidad deseado
    solucion, visitados = ids(nodo_raiz, profundidad_maxima)

    if solucion:
        print('Camino a la Solución!')
        imprimir_camino(solucion)

        print('\nÁrbol de búsqueda:')
        imprimir_arbol_consola(nodo_raiz)

        dot = imprimir_arbol(nodo_raiz)
        dot.render('arbol_completo-IDS', format='png', cleanup=True)
        dot.view()
        print(f"\nNodos visitados: {visitados}")
    else:
        print('No se encontró solución')


if __name__ == '__main__':
    main()
