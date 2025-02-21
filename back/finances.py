# Importar las bibliotecas necesarias
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Definir la clase Finance
class Finance:
    # Método de inicialización de la clase
    def __init__(self, df):
        # Almacenar el DataFrame original en la instancia
        self.df = df

        # Crear un nuevo DataFrame que excluya las filas donde 'type' es 'Ingreso'
        negative_totals_df = df[df['type'] != 'Ingreso'].copy()

        # Convertir los valores de la columna 'total' a negativos para representar gastos
        negative_totals_df['total'] = -negative_totals_df['total']

        # Almacenar el DataFrame modificado en la instancia
        self.outcomes = negative_totals_df

    # Método para obtener el DataFrame original
    def get_df(self):
        return self.df

    # Método para agregar una nueva fila al DataFrame
    def add_row(self, new_row):
        # Verificar que la nueva fila tenga el mismo número de elementos que las columnas del DataFrame
        if len(new_row) != len(self.df.columns):
            raise ValueError("The new row must have the same number of elements as the DataFrame columns.")

        # Validar y convertir los datos de la nueva fila
        for i, col in enumerate(self.df.columns):
            if col == 'date':  # Validar y convertir la fecha
                try:
                    pd.to_datetime(new_row[i], format='%d-%m-%Y')
                except ValueError:
                    raise ValueError(f"Invalid date format for column 'date'. Expected dd-mm-yyyy, got {new_row[i]}")
                new_row[i] = pd.to_datetime(new_row[i], format='%d-%m-%Y')
            elif col == 'type':  # Validar el tipo (debe ser 'Purchase' o 'Sale')
                if new_row[i] not in ['Purchase', 'Sale']:
                    raise ValueError(f"Invalid category for column 'type'. Expected 'Purchase' or 'Sale', got {new_row[i]}")
            else:  # Validar que el tipo de dato coincida con el de la columna correspondiente
                if not isinstance(new_row[i], type(self.df[col].iloc[0])):
                    try:
                        new_row[i] = type(self.df[col].iloc[0])(new_row[i])
                    except (ValueError, TypeError):
                        raise ValueError(f"Data type mismatch for column '{col}'. Expected {type(self.df[col].iloc[0])}, got {type(new_row[i])}")

        # Crear un nuevo DataFrame con la fila agregada
        new_df = pd.DataFrame([new_row], columns=self.df.columns)

        # Convertir la columna 'date' al formato de fecha correcto
        new_df['date'] = pd.to_datetime(new_df['date'], format='%d-%m-%Y').astype('datetime64[ns]')

        # Convertir la columna 'type' a tipo categórico
        new_df['type'] = new_df['type'].astype('category')

        # Concatenar el nuevo DataFrame con el original
        self.df = pd.concat([self.df, new_df], ignore_index=True)

    # Método para editar una fila existente en el DataFrame
    def edit_row(self, row_id, column_name, new_value):
        # Validar que el row_id sea un índice válido
        if not isinstance(row_id, int) or row_id < 0 or row_id >= len(self.df):
            print("Invalid row_id")
            return

        # Validar que el nombre de la columna exista en el DataFrame
        if column_name not in self.df.columns:
            print("Invalid column_name")
            return

        # Validar y convertir el nuevo valor según la columna
        if column_name == 'date':  # Validar y convertir la fecha
            try:
                pd.to_datetime(new_value, format='%d-%m-%Y')
            except ValueError:
                print(f"Invalid date format for column 'date'. Expected dd-mm-yyyy, got {new_value}")
                return
            new_value = pd.to_datetime(new_value, format='%d-%m-%Y')
        elif column_name == 'type':  # Validar el tipo (debe ser 'Purchase' o 'Sale')
            if new_value not in ['Purchase', 'Sale']:
                print(f"Invalid category for column 'type'. Expected 'Purchase' or 'Sale', got {new_value}")
                return
        else:  # Validar que el tipo de dato coincida con el de la columna correspondiente
            if not isinstance(new_value, type(self.df[column_name].iloc[0])):
                try:
                    new_value = type(self.df[column_name].iloc[0])(new_value)
                except (ValueError, TypeError):
                    print(f"Data type mismatch for column '{column_name}'. Expected {type(self.df[column_name].iloc[0])}, got {type(new_value)}")
                    return

        # Actualizar el valor en el DataFrame
        self.df.loc[row_id, column_name] = new_value

    # Método para generar un gráfico de pastel de los gastos por tipo
    def pieplot(self):
        # Agrupar los gastos por tipo y calcular la suma total de cada tipo
        type_totals = self.outcomes.groupby('type', observed=False)['total'].sum()

        # Eliminar la categoría 'Ingreso' (si existe)
        type_totals = type_totals.drop('Ingreso', errors='ignore')

        # Definir una paleta de colores para el gráfico
        palette_color = sns.color_palette('dark')

        # Calcular los porcentajes de cada tipo de gasto
        percentages = (type_totals / type_totals.sum()) * 100

        # Crear el gráfico de pastel
        wedges, texts = plt.pie(type_totals, colors=palette_color, textprops={'fontsize': 10})

        # Crear etiquetas para la leyenda
        legend_labels = [f'{label}' for label in type_totals.index]

        # Añadir la leyenda al gráfico
        plt.legend(wedges, legend_labels, loc="lower right")

        # Calcular la suma total de los gastos
        total_sum = type_totals.sum()

        # Mostrar el gráfico
        plt.show()

        # Limpiar la figura para evitar superposiciones en futuros gráficos
        plt.clf()

        # Devolver los totales y porcentajes en un DataFrame
        type_totals = pd.DataFrame({'total': type_totals, 'percentage': percentages})
        return type_totals, total_sum

    # Método para generar un gráfico de barras de los gastos semanales
    def plot_weekly(self):
        # Agrupar los gastos por semana y tipo, y calcular la suma total
        weekly_type_totals = self.outcomes.groupby(['week', 'type'], observed=False)['total'].sum().unstack()

        # Crear un gráfico de barras apiladas
        ax = weekly_type_totals.plot(kind='bar', stacked=True, figsize=(10, 6))

        # Añadir etiquetas y título al gráfico
        plt.xlabel('Week Number')
        plt.ylabel('Total (mxn)')
        plt.title('Total Finances per Week')

        # Rotar las etiquetas del eje x para mejor legibilidad
        plt.xticks(rotation=45, ha='right')

        # Añadir una leyenda al gráfico
        plt.legend(title='Type')

        # Ajustar el diseño para evitar cortes en las etiquetas
        plt.tight_layout()

        # Mostrar el gráfico
        plt.show()

        # Limpiar la figura para evitar superposiciones en futuros gráficos
        plt.clf()

        # Devolver los totales semanales
        return weekly_type_totals

    # Método para generar un gráfico de la evolución de los ingresos acumulados
    def total_revenue(self):
        # Calcular la suma diaria de los ingresos
        daily_sums = self.df.groupby('date')['total'].sum()

        # Calcular la suma acumulada de los ingresos
        cumulative_sums = daily_sums.cumsum()

        # Crear una figura para el gráfico
        plt.figure(figsize=(10, 6))

        # Formatear las fechas para el eje x
        dat1 = [str(d)[:-8] for d in daily_sums.index]

        # Obtener los valores acumulados para el eje y
        dat2 = [x for x in cumulative_sums.values]

        # Crear el gráfico de línea
        plt.plot(dat1, dat2)

        # Añadir etiquetas y título al gráfico
        plt.xlabel('Date')
        plt.ylabel('Revenue (mxn)')
        plt.title('Total Revenue')

        # Rotar las etiquetas del eje x para mejor legibilidad
        plt.xticks(rotation=45)

        # Ajustar el diseño para evitar cortes en las etiquetas
        plt.tight_layout()

        # Mostrar el gráfico
        plt.show()

        # Limpiar la figura para evitar superposiciones en futuros gráficos
        plt.clf()
