# Juego de las 8 reinas con el algoritmo: ascenso de colinas
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


def validarMovimiento(direccion, i, tablero):
    # Validar si el movimiento es posible
    if (direccion == 'arriba'):
        if i-1 >= 0:
            return i-1
        else:
            return i
    if (direccion == 'abajo'):
        if i+1 < len(tablero):
            return i+1
        else:
            return i


def ascenso_colina(tablero):
    iteracion = 1

    # Mientras haya reinas atacándose y no se alcance el máximo de iteraciones
    while ataques_en_tablero(tablero) != 0 and iteracion <= 100:
        # print("\t-> Iteracion: ", iteracion)
        for i in range(len(tablero)):
            for j in range(len(tablero)):
                if tablero[i][j] == 1:

                    # Movimiento hacia arriba
                    xArriba = validarMovimiento('arriba', i, tablero)
                    auxArriba = copy.deepcopy(tablero)
                    auxArriba[i][j] = 0
                    auxArriba[xArriba][j] = 1

                    # Movimiento hacia abajo
                    xAbajo = validarMovimiento('abajo', i, tablero)
                    auxAbajo = copy.deepcopy(tablero)
                    auxAbajo[i][j] = 0
                    auxAbajo[xAbajo][j] = 1

                    # Obtener el número de ataques en cada tablero
                    ataquesActual = ataques_en_tablero(tablero)
                    ataquesArriba = ataques_en_tablero(auxArriba)
                    ataquesAbajo = ataques_en_tablero(auxAbajo)

                    # Seleccionar el mejor movimiento (vecino)
                    if ((ataquesArriba <= ataquesActual) and (ataquesArriba < ataquesAbajo)):
                        tablero = copy.deepcopy(auxArriba)
                        print("Nuevo Tablero S: ")
                        print("Ataques:", ataques_en_tablero(tablero))
                        imprimir_tablero(tablero)
                        print("\n")
                    elif ((ataquesAbajo < ataquesActual) and (ataquesAbajo < ataquesArriba)):
                        tablero = copy.deepcopy(auxAbajo)
                        print("Nuevo Tablero I: ")
                        print("Ataques:", ataques_en_tablero(tablero))
                        imprimir_tablero(tablero)
                        print("\n")
                    else:
                        print("Tablero: ")
                        print("Ataques:", ataques_en_tablero(tablero))
                        imprimir_tablero(tablero)
                        print("\n")

                    # Salir del bucle interno si se encuentra una reina en la columna
                    if (ataques_en_tablero(tablero) == 0):
                        break
        break
        iteracion += 1
    return tablero


# Ejecutar el algoritmo
if __name__ == "__main__":
    tablero = tablero_inicial_random(8)
    print("Ataques en el tablero inicial:", ataques_en_tablero(tablero))
    print("Tablero inicial:")
    imprimir_tablero(tablero)
    solucion = ascenso_colina(tablero)
    imprimir_dos_tableros_con_colores(tablero, solucion)
