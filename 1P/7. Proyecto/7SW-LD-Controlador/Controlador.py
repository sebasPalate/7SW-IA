import numpy as np
from matplotlib import pyplot as plt
from fuzzy import *

# Definición de variables de entrada y rangos
error_maximo = 30
voltaje_maximo = 12

# Definir los rangos de las variables de entrada
error = np.linspace(-error_maximo, error_maximo, 100)
voltaje = np.linspace(-voltaje_maximo, voltaje_maximo, 100)

# Definir las funciones de membresía para el error
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
VPG = [trapmf, [voltaje_maximo/4, voltaje_maximo/2, voltaje_maximo, voltaje_maximo]]

# Definir las reglas difusas
ANT = [ENG, ENP, EZ, EPP, EPG]
CON = [VNG, VNP, VZ, VPP, VPG]

# Simulación
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
temperatura_actual = 0
temperatura_deseada = 25
potencia_c_r = 0

# Variables para graficar
tiempos = [tiempo_actual]
temperaturas = [temperatura_actual]
temperaturas_deseadas = [temperatura_deseada]

# Control de lazo cerrado
while tiempo_actual < tiempo_final:

    # Obtener la temperatura actual
    temperatura_actual = simular(potencia_c_r, temperaturas, intervalo)

    # Calcular el error
    error = temperatura_deseada - temperatura_actual

    # Controlador difuso
    res = fuzz(error, voltaje, ANT, CON)  # Funcion difusa

    # Defuzzificar
    out = defuzz(voltaje, res, 'centroid')
    potencia_c_r = out

    # Guardar los datos para graficar
    tiempo_actual += intervalo
    tiempos.append(tiempo_actual)
    temperaturas.append(temperatura_actual)
    temperaturas_deseadas.append(temperatura_deseada)

# Graficar
plt.figure()
plt.plot(tiempos, temperaturas, label='Temperatura actual')
plt.plot(tiempos, temperaturas_deseadas, 'r--', label='Temperatura deseada')
plt.xlabel('Tiempo')
plt.ylabel('Temperatura')
plt.legend()
plt.grid(True)
plt.title('Control de temperatura con lógica difusa')
plt.show()
