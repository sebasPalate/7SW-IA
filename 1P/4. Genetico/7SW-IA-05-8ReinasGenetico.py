import random


def generar_poblacion(n, n_individuos):
    # Verificar que n sea al menos 4
    if n < 4:
        print("El número de reinas debe ser al menos 4")
        return []
    elif n_individuos < 3:
        print("El número de individuos debe ser al menos 3")
        return []
    elif n_individuos > n ** n:
        print("El número de individuos no puede ser mayor a", n ** n)
        return []
    else:
        posiciones_reinas = []
        while len(posiciones_reinas) < n_individuos:
            posiciones = [random.randint(0, n - 1) for _ in range(n)]
            # posiciones_reinas.append(posiciones)

            # Verifica si las posiciones generadas ya existen
            if posiciones not in posiciones_reinas:
                posiciones_reinas.append(posiciones)

        return posiciones_reinas


def seleccion_padres(poblacion):
    # Calcular el total de ataques y las probabilidades de cada individuo
    total_ataques = sum(max_ataques(len(poblacion[0])) - contar_ataques(individuo)
                        for individuo in poblacion)

    if total_ataques == 0:
        print("Todos los individuos de la población tiene el maximo de ataques probables, por lo cual se selecionaran dos individuos aleatorios.")
        return random.choice(poblacion), random.choice(poblacion)

    probabilidades = [(max_ataques(len(poblacion[0])) - contar_ataques(individuo)) /
                      total_ataques for individuo in poblacion]

    # Crear el vector de selección basado en las probabilidades
    vector_seleccion = []
    for individuo, probabilidad in zip(poblacion, probabilidades):
        num_posiciones = int(probabilidad * 100000)
        vector_seleccion.extend([individuo] * num_posiciones)

    print("Vector de selección:", len(vector_seleccion))

    # Seleccionar dos padres diferentes aleatoriamente
    random.shuffle(vector_seleccion)
    padre1 = random.choice(vector_seleccion)
    padre2 = random.choice(vector_seleccion)

    return padre1, padre2


def contar_ataques(individuo):
    n = len(individuo)
    ataques = 0
    for i in range(n):
        for j in range(i + 1, n):
            # Verificar ataques en la misma fila
            if individuo[i] == individuo[j]:
                ataques += 1
            # Verificar ataques en la misma diagonal
            elif abs(individuo[i] - individuo[j]) == abs(i - j):
                ataques += 1
    return ataques


def max_ataques(n):
    max_ataques = 0
    for i in range(n):
        max_ataques += n - i - 1
    return max_ataques


def cruce(padre1, padre2, poblacion):
    n = len(padre1)
    punto_cruce = random.randint(1, n - 1)  # Valor aleatorio entre 1 y n-1

    hijo1 = padre1[:punto_cruce] + padre2[punto_cruce:]
    hijo2 = padre2[:punto_cruce] + padre1[punto_cruce:]

    agregar_hijos_poblacion(poblacion=poblacion, hijo1=hijo1, hijo2=hijo2)

    return hijo1, hijo2


def agregar_hijos_poblacion(poblacion, hijo1, hijo2):
    poblacion.append(hijo1)
    poblacion.append(hijo2)


def mutacion(probabilidad_mutacion, hijo1, hijo2):
    vector_mutacion = [1] * int(probabilidad_mutacion * 100) + \
        [0] * (100 - int(probabilidad_mutacion * 100))
    random.shuffle(vector_mutacion)
    mutar = random.choice(vector_mutacion)
    if (mutar == 1):
        seleccionar_hijo = random.randint(1, 2)
        if (seleccionar_hijo == 1):
            columna_mutacion = random.randint(0, len(hijo1) - 1)
            valor_original = hijo1[columna_mutacion]
            nuevo_valor = valor_original
            while nuevo_valor == valor_original:  # Asegurar que el nuevo valor sea diferente al original
                nuevo_valor = random.randint(0, len(hijo1) - 1)
            hijo1[columna_mutacion] = nuevo_valor

            print("Hijo 1 mutado:", hijo1)
        else:
            columna_mutacion = random.randint(0, len(hijo2) - 1)
            valor_original = hijo2[columna_mutacion]
            nuevo_valor = valor_original
            while nuevo_valor == valor_original:  # Asegurar que el nuevo valor sea diferente al original
                nuevo_valor = random.randint(0, len(hijo2) - 1)
            hijo2[columna_mutacion] = nuevo_valor

            print("Hijo 2 mutado:", hijo2)
    else:
        print("No muta ningun individuo")


def eliminar_padres(poblacion, padre1, padre2):
    poblacion.remove(padre1)
    poblacion.remove(padre2)


def eliminar_individuos_aleatorios(poblacion):
    # Seleccionar dos individuos aleatorios de la población y eliminarlos
    individuo1 = random.choice(poblacion)
    poblacion.remove(individuo1)
    individuo2 = random.choice(poblacion)
    poblacion.remove(individuo2)


def controlar_solucion(poblacion, generacion):
    for individuo in poblacion:
        if contar_ataques(individuo) == 0:
            print("Se ha encontrado una solución en",
                  generacion, "generaciones.")
            imprimir_tablero(individuo)
            return True  # Se ha encontrado una solución
    return False  # No se ha encontrado una solución


def imprimir_tablero(individuo):
    n = len(individuo)
    for i in range(n):
        row = ""
        for j in range(n):
            if individuo[j] == i:
                row += "1 "
            else:
                row += "0 "
        print(row)
    print()

# Mejor Tablero


def mejor_individuo(tableros):
    mejor_individuo = tableros[0]
    for tablero in tableros:
        if contar_ataques(tablero) < contar_ataques(mejor_individuo):
            mejor_individuo = tablero
    print("Ataques: ", contar_ataques(mejor_individuo))
    return mejor_individuo


def solucion(generaciones_max, poblacion, probabilidad_mutacion):
    iteraciones = 0
    while not controlar_solucion(poblacion, iteraciones) and len(poblacion) > 1:
        if iteraciones == generaciones_max:
            print("No se ha encontrado una solución en",
                  generaciones_max, "generaciones.")
            print("El mejor tablero es:")
            imprimir_tablero(mejor_individuo(poblacion))
            break
        print("Generación: ", iteraciones)
        print("Población: ", len(poblacion))
        # Seleccionar padres
        padre1, padre2 = seleccion_padres(poblacion)

        # Cruzar padres para generar hijos
        hijo1, hijo2 = cruce(padre1, padre2, poblacion)

        # Aplicar mutación a los hijos
        mutacion(probabilidad_mutacion, hijo1, hijo2)

        # Eliminar padres de la población
        eliminar_padres(poblacion, padre1, padre2)

        # Eliminar dos individuos aleatorios de la población
        # eliminar_individuos_aleatorios(poblacion)

        iteraciones += 1


# Ejemplo de uso del algoritmo genético para resolver el problema de las 8 reinas
# Generación inicial de la población
poblacion = generar_poblacion(n=10, n_individuos=10000)
generaciones_max = 20000
probabilidad_mutacion = 0.25
solucion(generaciones_max, poblacion,
         probabilidad_mutacion=probabilidad_mutacion)
