from calendar import c
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import streamlit as st
import pandas as pd
import datetime

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.sidebar.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.sidebar.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            if is_datetime64_any_dtype(df[column]):
                _min = df[column].min().to_pydatetime()
                _max = df[column].max().to_pydatetime()
                user_date_input = right.slider(
                    "Datetime slider",
                    value = (_min, _max),
                    min_value = _min,
                    max_value = _max,
                    step = datetime.timedelta(days=365)
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            elif is_categorical_dtype(df[column]):
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                if df[column].dtype == 'int64' or df[column].dtype == 'int32':
                    _min = int(df[column].min())
                    _max = int(df[column].max())
                    user_num_input = right.slider(
                        f"Values for {column}",
                        min_value = _min,
                        max_value = _max,
                        value = (_min, _max),
                        step = 1,
                    )
                else:
                    _min = float(df[column].min())
                    _max = float(df[column].max())
                    step = (_max - _min) / 10
                    user_num_input = right.slider(
                        f"Values for {column}",
                        min_value=_min,
                        max_value=_max,
                        value=(_min, _max),
                        step=step,
                    )
                df = df[df[column].between(*user_num_input)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df

@st.cache_data
def get_data(path: str, sep = ';', encoding='latin-1') -> pd.DataFrame:
    df = pd.read_csv(path, sep = sep, encoding = encoding)
    df = df.dropna(how='all', axis='columns')
    df = df.dropna()

    df = df.drop(columns=['FECHA_CORTE', 'N_SEC', 'UBIGEO', 'REG_NAT','PROVINCIA', 'DISTRITO', 'POB_URBANA', 'POB_RURAL'])

    df['DEPARTAMENTO'] = df['DEPARTAMENTO'].astype('category')

    df['PERIODO'] = pd.to_datetime(df['PERIODO'], format='%Y')
    df['PERIODO'] = pd.DatetimeIndex(df['PERIODO']).year

    df['POB_TOTAL'] = df['POB_TOTAL'].astype('int64')

    return df

def resume_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df['GPC_DOM'] *= df['POB_TOTAL']

    df = df.groupby(['DEPARTAMENTO', 'PERIODO']).sum().reset_index()

    df['GPC_DOM'] /= df['POB_TOTAL']

    return df

def compress_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    global not_compress, compress
    new_df = pd.DataFrame()

    for col in not_compress:
        new_df[col] = df[col]

    for key, value in compress.items():
        new_df[key] = df[value].sum(axis=1)
        new_df[key] /= 365*df['POB_TOTAL']/1000

    return new_df



# Variables
not_compress = ['DEPARTAMENTO', 'PERIODO', 'POB_TOTAL', 'GPC_DOM']
compress = {
    'DOMICILIARIOS': ['QRESIDUOS_DOM'],
    'ORGANICOS': ['QRESIDUOS_ALIMENTOS', 'QRESIDUOS_MALEZA', 'QRESIDUOS_OTROS_ORGANICOS'],
    'PAPEL': ['QRESIDUOS_PAPEL_BLANCO', 'QRESIDUOS_PAPEL_PERIODICO', 'QRESIDUOS_PAPEL_MIXTO'],
    'CARTON': ['QRESIDUOS_CARTON_BLANCO', 'QRESIDUOS_CARTON_MARRON', 'QRESIDUOS_CARTON_MIXTO'],
    'VIDRIO': ['QRESIDUOS_VIDRIO_TRANSPARENTE', 'QRESIDUOS_VIDRIO_OTROS_COLORES', 'QRESIDUOS_VIDRIOS_OTROS'],
    'POLIETILENO': ['QRESIDUOS_TEREFLATO_POLIETILENO', 'QRESIDUOS_POLIETILENO_ALTA_DENSIDAD', 'QRESIDUOS_POLIETILENO_BAJA_DENSIDAD', 'QRESIDUOS_POLIPROPILENO', 'QRESIDUOS_POLIESTIRENO', 'QRESIDUOS_POLICLORURO_VINILO'],
    'TETRABRICK': ['QRESIDUOS_TETRABRICK'],
    'METALES': ['QRESIDUOS_LATA', 'QRESIDUOS_METALES_FERROSOS', 'QRESIDUOS_ALUMINIO', 'QRESIDUOS_OTROS_METALES'],
    'NO_APROVECHABLES':['QRESIDUOS_BOLSAS_PLASTICAS', 'QRESIDUOS_SANITARIOS', 'QRESIDUOS_PILAS', 'QRESIDUOS_TECNOPOR', 'QRESIDUOS_INERTES', 'QRESIDUOS_TEXTILES', 'QRESIDUOS_CAUCHO_CUERO', 'QRESIDUOS_MEDICAMENTOS', 'QRESIDUOS_ENVOLTURAS_SNAKCS_OTROS', 'QRESIDUOS_OTROS_NO_CATEGORIZADOS']}