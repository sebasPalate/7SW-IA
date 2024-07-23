import pandas as pd


def aprender_regla(clase, ejemplos, atributos):
    # Seleccionar los ejemplos que pertenecen a la clase actual
    ejemplos_clase = [ejemplo for ejemplo in ejemplos if ejemplo[-1] == clase]

    # Crear una regla con el antecedente y el consecuente como la clase actual
    regla = {"antecedente": [], "consecuente": clase}

    # Crear una copia de la lista de atributos
    atributos_aux = atributos.copy()

    # Mientras la regla cubra algún ejemplo negativo y que los atributos sean diferentes de 0
    while cubre_ejemplos_negativos(regla, ejemplos_clase) and len(atributos_aux) != 0:
        restricciones = []

        for atributo in atributos_aux:
            # Para cada atributo no usado en la regla
            if atributo not in [r.keys()[0] for r in regla["antecedente"]]:
                # Para cada valor del atributo
                valores_atributo = set(
                    [ejemplo[atributos.index(atributo)] for ejemplo in ejemplos])

                for valor in valores_atributo:
                    # Crear una restricción
                    restriccion = {atributo: valor}
                    # Verificar si la restricción es única
                    if restriccion not in restricciones:
                        restricciones.append(restriccion)

        # Obtener la mejor restricción
        restriccion = mejor_restriccion(restricciones, regla)

        # Añadir restricción a la regla
        regla["antecedente"].append(restriccion)

    return regla


def cubre_ejemplos_negativos(regla, ejemplos_clase):
    # Verificar si la regla cubre todos los ejemplos negativos
    for ejemplo in ejemplos_clase:
        # Si la regla clasifica el ejemplo como positivo, la regla no cubre los ejemplos negativos
        if not clasifica_correctamente(regla, ejemplo):
            return False
    return True


def clasifica_correctamente(regla, ejemplo):
    # Verificar si la regla clasifica correctamente el ejemplo
    antecedente = regla["antecedente"]
    for restriccion in antecedente:
        for atributo, valor in restriccion.items():
            indice_atributo = atributos.index(atributo)
            if ejemplo[indice_atributo] != valor:
                return False
    return True


def mejor_restriccion(restricciones, regla):
    mejor_restriccion = None
    mejor_confianza = -1
    mejor_soporte = -1

    for restriccion in restricciones:
        # Convertir la restricción a una cadena
        restriccion_str = str(restriccion)

        if restriccion_str not in [str(r) for r in regla["antecedente"]]:

            confianza = calcular_confianza(regla, restriccion)
            soporte = calcular_soporte(regla, restriccion)
            lift = calcular_lift(regla, restriccion, confianza)

            print("\trestriccion: ", restriccion)
            print("\tconfianza: ", confianza)
            print("\tsoporte: ", soporte)
            print("\tlift: ", lift)

            # Verificar si la confianza es igual y el soporte es mayor
            if confianza == mejor_confianza and soporte > mejor_soporte:
                mejor_restriccion = restriccion
                mejor_confianza = confianza
                mejor_soporte = soporte
            # Si la confianza es mayor
            elif confianza > mejor_confianza:
                mejor_restriccion = restriccion
                mejor_confianza = confianza
                mejor_soporte = soporte

            print("\n")

    return mejor_restriccion


def calcular_confianza(regla, restriccion):
    # Construir la regla extendida
    regla_ext = regla.copy()
    regla_ext["antecedente"].append(restriccion)
    print("regla_ext confianza: ", regla_ext)

    # Contar el número de ejemplos que cumplen la regla extendida
    cumplen_regla = 0
    for ejemplo in ejemplos:
        for restriccion in regla_ext["antecedente"]:
            for attr, val in restriccion.items():
                # Obtener el índice del atributo en los atributos
                indice_atributo = atributos.index(attr)
                # Verificar si cumple con la regla extendida
                if ejemplo[indice_atributo] == val and ejemplo[-1] == regla_ext["consecuente"]:
                    cumplen_regla += 1

    # Contar el número de ejemplos que cumplen el antecedente
    cumplen_antecedente = 0
    for ejemplo in ejemplos:
        for restriccion in regla["antecedente"]:
            for attr, val in restriccion.items():
                # Obtener el índice del atributo en los atributos
                indice_atributo = atributos.index(attr)
                # Verificar si cumple con el antecedente
                if ejemplo[indice_atributo] == val:
                    cumplen_antecedente += 1

    # Calcular confienza
    confianza = cumplen_regla / cumplen_antecedente if cumplen_antecedente > 0 else 0

    return confianza


def calcular_soporte(regla, restriccion):
    # Construir la regla extendida
    regla_ext = regla.copy()
    regla_ext["antecedente"].append(restriccion)
    # print("regla_ext: ", regla_ext)

    # Contar el número de ejemplos que cumplen la regla extendida
    cumplen_regla = 0
    for ejemplo in ejemplos:
        for restriccion in regla_ext["antecedente"]:
            for attr, val in restriccion.items():
                # Obtener el índice del atributo en los atributos
                indice_atributo = atributos.index(attr)
                # Verificar si cumple con la regla extendida
                if ejemplo[indice_atributo] == val and ejemplo[-1] == regla_ext["consecuente"]:
                    cumplen_regla += 1

    # Contar el numero total de ejemplos
    total_ejemplos = len(ejemplos)

    # Calcular soporte
    soporte = cumplen_regla / total_ejemplos if total_ejemplos > 0 else 0

    return soporte


def calcular_lift(regla, restriccion, confianza):

    # Construir la regla extendida
    regla_ext = regla.copy()
    regla_ext["antecedente"].append(restriccion)
    # print("regla_ext: ", regla_ext)

    # Calcular la probabilidad de que se cumpla el consecuente
    prob_consecuente = 0
    for ejemplo in ejemplos:
        if ejemplo[-1] == regla["consecuente"]:
            prob_consecuente += 1

    lift = confianza / prob_consecuente if prob_consecuente > 0 else 0
    return lift


def cumple_restriccion(restriccion, ejemplo):
    # Iterar sobre los elementos de la restricción
    for atributo, valor in restriccion.items():
        # Verificar si el valor del atributo en el ejemplo coincide con el valor de la restricción
        if ejemplo[atributos.index(atributo)] != valor:
            # Si no coincide, el ejemplo no cumple con la restricción, por lo que retornamos False
            return False
    # Si se cumple la restricción para todos los atributos, retornamos True
    return True


def recubrimiento_secuencial(clases, atributos, ejemplos):
    reglas = []
    for clase in clases:
        regla = aprender_regla(clase, ejemplos, atributos)
        reglas.append(regla)
        break


# Leer el dataset
df = pd.read_csv('dataset/RespuestasFormLimpio.csv', sep=';', encoding='utf-8')

# Obtener los atributos (cabecera del dataset)
atributos = df.columns.tolist()

# Obtener las clases únicas
clases = df['carrera'].unique().tolist()

# Dataset, sin la cabecera
ejemplos = df.values.tolist()

# Ejecutar el algoritmo de recubrimiento secuencial
resultado = recubrimiento_secuencial(clases, atributos, ejemplos)
