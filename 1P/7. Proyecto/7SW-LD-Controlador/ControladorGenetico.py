import random
import numpy as np
from matplotlib import pyplot as plt
from fuzzy import *


def simular_control_difuso(error_maximo, voltaje_maximo, metodo_defuzzificacion):
    # Definir los rangos de las variables de entrada
    error = np.linspace(-error_maximo, error_maximo, 100)
    voltaje = np.linspace(-voltaje_maximo, voltaje_maximo, 100)

    # Definir las funciones de membresía para el error y el voltaje (puedes ajustarlas si es necesario)
    ENG = [trapmf, [-error_maximo, -error_maximo, -error_maximo/2, -error_maximo/4]]
    ENP = [trimf, [-error_maximo/2, -error_maximo/4, 0]]
    EZ = [trimf, [-error_maximo/4, 0, error_maximo/4]]
    EPP = [trimf, [0, error_maximo/4, error_maximo/2]]
    EPG = [trapmf, [error_maximo/4, error_maximo/2, error_maximo, error_maximo]]

    # Definir las funciones de membresía para la resistencia/potencia
    VNG = [trapmf, [-voltaje_maximo, -voltaje_maximo, -
                    voltaje_maximo/2, -voltaje_maximo/4]]
    VNP = [trimf, [-voltaje_maximo/2, -voltaje_maximo/4, 0]]
    VZ = [trimf, [-voltaje_maximo/4, 0, voltaje_maximo/4]]
    VPP = [trimf, [0, voltaje_maximo/4, voltaje_maximo/2]]
    VPG = [trapmf, [voltaje_maximo/4, voltaje_maximo /
                    2, voltaje_maximo, voltaje_maximo]]

    # Definir las reglas difusas (puedes ajustarlas si es necesario)
    ANT = [ENG, ENP, EZ, EPP, EPG]
    CON = [VNG, VNP, VZ, VPP, VPG]

    # Simulación del sistema de control difuso
    def simular(voltaje, temperatura, dt):
        a = 0.1
        b = 25
        k = 2e3
        i = len(temperatura)
        nueva_temperatura = (dt**2*voltaje*k+((a+b)*dt+2) *
                             temperatura[i-1]-temperatura[i-2])/(a*b*dt**2+(a+b)*dt+1)
        return nueva_temperatura

    # Definir los parametros de simulacion
    tiempo_actual = 0
    tiempo_final = 10
    intervalo = 0.01

    # Definir las condiciones iniciales
    temperatura_actual = 15
    temperatura_deseada = 25
    potencia_c_r = 0

    # Variables para calcular el consumo energético
    consumo_energetico = 0

    # Control de lazo cerrado
    # Lista para almacenar las temperaturas registradas
    temperaturas = [temperatura_actual]
    while tiempo_actual < tiempo_final:

        # Obtener la temperatura actual
        temperatura_actual = simular(potencia_c_r, temperaturas, intervalo)

        # Calcular el error
        error = temperatura_deseada - temperatura_actual

        # Controlador difuso
        res = fuzz(error, voltaje, ANT, CON)  # Funcion difusa

        # Defuzzificar
        out = defuzz(voltaje, res, metodo_defuzzificacion)
        potencia_c_r = out

        # Calcular el consumo energético
        # Potencia * Tiempo
        consumo_energetico += abs(potencia_c_r * intervalo)

        # Guardar las temperaturas para calcular el tiempo de convergencia
        temperaturas.append(temperatura_actual)

        # Actualizar el tiempo
        tiempo_actual += intervalo

    # Aquí deberías implementar la lógica de simulación del sistema de control difuso
    # Recuerda que debes calcular el consumo energético total

    return consumo_energetico


# Definir rangos para cada parámetro
rango_error_maximo = [20, 50]
rango_voltaje_maximo = [10, 20]
metodos_defuzzificacion = ['centroid', 'bisector', 'MOM', 'SOM', 'LOM']


def generar_solucion():
    error_maximo = random.uniform(rango_error_maximo[0], rango_error_maximo[1])
    voltaje_maximo = random.uniform(
        rango_voltaje_maximo[0], rango_voltaje_maximo[1])
    metodo_defuzzificacion = random.choice(metodos_defuzzificacion)
    return error_maximo, voltaje_maximo, metodo_defuzzificacion


def poblacion_inicial(tamano_poblacion):
    return [generar_solucion() for _ in range(tamano_poblacion)]


""" def seleccion_por_ruleta(poblacion, resultados_evaluacion):
    # Obtener las puntuaciones de ajuste (en este caso, el consumo de energía)
    puntuaciones = [rendimiento for _, rendimiento in resultados_evaluacion]

    # Invertir las puntuaciones para que los individuos con menor rendimiento tengan una mayor probabilidad
    puntuaciones_invertidas = [1 / rendimiento for rendimiento in puntuaciones]

    # Normalizar las puntuaciones invertidas para que sumen 1
    total_puntuaciones = sum(puntuaciones_invertidas)
    puntuaciones_normalizadas = [
        puntuacion / total_puntuaciones for puntuacion in puntuaciones_invertidas]

    # Seleccionar un individuo utilizando la ruleta
    indice_seleccionado = np.random.choice(
        len(poblacion), p=puntuaciones_normalizadas)
    return poblacion[indice_seleccionado] """


def seleccion_por_ruleta(poblacion, resultados_evaluacion):
    # Obtener las puntuaciones de ajuste (en este caso, el consumo de energía)
    puntuaciones = [rendimiento for _, rendimiento in resultados_evaluacion]

    # Calcular las probabilidades de selección en función de las puntuaciones de ajuste
    total_puntuaciones = sum(puntuaciones)
    probabilidades_seleccion = [
        puntuacion / total_puntuaciones for puntuacion in puntuaciones]

    # Seleccionar un individuo aleatoriamente basado en las probabilidades de selección
    indice_seleccionado = np.random.choice(
        len(poblacion), p=probabilidades_seleccion)
    if indice_seleccionado == len(poblacion):
        indice_seleccionado -= 1
        
    individuo_seleccionado = poblacion[indice_seleccionado]

    return individuo_seleccionado


def seleccion_de_padres_por_ruleta(poblacion, resultados_evaluacion, num_padres):
    # Seleccionar padres utilizando el método de selección por ruleta
    padres_seleccionados = []
    while len(padres_seleccionados) < num_padres:
        padre = seleccion_por_ruleta(poblacion, resultados_evaluacion)
        # Asegurar que el padre seleccionado no esté ya en la lista de padres seleccionados
        if padre not in padres_seleccionados:
            padres_seleccionados.append(padre)
    return padres_seleccionados


def cruce_en_un_punto(padre1, padre2):
    # Elegir un punto de corte aleatorio
    punto_de_corte = random.randint(1, len(padre1) - 1)

    # Generar los descendientes intercambiando las porciones de los padres a cada lado del punto de corte
    hijo1 = padre1[:punto_de_corte] + padre2[punto_de_corte:]
    hijo2 = padre2[:punto_de_corte] + padre1[punto_de_corte:]

    return hijo1, hijo2


def mutacion(hijo1, hijo2, probabilidad_mutacion, metodos_defuzzificacion):
    # Evaluar si se debe aplicar la mutación
    if random.random() < probabilidad_mutacion:
        # Seleccionar aleatoriamente uno de los dos hijos
        hijo_seleccionado = hijo1 if random.random() < 0.5 else hijo2
        print("Hijo seleccionado para mutación:", hijo_seleccionado)

        # Convertir el hijo seleccionado en una lista mutable
        hijo_mutado = list(hijo_seleccionado)

        # Seleccionar aleatoriamente que parametro mutar
        parametro_mutado = random.randint(0, 2)
        print("Parámetro mutado:", parametro_mutado)

        if parametro_mutado == 0:
            # Mutar el error máximo
            hijo_mutado[parametro_mutado] = random.uniform(
                rango_error_maximo[0], rango_error_maximo[1])

        elif parametro_mutado == 1:
            # Mutar el voltaje máximo
            hijo_mutado[parametro_mutado] = random.uniform(
                rango_voltaje_maximo[0], rango_voltaje_maximo[1])

        else:
            # Mutar el método de defusificación
            hijo_mutado[parametro_mutado] = random.choice(
                metodos_defuzzificacion)

        # Devolver el hijo mutado como una tupla
        hijo_mutado = tuple(hijo_mutado)
        if hijo_seleccionado == hijo1:
            hijo1 = hijo_mutado
        else:
            hijo2 = hijo_mutado
    else:
        print("No se aplicó la mutación")


def detener(poblacion):
    for individuo in poblacion:
        error_maximo, voltaje_maximo, metodo_defuzzificacion = individuo
        rendimiento = simular_control_difuso(
            error_maximo, voltaje_maximo, metodo_defuzzificacion)
        if rendimiento <= 0.5:
            return individuo
    return None


def mejor_individuo(poblacion):
    mejor_individuo = None
    mejor_rendimiento = 0
    for individuo in poblacion:
        error_maximo, voltaje_maximo, metodo_defuzzificacion = individuo
        rendimiento = simular_control_difuso(
            error_maximo, voltaje_maximo, metodo_defuzzificacion)
        if rendimiento > mejor_rendimiento:
            mejor_rendimiento = rendimiento
            mejor_individuo = individuo
    return mejor_individuo


def genetico(generaciones, probabilidad_mutacion, poblacion):
    i = 0
    while i < generaciones:
        print("\n\t -> Generación:", i)
        if poblacion:

            # Evaluación de cada solución
            resultados_evaluacion = [(solucion, simular_control_difuso(
                solucion[0], solucion[1], solucion[2])) for solucion in poblacion]

            # Mostrar los resultados de la evaluación
            for solucion, rendimiento in resultados_evaluacion:
                print("Solución:", solucion)
                print("Rendimiento:", rendimiento)
                print()

            # Seleccion de padres
            padres = seleccion_de_padres_por_ruleta(
                poblacion, resultados_evaluacion, 2)

            # Cruzamiento de los padres
            hijo1, hijo2 = cruce_en_un_punto(padres[0], padres[1])

            # Mutación de un individuo
            mutacion(
                hijo1, hijo2, probabilidad_mutacion, metodos_defuzzificacion)

            # Seleccionar individuos
            individuo1 = random.choice(poblacion)
            poblacion.remove(individuo1)
            individuo2 = random.choice(poblacion)
            poblacion.remove(individuo2)

            # Detener
            solucion = detener(poblacion)

            if solucion is not None:
                print("Se encontró una solución:")
                print(solucion)
                break

            # Mejor individuo
            mejor = mejor_individuo(poblacion)
            if mejor is not None:
                print("Mejor individuo de la generacion", i, ":")
                print(mejor)
        i += 1


# Parametros del algoritmo genético
poblacion = poblacion_inicial(5)
generaciones = 5
probabilidad_mutacion = 0.25
genetico(generaciones, probabilidad_mutacion, poblacion)
