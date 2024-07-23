# Juego de las 8 reinas con el algoritmo: ascenso de colinas estocastico
import random
import copy

import numpy as np
import matplotlib.pyplot as plt


def tablero_inicial_random(n):
    tablero = []
    for i in range(n):
        tablero.append([0]*n)

    for j in range(n):  # Itera sobre las columnas
        posicion_reina = random.randint(0, n-1)
        tablero[posicion_reina][j] = 1

    return tablero


def imprimir_tablero(tablero):
    for fila in tablero:
        print('  '.join(map(str, fila)))


def imprimir_dos_tableros_con_colores(tablero, solucion):
    n = len(tablero)

    chessboard1 = np.zeros((n, n, 3))
    chessboard2 = np.zeros((n, n, 3))

    for i in range(n):
        for j in range(n):
            if tablero[i][j] == 1:
                # Rojo para las reinas en el primer tablero
                chessboard1[i, j] = [1, 0, 0]

            if solucion[i][j] == 1:
                # Azul para las reinas en el segundo tablero
                chessboard2[i, j] = [0, 0, 1]

    fig, axs = plt.subplots(1, 2, figsize=(8, 4))  # 1 fila, 2 columnas

    axs[0].imshow(chessboard1, interpolation='nearest')
    axs[0].set_facecolor('white')  # Fondo blanco
    axs[0].grid(True, which='both', linestyle='-', linewidth=1, color='white')
    axs[0].set_xticks(np.arange(-0.5, n - 0.5, 1))
    axs[0].set_yticks(np.arange(-0.5, n - 0.5, 1))
    axs[0].set_title('Tablero Inicial')

    axs[1].imshow(chessboard2, interpolation='nearest')
    axs[1].set_facecolor('white')  # Fondo blanco
    axs[1].grid(True, which='both', linestyle='-', linewidth=1, color='white')
    axs[1].set_xticks(np.arange(-0.5, n - 0.5, 1))
    axs[1].set_yticks(np.arange(-0.5, n - 0.5, 1))
    axs[1].set_title('Solución')

    plt.show()


def ataques_en_tablero(tablero):
    n = len(tablero)
    ataques_totales = 0

    for i in range(n):
        for j in range(n):
            if tablero[i][j] == 1:
                # Verificar la columna
                for k in range(n):
                    if k != i and tablero[k][j] == 1:
                        ataques_totales += 1

                # Verificar fila
                for k in range(n):
                    if k != j and tablero[i][k] == 1:
                        ataques_totales += 1

                # Verificar diagonales
                for k in range(n):
                    for l in range(n):
                        if k != i and l != j and tablero[k][l] == 1:
                            if abs(i - k) == abs(j - l):
                                ataques_totales += 1

    return ataques_totales // 2  # Dividir por 2 para evitar el doble conteo


# Asenso de colinas estocastico (mover fichas aleatoriamente)
def ascenso_colina_estocastico(tablero):

    # Mientras haya ataques en el tablero
    while ataques_en_tablero(tablero) != 0:
        for fila in range(len(tablero)):
            for columna in range(len(tablero)):

                if tablero[fila][columna] == 1:
                    # Mover la reina a una nueva posición aleatoria (0 - 7)
                    x = random.randint(0, len(tablero)-1)
                    y = columna  # Mantener la columna fija

                    if tablero[x][y] != 1:
                        tablero_aux = copy.deepcopy(tablero)
                        tablero_aux[fila][columna] = 0
                        tablero_aux[x][y] = 1

                        # Si el nuevo tablero tiene menos ataques, actualizar el tablero
                        if ((ataques_en_tablero(tablero_aux) <= ataques_en_tablero(tablero))):
                            tablero = copy.deepcopy(tablero_aux)
                            print("Nuevo Tablero: ")
                            print("Ataques:", ataques_en_tablero(tablero))
                            imprimir_tablero(tablero)
                            print("\n")
    return tablero


# Ejecutar el algoritmo
if __name__ == "__main__":
    tablero = tablero_inicial_random(8)
    print("Ataques en el tablero inicial:", ataques_en_tablero(tablero))
    print("Tablero inicial:")
    imprimir_tablero(tablero)
    solucion = ascenso_colina_estocastico(tablero)
    imprimir_dos_tableros_con_colores(tablero, solucion)
