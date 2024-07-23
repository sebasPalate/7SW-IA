import pandas as pd

# Cargar el archivo csv
df = pd.read_csv('test.csv')

# Establecer 'PassengerId' como índice
df.set_index('PassengerId', inplace=True)

# Seleccionar las columnas categóricas
categorical_cols = ['Pclass', 'Sex', 'Embarked']  

# Aplicar one-hot encoding a las columnas categóricas
df = pd.get_dummies(df[categorical_cols + ['Age', 'Survived']], columns=categorical_cols)

# Guardar el nuevo dataframe en un nuevo archivo csv, manteniendo el índice
df.to_csv('test_one_hot.csv')