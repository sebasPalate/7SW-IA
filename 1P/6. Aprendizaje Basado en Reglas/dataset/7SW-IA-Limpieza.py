from sklearn.impute import SimpleImputer
import pandas as pd


def imputar_nulos(df):
    # Identificar columnas con valores nulos
    columnas_con_nulos = df.columns[df.isnull().any()]

    # Crear un imputador con la estrategia de imputación más frecuente
    imputer = SimpleImputer(strategy='most_frequent')

    # Imputar valores nulos en las columnas identificadas
    df[columnas_con_nulos] = imputer.fit_transform(df[columnas_con_nulos])

    return df


def dividir_columna(df, columna, nuevo_nombre_columna, separador):
    # Crear una lista para almacenar las nuevas filas
    nuevas_filas = []

    # Iterar sobre las filas del DataFrame
    for index, fila in df.iterrows():
        # Dividir la columna por el separador
        elementos = [elemento.strip()
                     for elemento in fila[columna].split(separador)]

        # Crear una fila para cada elemento
        for elemento in elementos:
            nueva_fila = fila.copy()
            nueva_fila[nuevo_nombre_columna] = elemento  # Renombrar columna
            nuevas_filas.append(nueva_fila)

    # Concatenar las nuevas filas al DataFrame original
    df_extendido = pd.DataFrame(nuevas_filas)

    # Reordenar las columnas para mantener el orden original
    columnas = list(df.columns)
    columnas.insert(columnas.index(columna), nuevo_nombre_columna)
    df_extendido = df_extendido[columnas]

    # Eliminar la columna original si no es la misma que la nueva
    if nuevo_nombre_columna != columna:
        del df_extendido[columna]

    return df_extendido


# Leer el dataset
df = pd.read_csv('dataset/RespuestasForm.csv', sep=";", encoding='utf-8')

# Excluir las tres primeras columnas
df = df.iloc[:, 3:]

# Imputar valores nulos (completar los valores nulos con la moda)
df = imputar_nulos(df)

""" INICIO DE UNIR LAS "CARRERAS_SELECCIONADAS" CON "OTRAS_CARRERAS" A "CARRERAS" """
# Crear una lista para almacenar las nuevas filas
nuevas_filas = []

# Iterar sobre las filas del DataFrame
for index, fila in df.iterrows():
    # Dividir la columna "seleccion_carrera" por la coma
    carreras_seleccionadas = [carrera.strip()
                              for carrera in fila["seleccion_carrera"].split(",")]

    # Crear una fila para cada carrera seleccionada
    for carrera in carreras_seleccionadas:
        nueva_fila = fila.copy()
        nueva_fila["carreras"] = carrera
        nuevas_filas.append(nueva_fila)

    # Agregar otra carrera si está presente
    otra_carrera = fila["otra_carrera"]
    if otra_carrera.strip():  # Verificar si hay algo en la otra carrera
        nueva_fila = fila.copy()
        nueva_fila["carreras"] = otra_carrera.strip()
        nuevas_filas.append(nueva_fila)

# Concatenar las nuevas filas al DataFrame original
df_extendido = pd.DataFrame(nuevas_filas)

# Eliminar las columnas "seleccion_carrera" y "otra_carrera" originales
df_extendido.drop(columns=["seleccion_carrera", "otra_carrera"], inplace=True)

""" FIN DE UNIR LAS "CARRERAS_SELECCIONADAS" CON "OTRAS_CARRERAS" A "CARRERAS" """


# Convertir todas las columnas a mayúsculas
df_extendido = df_extendido.applymap(
    lambda x: x.upper() if isinstance(x, str) else x)

# Reemplazar valores repetidos (sucios) en la columna "colegio_actua"
reemplazos = {
    'UNIDAD EDUCATIVA "AMBATO"': "UNIDAD EDUCATIVA AMBATO",  # con comillas
    'UNIDAD EDUCATIVA "AMBATO "': "UNIDAD EDUCATIVA AMBATO",  # con comillas especiales
    'UNIDAD EDUCATIVA “AMBATO”': "UNIDAD EDUCATIVA AMBATO",  # con comillas especiales
    'UNIDAD EDUCATIVA "AMBATO" ': "UNIDAD EDUCATIVA AMBATO",
    'UNIDAD EDUCATIVA " AMBATO "': "UNIDAD EDUCATIVA AMBATO",
    'UNIDAD EDUCATIVA AMBATO ': "UNIDAD EDUCATIVA AMBATO",  # con espacio en blanco
    'AMBATO': "UNIDAD EDUCATIVA AMBATO",  # nombre unico
    'AMBATO ': "UNIDAD EDUCATIVA AMBATO",  # nombre unico con espacio en blanco
    'UNIDAD. EDUCATIVA. AMBATO': "UNIDAD EDUCATIVA AMBATO",
    'U NIDADA EDUCATIVA AMBATO': "UNIDAD EDUCATIVA AMBATO",

    'UNIDAD EDUCATIVA "GUAYAQUIL"': "UNIDAD EDUCATIVA GUAYAQUIL",  # con comillas
    'UNIDAD EDUCATIVA GUAYAQUIL ': "UNIDAD EDUCATIVA GUAYAQUIL",  # con espacio en blanco
    'GUAYAQUIL': "UNIDAD EDUCATIVA GUAYAQUIL",  # nombre unico
    'GUAYAQUIL ': "UNIDAD EDUCATIVA GUAYAQUIL",
    'U E GUAYAQUIL ': "UNIDAD EDUCATIVA GUAYAQUIL",
    'U.E GUAYAQUIL ': "UNIDAD EDUCATIVA GUAYAQUIL",
    "UNIDAD EDUCATIVA 'GUAYAQUIL' ": "UNIDAD EDUCATIVA GUAYAQUIL",  # con comillas simples
    'UNIDAS EDUCATIVA GUAYAQUIL ': "UNIDAD EDUCATIVA GUAYAQUIL",

    'MARIO COBO BARONA': "UNIDAD EDUCATIVA MARIO COBO BARONA",
    'UNIDAD EDUCATIVA "MARIO COBO BARONA"': "UNIDAD EDUCATIVA MARIO COBO BARONA",
    'U.E MARIO COBO': "UNIDAD EDUCATIVA MARIO COBO BARONA",
    'U.E. MARIO COBO BARONA': "UNIDAD EDUCATIVA MARIO COBO BARONA",
    'UNIDAD EDUCATIVA"MARIO COBO BARONA"': "UNIDAD EDUCATIVA MARIO COBO BARONA",
    'UNIDAD EDUCATIVA  MARIO COBO BARONA': "UNIDAD EDUCATIVA MARIO COBO BARONA",
    '"UNIDAD EDUCATIVA MARIO COBO BARONA"': "UNIDAD EDUCATIVA MARIO COBO BARONA",
    'MARIO COBO BARONA ': "UNIDAD EDUCATIVA MARIO COBO BARONA",
    'MARICO COBO BARONA': "UNIDAD EDUCATIVA MARIO COBO BARONA",
    'UNIDAD EDUCATIVA MARIO COBO BARONA ': "UNIDAD EDUCATIVA MARIO COBO BARONA",
    'Y.E "MARIO COBO BARONA"': "UNIDAD EDUCATIVA MARIO COBO BARONA",
    'MARIO COBOS BARONA': "UNIDAD EDUCATIVA MARIO COBO BARONA",
    'MARIO COBOS BARONA ': "UNIDAD EDUCATIVA MARIO COBO BARONA",
    'U.E "MARIO COBO BARONA"': "UNIDAD EDUCATIVA MARIO COBO BARONA",

    'MARIO COBO BARONAS ': "UNIDAD EDUCATIVA MARIO COBO BARONA",
    'UNIDAD EDUCATIVA MARIO COBO BARONA  ': "UNIDAD EDUCATIVA MARIO COBO BARONA",
    'U.E MARIO COBO BARONA': "UNIDAD EDUCATIVA MARIO COBO BARONA",
    'MARIO COBO NBARONA': "UNIDAD EDUCATIVA MARIO COBO BARONA",
    'MARIO  COBO  BARONA ': "UNIDAD EDUCATIVA MARIO COBO BARONA",
    'MARIO COBO BARAONA': "UNIDAD EDUCATIVA MARIO COBO BARONA",
}

# Reemplazar los valores en la columna "colegio_actua"
df_extendido["colegio_actua"] = df_extendido["colegio_actua"].replace(
    reemplazos)

# Dividir la columna "factor_carrera" por el separador
df_extendido = dividir_columna(
    df_extendido, "factores_carrera", "factor_carrera", ",")

# Dividir la columna "carreras" por el separador
df_extendido = dividir_columna(df_extendido, "carreras", "carrera", ",")

# Reemplazar valores en la columna "carrera"
reemplazos = {
    'ROBOTICA': 'AUTOMATIZACIÓN Y ROBÓTICA',

    'PROGRAMACION': 'PROGRAMACIÓN E INFORMÁTICA',
    'INFORMATICA ': 'PROGRAMACIÓN E INFORMÁTICA',

    'INGENIERO EN SISTEMAS': 'INGENIERÍA EN SISTEMAS',

    'DISEÑO EN SOFWARE': 'INGENIERÍA DE SOFTWARE',
    'SOFTWARE': 'INGENIERÍA DE SOFTWARE',

    'TECNOLOGÍAS DE LA INFORMACIÓN': 'INGENIERÍA EN TECNOLOGÍAS DE LA INFORMACIÓN',
    'TECNOLOGIAS': 'INGENIERÍA EN TECNOLOGÍAS DE LA INFORMACIÓN',


    'INGENIERÍA AUTOMOTRIZ': 'INGENIERÍA AUTOMOTRIZ',
    'INGENIERÍA AUTOMOTRIS': 'INGENIERÍA AUTOMOTRIZ',
    'MECÁNICA AUTOMOTRIZ': 'INGENIERÍA AUTOMOTRIZ',
    'TECNOLÓGICO AUTOMOTRIZ': 'INGENIERÍA AUTOMOTRIZ',

    'INGENIERO MECÁNICO': 'INGENIERÍA MECÁNICA',
    'MECANICA': 'INGENIERÍA MECÁNICA',

    'LA MECATRONICA': "INGENIERÍA MECATRÓNICA",
    'MECATRONICA': "INGENIERÍA MECATRÓNICA",
    'MECATRÓNICA': "INGENIERÍA MECATRÓNICA",

    'ODONTOLOGIA': 'ODONTOLOGÍA',

    'ECONOMIA O ALGO CON FINANZAS': 'ECONOMÍA Y FINANZAS',
    'ADMINISTRACION': 'ADMINISTRACIÓN DE EMPRESAS',

    'JURISPRUDENCIA': 'DERECHO Y JUSTICIA',
    'DERECHO Y CRIMINALISTICA': 'DERECHO Y JUSTICIA',
    'CRIMINALISTICA': 'CRIMINOLOGÍA/CRIMINALÍSTICA',
    'CRIMINOLOGÍA/CRIMINALÍSTICA': 'CRIMINOLOGÍA/CRIMINALÍSTICA',
    'CRIMINOLOGIA/CRIMINALISTICA': 'CRIMINOLOGÍA/CRIMINALÍSTICA',

    'ARTES AUDIOVISUALES': 'ARTE Y DISEÑO',
    'FOTOGRAFIA Y DISEÑO': 'ARTE Y DISEÑO',
    'DISENO DE MODAS': 'ARTE Y DISEÑO',
    'DISEÑO DIGITAL': 'ARTE Y DISEÑO',
    'ARTE': 'ARTE Y DISEÑO',

    'MARKETING': 'MARKETING Y PUBLICIDAD',
    'MARKETING DIGITAL': 'MARKETING Y PUBLICIDAD',

    'DISEÑO GRÁFICO': 'DISEÑO GRAFICO',
    'DISEÑADOR GRAFICO': 'DISEÑO GRAFICO',

    'INGENIERIA CIVIL': 'INGENIERÍA CIVIL',

    'NINGUNA': 'NINGUNA',
    'NOSE': 'NINGUNA',
    'VGRHDG': 'NINGUNA',
    'NO': 'NINGUNA',
}

# Reemplazar los valores en la columna "carreras"
df_extendido["carrera"] = df_extendido["carrera"].replace(reemplazos)


# Guardar el nuevo DataFrame en un nuevo archivo CSV
df_extendido.to_csv('dataset/RespuestasFormLimpio.csv', sep=";",
                    encoding='utf-8', index=False)
