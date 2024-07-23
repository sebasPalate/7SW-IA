import random


def poblacion_inicial(n_individuos):
    if (n_individuos > 2):
        poblacion = []
        for _ in range(n_individuos):
            individuo = [random.randint(0, 1) for _ in range(6)]

            # Verificar que el individuo no esté repetido
            if individuo not in poblacion:
                poblacion.append(individuo)
        return poblacion
    else:
        print("El número de individuos debe ser mayor que 2")
        return []


def seleccionar_padres(poblacion):

    total_iluminacion = sum(iluminacion_maxima() - iluminacion(individuo)
                            for individuo in poblacion)

    total_costo = sum(costo_maximo() - costo(individuo)
                      for individuo in poblacion)

    probabilidades_totales = [(((iluminacion_maxima() - iluminacion(individuo)) / total_iluminacion) +
                              ((costo_maximo() - costo(individuo)) / total_costo)) / 2
                              for individuo in poblacion]

    vector_seleccion = []
    for individuo, probabilidad_total in zip(poblacion, probabilidades_totales):
        print(individuo,
              "->", round(probabilidad_total*100, 2), "%",
              "->", int(round(probabilidad_total*100, 2)))
        num_repeticiones = int(round(probabilidad_total*100, 2))
        vector_seleccion.extend([individuo] * num_repeticiones)

    random.shuffle(vector_seleccion)
    padre1 = random.choice(vector_seleccion)
    padre2 = random.choice(vector_seleccion)

    """ # Verificar que los padres sean diferentes
    while padre1 == padre2:
        padre2 = random.choice(vector_seleccion) """

    return padre1, padre2


def cruce(poblacion, padre1, padre2):
    n = len(padre1)
    punto = random.randint(1, n - 1)

    hijo1 = padre1[:punto] + padre2[punto:]
    hijo2 = padre2[:punto] + padre1[punto:]

    poblacion.append(hijo1)
    poblacion.append(hijo2)

    return hijo1, hijo2


def mutacion(probabilidad_mutacion, hijo1, hijo2):
    vector_mutacion = [1] * int(probabilidad_mutacion * 100) + \
        [0] * (100 - int(probabilidad_mutacion * 100)
               )
    random.shuffle(vector_mutacion)
    mutar = random.choice(vector_mutacion)

    if mutar == 1:
        seleccionar_hijo = random.randint(1, 2)
        if seleccionar_hijo == 1:
            columna_mutacion = random.randint(0, len(hijo1) - 1)
            valor_original = hijo1[columna_mutacion]
            nuevo_valor = valor_original

            # Asegurar que el nuevo valor sea diferente al original
            while nuevo_valor == valor_original:
                nuevo_valor = random.randint(0, 1)

            hijo1[columna_mutacion] = nuevo_valor

            print("Hijo 1 mutado:", hijo1)

        else:
            columna_mutacion = random.randint(0, len(hijo2) - 1)
            valor_original = hijo2[columna_mutacion]
            nuevo_valor = valor_original

            # Asegurar que el nuevo valor sea diferente al original
            while nuevo_valor == valor_original:
                nuevo_valor = random.randint(0, 1)

            hijo2[columna_mutacion] = nuevo_valor

            print("Hijo 2 mutado:", hijo2)
    else:
        print("No muta ningun individuo")


def seleccionar_individuos(poblacion):
    individuo1 = random.choice(poblacion)
    poblacion.remove(individuo1)
    individuo2 = random.choice(poblacion)
    poblacion.remove(individuo2)


def detencion(poblacion):
    for individuo in poblacion:
        if iluminacion(individuo) > 50 and costo(individuo) >= 100 and costo(individuo) <= 160:
            return individuo
    return None


def mejor_individuo(poblacion):
    mejor_individuo = None
    mejor_iluminacion = 0

    for individuo in poblacion:
        iluminacion_total = iluminacion(individuo)
        if iluminacion_total > mejor_iluminacion:
            mejor_iluminacion = iluminacion_total
            mejor_individuo = individuo

    return mejor_individuo


switches = [
    {"iluminacion": 25, "costo": 120},
    {"iluminacion": 15, "costo": 30},
    {"iluminacion": 15, "costo": 30},
    {"iluminacion": 10, "costo": 25},
    {"iluminacion": 25, "costo": 60},
    {"iluminacion": 50, "costo": 350}
]


def iluminacion_maxima():
    return sum(switch["iluminacion"] for switch in switches)


def costo_maximo():
    return sum(switch["costo"] for switch in switches)


def iluminacion(individuo):
    iluminacion_total = 0
    for i, bit in enumerate(individuo):
        if bit == 1:  # Si el switch está encendido
            iluminacion_total += switches[i]["iluminacion"]

    return iluminacion_total


def costo(individuo):
    costo_total = 0
    for i, bit in enumerate(individuo):
        if bit == 1:  # Si el switch está encendido
            costo_total += switches[i]["costo"]

    return costo_total


def calcular_iluminacion_y_costo(individuo, switches):
    iluminacion_total = 0
    costo_total = 0

    for i, bit in enumerate(individuo):
        if bit == 1:  # Si el switch está encendido
            iluminacion_total += switches[i]["iluminacion"]
            costo_total += switches[i]["costo"]

    return iluminacion_total, costo_total


def genetico(generaciones, probabilidad_mutacion, poblacion):
    i = 0
    while i <= generaciones:
        print("\t -> Generación:", i)
        if poblacion:
            print("Población:", len(poblacion))

            # print("\nSelección de Padres")
            padre1, padre2 = seleccionar_padres(poblacion)
            # print("\tPadres:", padre1, padre2)

            # print("\nCruce")
            hijo1, hijo2 = cruce(poblacion, padre1, padre2)
            # print("Hijos:", hijo1, hijo2)

            # print("\nMutación")
            mutacion(probabilidad_mutacion, hijo1, hijo2)

            # print("\nSelección de Individuos")
            seleccionar_individuos(poblacion)

            # print("\nDetención")
            solucion = detencion(poblacion)

            if solucion:
                print("Solución encontrada:", solucion)
                break
            else:
                print("No se encontró ninguna solución")

            print("\nMejor Individuo")
            mejor = mejor_individuo(poblacion)
            if mejor:
                print(mejor)
        i += 1


poblacion = poblacion_inicial(10)
generaciones = 10
probabilidad_mutacion = 0.25
genetico(generaciones, probabilidad_mutacion, poblacion)
