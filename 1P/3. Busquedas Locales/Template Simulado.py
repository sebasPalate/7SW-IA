# Juego de las 8 reinas con el algoritmo: template simulado
import random
import copy
import math

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


def temperatura_actual(iteracion):
    return 1 / iteracion


def movimiento_aleatorio(tablero):
    n = len(tablero)
    columna = random.randint(0, n - 1)

    # Encuentra la fila actual de la reina en la columna j
    fila_actual = [fila for fila in range(n) if tablero[fila][columna] == 1][0]
    print("Fila actual:", fila_actual)

    nueva_fila = random.randint(0, n - 1)
    while nueva_fila == fila_actual:
        nueva_fila = random.randint(0, n - 1)
    return fila_actual, columna, nueva_fila


def templete_simulado(tablero, temp):
    iteracion = 1

    while ataques_en_tablero(tablero) != 0:
        print("\t->Iteracion: ", iteracion)

        nueva_solucion = copy.deepcopy(tablero)
        fila_actual, j, nueva_fila = movimiento_aleatorio(nueva_solucion)
        nueva_solucion[fila_actual][j] = 0
        nueva_solucion[nueva_fila][j] = 1

        delta_energia = ataques_en_tablero(
            nueva_solucion) - ataques_en_tablero(tablero)
        if delta_energia < 0 or random.random() < math.exp(-delta_energia / temp):
            tablero = nueva_solucion
            print("Nuevo tablero:")
            print("Ataques:", ataques_en_tablero(tablero))
            imprimir_tablero(tablero)
            print("\n")

        temp = temperatura_actual(iteracion)
        iteracion += 1

    return tablero


# Ejecutar el algoritmo
if __name__ == "__main__":
    tablero = tablero_inicial_random(8)
    print("Tablero inicial:")
    imprimir_tablero(tablero)
    print("Ataques en el tablero inicial:", ataques_en_tablero(tablero))
    solucion = templete_simulado(tablero, 100)
    imprimir_dos_tableros_con_colores(tablero, solucion)
