import streamlit as st
from utilities import *
from main import data

st.header('Dataset Original/Filtrado', divider=True)
st.sidebar.header('Dataset Original/Filtrado', divider=True)
st.write('''
        Dataset original, con la data limpia, se hace caso omiso a los distritos y se analizará por departamentos, ya que sería mucha sobrecarga de información. Adicionalmente se presenta la opción de eliminar datos aplicando filtros en las columnas seleccionadas en el cuadro de la izquierda. De esta manera, se pueden eliminar datos que no son de interés para el análisis, poniendo límites inferiores en los datos requeridos.
        ''')
filtered_data = filter_dataframe(data)
st.dataframe(filtered_data)


st.header('Dataset Resumido por Años', divider=True)
st.write('''
        Dataset resumido, empleando el dataset filtrado anteriormente se resume la data por departamento, mostrando las estadísticas por departamento. Para una mejor visualización se puede seleccionar departamentos específicos en el cuadro, de esta manera se puede comparar los departamentos seleccionados en el gráfico de población inferior **(Esta selección no modificará el dataset a menos que se le de click a la opción de "Guardar Departamentos Seleccionados" en el cuadro de la izquierda)**.
        ''')
resumed_data = resume_dataframe(data).reset_index(drop=True)
st.dataframe(resumed_data)