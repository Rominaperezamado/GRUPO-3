import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

from utilities import *
from pages.Dataset import resumed_data

plt.rcParams["figure.autolayout"] = True

st.sidebar.subheader('Gráficas de todos los residuos per capita', divider='green')
df = resumed_data.copy()
column = 'PERIODO'
_min = int(df[column].min())
_max = int(df[column].max())
user_num_input = st.sidebar.slider(
f"Ingrese el rango de años a visualizar en las gráfica.",
min_value = _min,
max_value = _max,
value = (_min, _max),
step = 1,
)
df = df[df[column].between(*user_num_input)]

st.header('Gráficos de Generación de Residuos per cápita (kg/hab-día)', divider=True)
compressed_data = compress_dataframe(df).reset_index(drop=True)
st.subheader('Gráficas de todos los residuos per capita', divider='green')
departments = list(df['DEPARTAMENTO'].unique())
for i in range(len(departments)):
        departments[i] = departments[i][:3]

sns.set(font_scale=0.5)
sns.set_style("whitegrid")
fig, ax = plt.subplots(3, 3, figsize=(10, 10))
for i, (key, value) in enumerate(compress.items()):
        sns.lineplot(data = compressed_data, x = 'DEPARTAMENTO', y = key, hue = 'PERIODO', ax = ax[i//3, i%3], palette="bright", alpha=.9)
        ax[i//3, i%3].set_title(key)
        ax[i//3, i%3].set_xticklabels(departments,rotation=90)
        ax[i//3, i%3].set_xlabel(None)
st.pyplot(fig)


st.sidebar.header('Generación del Residuo Seleccionado per cápita (kg/hab-día)', divider='orange')
option = st.sidebar.selectbox('Selecciona el tipo de residuo a mostrar en la gráfica.', compress.keys())
sns.set(font_scale=1)

st.subheader('Generación del Residuo Seleccionado per cápita (kg/hab-día)', divider='orange')
plot = sns.relplot(data = compressed_data, x = 'DEPARTAMENTO', y = option, hue = 'PERIODO', kind = 'line', palette="bright", alpha=.9, height=9)
plot.set_ylabels('Generación Residuos seleccionados per cápita (kg/hab-día)')
plot.set_xlabels('Departamento')
plot.set_xticklabels(rotation=90)
plot.set(title = option)
st.pyplot(plot)


options = list(resumed_data['DEPARTAMENTO'].unique())
options.sort()
st.sidebar.header('DataSet Compreso', divider='red')
countries = st.sidebar.multiselect(
        "Escoge departamentos a visualizar en el gráfico(3 como máximo).", options, default = ['LIMA'], max_selections=3
)
compressed_data = compress_dataframe(resumed_data[resumed_data['DEPARTAMENTO'].isin(countries)]).reset_index(drop=True)

st.header('Dataset Compreso', divider='red')
st.write('''
        Dataset comprimido, empleando el dataset resumido anteriormente se comprime la data por departamento, mostrando las estadísticas por categoría de desperdicio.
        ''')

st.dataframe(compressed_data)

df = compressed_data.copy()
print(compressed_data.head())

st.header('Gráficos', divider='rainbow')

sns.set_theme(style="whitegrid")

# Gráfico de barras de Población
plot = sns.catplot(data=df, x = 'DEPARTAMENTO', y = 'POB_TOTAL', hue = 'PERIODO', kind = 'bar',
                palette="dark", alpha=.6, height=9)
plot.set_ylabels('Población')
plot.set_xlabels('Departamento')
plot.set_xticklabels(rotation=90)
st.pyplot(plot)

sns.set(font_scale=0.5)
sns.set_style("whitegrid")
fig, ax = plt.subplots(3, 3, figsize=(10, 10))
for i, (key, value) in enumerate(compress.items()):
        sns.lineplot(data = df, x = 'DEPARTAMENTO', y = key, hue = 'PERIODO', ax = ax[i//3, i%3], palette="bright", alpha=.9)
        ax[i//3, i%3].set_title(key)
        ax[i//3, i%3].set_xticklabels(departments,rotation=90)
        ax[i//3, i%3].set_xlabel(None)
st.pyplot(fig)