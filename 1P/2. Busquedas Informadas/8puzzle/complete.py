# rompecabezas.py

import random
import copy
import heapq


class Nodo:
    def __init__(self, rompecabezas, direccion=None, g=0):
        self.rompecabezas = rompecabezas
        self.direccion = direccion
        self.g = g

    def __lt__(self, other):
        return self.g < other.g


def generar_matriz_aleatoria():
    numeros = random.sample(range(9), 9)

    grupos_de_tres = []

    for i in range(0, len(numeros), 3):
        grupo = numeros[i:i+3]  # Tomar un grupo de tres elementos
        grupos_de_tres.append(grupo)  # Agregar el grupo a la lista de grupos

    return grupos_de_tres


def movimientos_posibles(puzzle):
    i, j = encontrar_ficha(puzzle, 0)
    mapa = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    resultado = []
    dir = {
        (-1, 0): "ARRIBA",
        (1, 0): "ABAJO",
        (0, -1): "IZQUIERDA",
        (0, 1): "DERECHA"
    }
    for k in mapa:
        if 0 <= i + k[0] < 3 and 0 <= j + k[1] < 3:
            resultado.append(dir[k])
    return resultado

# Funciones de heurística, camino acumulado y costo


def heuristica(puzzle, objetivo):
    return sum(1 for i in range(3) for j in range(3) if puzzle[i][j] != objetivo[i][j])


def camino_acumulado(ruta):
    return len(ruta) - 1


def costo(ruta, objetivo):
    return camino_acumulado(ruta) + heuristica(ruta[-1].rompecabezas, objetivo)

#


def encontrar_ficha(puzzle, num):
    for i, fila in enumerate(puzzle):
        if num in fila:
            return i, fila.index(num)


def generar_estado(nodo, movimientos_posibles):
    dir_dict = {
        "ARRIBA": (-1, 0),
        "ABAJO": (1, 0),
        "IZQUIERDA": (0, -1),
        "DERECHA": (0, 1)
    }

    i, j = encontrar_ficha(nodo.rompecabezas, 0)
    mover_a = []
    for d in movimientos_posibles:
        new_i, new_j = i + dir_dict[d][0], j + dir_dict[d][1]
        if 0 <= new_i < 3 and 0 <= new_j < 3:
            nuevo_rompecabezas = copy.deepcopy(nodo.rompecabezas)
            nuevo_rompecabezas[i][j], nuevo_rompecabezas[new_i][new_j] = nuevo_rompecabezas[new_i][new_j], nuevo_rompecabezas[i][j]
            mover_a.append(Nodo(nuevo_rompecabezas, d, nodo.g + 1))

    return mover_a

#


def mostrar_rompecabezas(ruta, objetivo):
    for i, paso in enumerate(ruta):
        rompecabezas, direccion = paso.rompecabezas, paso.direccion
        g = paso.g
        h = heuristica(rompecabezas, objetivo)
        f = g + h
        print("    Paso {} -> {}".format(i, direccion))
        print("   g = {} h = {} f = {}".format(g, h, f))
        print()

        for fila in rompecabezas:
            print("\t", " ".join(map(str, fila)))
        print("")


def obtener_inversiones(puzzle):
    flatten_puzzle = [num for fila in puzzle for num in fila if num != 0]
    return [(flatten_puzzle[i], flatten_puzzle[j]) for i in range(len(flatten_puzzle)) for j in range(i + 1, len(flatten_puzzle)) if flatten_puzzle[i] > flatten_puzzle[j]]


def tiene_solucion(puzzle, objetivo):
    inversiones_puzzle = obtener_inversiones(puzzle)
    inversiones_objetivo = obtener_inversiones(objetivo)

    mensaje = "Número de inversiones en el rompecabezas aleatorio: {}\nInversiones en el rompecabezas aleatorio: {}".format(
        len(inversiones_puzzle), inversiones_puzzle)

    return (len(inversiones_puzzle) % 2 == 0) == (len(inversiones_objetivo) % 2 == 0), mensaje


def resolver_rompecabezas(puzzle, objetivo):
    solucion, mensaje_solucion = tiene_solucion(puzzle, objetivo)

    if not solucion:
        print("El rompecabezas no tiene solucion :(")
        print(mensaje_solucion)
        return None

    camino = []
    revisado = {tuple(map(tuple, map(tuple, puzzle))): 0}

    heapq.heappush(camino, (costo([Nodo(puzzle, "INICIO", 0)], objetivo), [
                   Nodo(puzzle, "INICIO", 0)]))

    while camino:
        ruta_actual = heapq.heappop(camino)[1]
        nodo_actual = ruta_actual[-1]

        if nodo_actual.rompecabezas == objetivo:
            return ruta_actual

        if revisado[tuple(map(tuple, nodo_actual.rompecabezas))] < nodo_actual.g:
            continue

        # Generar estados sucesores
        siguientes_estados = generar_estado(
            nodo_actual, movimientos_posibles(nodo_actual.rompecabezas))

        # Explorar los estados sucesores
        for siguiente_nodo in siguientes_estados:

            # Verificar si el estado ya ha sido revisado
            if tuple(map(tuple, map(tuple, siguiente_nodo.rompecabezas))) in revisado:
                if siguiente_nodo.g < revisado[tuple(map(tuple, map(tuple, siguiente_nodo.rompecabezas)))]:
                    revisado[tuple(
                        map(tuple, map(tuple, siguiente_nodo.rompecabezas)))] = siguiente_nodo.g
                    heapq.heappush(camino, (costo(
                        ruta_actual + [siguiente_nodo], objetivo), ruta_actual + [siguiente_nodo]))
            else:
                revisado[tuple(
                    map(tuple, map(tuple, siguiente_nodo.rompecabezas)))] = siguiente_nodo.g
                heapq.heappush(camino, (costo(
                    ruta_actual + [siguiente_nodo], objetivo), ruta_actual + [siguiente_nodo]))

    # Si no se encuentra solución, se imprime un mensaje y se devuelve None
    print("No se encontró solución.")
    return None


# EJEMPLO DE USO
# Generar una matriz aleatoria de 3x3
rompecabezas_inicial = generar_matriz_aleatoria()

# Imprimir la matriz aleatoria
print("\nEstado Inicial:")
for fila in rompecabezas_inicial:
    print("\t", " ".join(map(str, fila)))

# Ingresar la matriz objetivo
print("\nEstado Objetivo:")
objetivo = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8]
]
for fila in objetivo:
    print("\t", " ".join(map(str, fila)))

print("\n")

# Resolver el rompecabezas
solucion = resolver_rompecabezas(rompecabezas_inicial, objetivo)

# Mostrar la solución
if solucion is not None:
    mostrar_rompecabezas(solucion, objetivo)
else:
    print("No se encontró solución.")
