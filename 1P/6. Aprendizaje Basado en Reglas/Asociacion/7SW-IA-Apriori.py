import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd

# Variable global para mantener la instancia de la ventana principal
ventana_principal = None


class VentanaSeleccion(tk.Toplevel):
    def __init__(self, master, caracteristicas_seleccionadas, dataset, lb_caracteristicas):
        super().__init__(master)
        self.caracteristicas_seleccionadas = caracteristicas_seleccionadas
        self.dataset = dataset
        # Mantener la referencia a lb_caracteristicas
        self.lb_caracteristicas = lb_caracteristicas

        self.title("Características Seleccionadas")

        self.label = tk.Label(self, text="Complete el formulario:")
        self.label.pack()

        self.comboboxes = {}

        for caracteristica in self.caracteristicas_seleccionadas:
            opciones_unicas = self.obtener_opciones_unicas(caracteristica)
            if opciones_unicas:
                frame = tk.Frame(self)
                frame.pack()

                tk.Label(frame, text=caracteristica).pack(side=tk.LEFT)
                combo = ttk.Combobox(frame, values=opciones_unicas)
                combo.pack(side=tk.LEFT)
                self.comboboxes[caracteristica] = combo

        self.btn_guardar = tk.Button(
            self, text="Calcular", command=self.mostrar_salida)
        self.btn_guardar.pack()

        self.btn_regresar = tk.Button(
            self, text="Regresar a la selección de características", command=self.regresar_seleccion_caracteristicas)
        self.btn_regresar.pack()

    def regresar_seleccion_caracteristicas(self):
        self.destroy()  # Cierra la ventana actual
        ventana_principal.deiconify()  # Vuelve a mostrar la ventana principal

    def obtener_opciones_unicas(self, caracteristica):
        return self.dataset[caracteristica.lower().replace(" ", "_")].unique().tolist()

    def guardar_formulario(self):
        datos_formulario = {caracteristica: combo.get()
                            for caracteristica, combo in self.comboboxes.items()}
        print("Datos del formulario:", datos_formulario)

    def calcular_confianza(self, datos_formulario, df_filtrado, caracteristicas, df):
        # Total de observaciones que cumplen con todas las características seleccionadas y la clase seleccionada
        total = len(df_filtrado)

        # Datos del formulario sin la clase
        datos_formulario_sin_clase = datos_formulario.copy()
        datos_formulario_sin_clase.pop(caracteristicas[-1])

        df_aux = df.copy()
        for caracteristica, valor in datos_formulario_sin_clase.items():
            df_aux = df_aux[df_aux[caracteristica.lower().replace(
                " ", "_")] == valor]

        confianza = 0 if df_aux.shape[0] == 0 else total / df_aux.shape[0]
        return confianza

    def calcular_soporte(self, df, datos_formulario):
        # Filtrar el DataFrame con las características seleccionadas
        df_filtrado = df
        for caracteristica, valor in datos_formulario.items():
            df_filtrado = df_filtrado[df_filtrado[caracteristica.lower().replace(
                " ", "_")] == valor]
        # Calcular el soporte
        soporte = 0 if len(df) == 0 else len(df_filtrado) / len(df)
        return soporte, df_filtrado

    def calcular_lift(self, confianza, df, datos_formulario, caracteristicas):
        # Calcular el lift
        # Lift=(confianza)/(probabilidad de que ocurra la clase)
        # Probabilidad de que ocurra la clase = total de observaciones que cumplen con la clase seleccionada
        probabilidad_clase = len(df[df[df.columns[-1].lower().replace(" ", "_")]
                                 == datos_formulario[caracteristicas[-1]]]) / len(df)
        lift = 0 if probabilidad_clase == 0 else confianza / probabilidad_clase
        return lift

    def mostrar_salida(self):
        df = pd.read_csv('dataset/RespuestasFormLimpio.csv', sep=';', encoding='utf-8')
        caracteristicas = self.caracteristicas_seleccionadas
        datos_formulario = {caracteristica: combo.get()
                            for caracteristica, combo in self.comboboxes.items()}

        # Calcular la soporte
        soporte, df_filtrado = self.calcular_soporte(df, datos_formulario)

        # Calcular la confianza
        confianza = self.calcular_confianza(
            datos_formulario, df_filtrado, caracteristicas, df)

        # Calcular el lift
        lift = self.calcular_lift(
            confianza, df, datos_formulario, caracteristicas)

        # Mostrar los resultados
        tk.messagebox.showinfo(
            "Resultados", f"Confianza: {round(confianza*100,2)}%\nSoporte: {round(soporte*100,2)}%\nLift: {round(lift,4)}")


def seleccionar_caracteristicas(caracteristicas_disponibles, clase, dataset):
    global ventana_principal  # Utiliza la variable global
    ventana_principal = tk.Tk()
    ventana_principal.title("Seleccionar Características")

    lb_caracteristicas = []
    for caracteristica in caracteristicas_disponibles:
        var = tk.IntVar()
        chk = tk.Checkbutton(
            ventana_principal, text=caracteristica, variable=var)
        lb_caracteristicas.append((var, caracteristica))
        chk.pack()

    # Marcar la clase por defecto para que no se pueda deseleccionar
    var_clase = tk.IntVar()
    chk_clase = tk.Checkbutton(
        ventana_principal, text=clase, variable=var_clase, state=tk.DISABLED)
    lb_caracteristicas.append((var_clase, clase))
    chk_clase.select()
    chk_clase.pack()

    btn_seleccionar = tk.Button(ventana_principal, text="Seleccionar",
                                command=lambda: abrir_ventana_resultados(lb_caracteristicas, dataset))
    btn_seleccionar.pack()

    ventana_principal.mainloop()


def abrir_ventana_resultados(lb_caracteristicas, dataset):
    global ventana_principal  # Utiliza la variable global
    ventana_principal.withdraw()  # Oculta la ventana principal
    caracteristicas_seleccionadas = [
        caracteristica for var, caracteristica in lb_caracteristicas if var.get()]

    clases_seleccionadas = [caracteristica for var, caracteristica in lb_caracteristicas if var.get(
    ) and caracteristica != "CARRERA"]

    # Filtrar las características seleccionadas para que no se incluya la clase
    if not clases_seleccionadas:
        advertencia = tk.messagebox.showwarning(
            "Advertencia", "Por favor, seleccione al menos una característica aparte de la clase.", parent=ventana_principal)
        if advertencia == "ok":
            ventana_principal.deiconify()  # Vuelve a mostrar la ventana principal
            return
    else:
        VentanaSeleccion(
            ventana_principal, caracteristicas_seleccionadas, dataset, lb_caracteristicas)


def main():
    # Cargar el archivo CSV en un DataFrame
    df = pd.read_csv('dataset/RespuestasFormLimpio.csv', sep=';', encoding='utf-8')
    # Obtener el vector de características disponibles excluyendo la columna de etiquetas
    caracteristicas_disponibles = df.columns[:-1].tolist()
    # Remplazar el "_" con un " " en caracteristicas_disponibles y convertir a mayúsculas
    caracteristicas_disponibles = [caracteristica.replace(
        "_", " ").upper() for caracteristica in caracteristicas_disponibles]
    clase = (df.columns[-1]).replace("_", " ").upper()
    seleccionar_caracteristicas(caracteristicas_disponibles, clase, df)


if __name__ == "__main__":
    main()

