import warnings
warnings.filterwarnings('ignore')

import streamlit as st
import pandas as pd
from utilities import *


st.set_page_config(     
    page_title="Dashboard Programación Avanzada",
    layout="wide",
)

used = st.sidebar.checkbox("Solo mostrar columnas usadas", value=True)
if used:
    info = pd.read_excel('data/info_used.xlsx')
else:
    info = pd.read_excel('data/info.xlsx')


url = 'https://www.datosabiertos.gob.pe/sites/default/files/D.%20Composici%C3%B3n%20Anual%20de%20residuos%20domiciliarios_Distrital_2019_2022.csv'

data = get_data(url, sep = ';', encoding='latin-1')

st.title('Dashboard Programación Avanzada')
st.header('Proyecto: Análisis de residuos sólidos en el Perú', divider=True)
st.header('Integrantes:', divider=True)
st.markdown('''
            - **Antay Bellido Lizbeth**
            - **Atao Surichaqui Ester Solamit**
            - **Romina Perez Amado**
            ''')
st.header('Resumen:', divider=True)

st.markdown('''

- **Objetivo general:** Desarrollar un Dashboard empleando Streamlit analizando la data de residuos sólidos en diferentes regiones del Perú.
- **Objetivos específicos:**
    - Identificar la composición de residuos sólidos en el Perú.
    - Identificar las principales fuentes de contaminación.
    - Proponer soluciones para mitigar el impacto ambiental.

- **Fuentes de datos:** [Datos Abiertos del Perú](https://www.datosabiertos.gob.pe/dataset/composicion-anual-de-residuos-domiciliarios-distrital-2019-2022)
''')
st.markdown('- Cantidad de registros: :green[{}]'.format(data.shape[0]))

st.table(info)