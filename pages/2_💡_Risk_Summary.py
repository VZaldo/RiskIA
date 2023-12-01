import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
#from query import *
import time

from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters")

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

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 20:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df

st.set_page_config(page_title="Riesgos de IA",page_icon="💡",layout="wide")
st.title('💡 Risk_Summary')
st.subheader("🚨  :blue[Panel de Evaluación de Riesgos de IA]")
st.markdown('''
    :blue[El objetivo de este panel es la visualización de los riesgos asociados a un sistema de Inteligencia artificial según el Framework elaborado por 
    KPMG y Telefónica en base al cuestionario del sistema de registro y el modelo de evaluación de riesgos de la IA.]''')
st.markdown("""---""")
theme_plotly = None # None or streamlit
# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

# ---- READ EXCEL ----
def get_data_from_excel():
    df = pd.read_excel(
        io="data.xlsm",
        engine="openpyxl",
        sheet_name="Evaluación de riesgos",
        #skiprows=6,
        #usecols="B:E",
        #nrows=13
    )
    return df

df = get_data_from_excel()

def color_vowel(value):
    return f"background-color: pink;" if value in [*"NO"] else None

#switcher
st.sidebar.header("Filtrado del cuestionario de riesgo de IA")

dominio=st.sidebar.multiselect(
    "Select DOMINIO",
     options=df["DOMINIO"].unique(),
     default=df["DOMINIO"].unique(),
)

df_selection=df.query(
    "DOMINIO==@dominio"
)

df_pro_mean = pd.DataFrame(df_selection[["Valores centrados en el ser humano y equidad - Valor Probabilidad","Robustez y seguridad - Valor Probabilidad", "Responsabilidad - Valor Probabilidad", "Transparencia y explicabilidad - Valor Probabilidad", "Bienestar social y ambiental - Valor Probabilidad", "Privacidad y data governance - Valor Probabilidad"]].mean())
df_impa_mean = pd.DataFrame(df_selection[["Valores centrados en el ser humano y equidad - Valor Impacto","Robustez y seguridad - Valor Impacto", "Responsabilidad - Valor Impacto", "Transparencia y explicabilidad - Valor Impacto", "Bienestar social y ambiental - Valor Impacto", "Privacidad y data governance - Valor Impacto"]].mean())
df_escala_max = pd.DataFrame(df_selection[["Valores centrados en el ser humano y equidad - Escala","Robustez y seguridad - Escala", "Responsabilidad - Escala", "Transparencia y explicabilidad - Escala", "Bienestar social y ambiental - Escala", "Privacidad y data governance - Escala"]].max())
df_pro_mean.reset_index(inplace=True)
df_impa_mean.reset_index(inplace=True)
df_escala_max.reset_index(inplace=True)
df_summary = pd.concat([df_pro_mean, df_impa_mean.iloc[:, 1], df_escala_max.iloc[:, 1]], axis=1)
df_summary.columns = ['Risk', 'Probabilidad', 'Impacto', 'Escala']
df_summary['Risk'] = df_summary['Risk'].str.replace(' - Valor Probabilidad', '')


def Home():
    with st.expander("⏰ Evaluación de Riesgos WorkBook"):
        st.dataframe(df_selection, use_container_width=True)
        
    #compute top analytics
    val1 = float(df_summary['Probabilidad'].mean())
    val2 = float(df_summary['Impacto'].mean())
    val3 = float(df_summary['Escala'].max())

    val_1, val_2, val_3 = st.columns(3, gap='large')
    with val_1:
        st.info('Probabilidad Riesgo Media',icon="🔥")
        st.metric(label="Probabilidad",value=f"{val1:,.0f}")
    with val_2:
        st.info('Impacto Riesgo Medio',icon="🚩")
        st.metric(label="Impacto",value=f"{val2:,.0f}")
    with val_3:
        st.info('Escala Riesgo Maxima',icon="🚨")
        st.metric(label="Escala",value=f"{val3:,.0f}")

    st.markdown("""---""")
#df_pro_mean.rename(columns={"Bienestar social y ambiental - Valor Impacto": "Value"}, inplace=True)

fig4 = px.line_polar(df_summary, r="Impacto", theta="Risk", color="Probabilidad", color_discrete_sequence=px.colors.sequential.Plasma_r, template="plotly_dark")

def graphs_1():
    tab1, tab2, tab3, tab4 = st.tabs(["Riesgos por bloque", "Riesgos por bloque 3D", "Matriz de Riesgos", "Polar"])    
    with tab1:        
        fig = px.scatter(df_summary,
        x="Impacto",
        y="Probabilidad",
        size="Escala",
        color="Risk",
        hover_name="Risk"
        )
        fig.update_layout(yaxis_range=[0,5])
        fig.update_layout(xaxis_range=[0,5])
        fig.update_layout(width=1100, height=700)
        tab1.subheader("Riesgos por bloque")
        st.plotly_chart(fig, theme="streamlit")
    with tab2:        
        fig2 = px.scatter_3d(df_summary, x='Impacto', y='Probabilidad', z='Escala', color='Risk', width=1100, height=700)
        tab2.subheader("Riesgos por bloque 3D")
        st.plotly_chart(fig2, theme="streamlit")
    with tab3:
        #HeatMap
        HeatMap=[[5,10,	15,	20,	25],
                [4,	8,	12,	16,	20],
                [3,	6,	9,	12,	15],
                [2,	4,	6,	8,	10],
                [1,	2,	3,	4,	5]]
        fig_HeatMap = px.imshow(HeatMap, labels=dict(x="Impacto", y="Probabilidad", color="Riesgo"),
                        x=['Minimo', 'Moderado', 'Serio', 'Grave', 'Muy Grave'],
                        y=['Frecuente', 'Recurrente', 'Posible', 'Inusual', 'Remota'], aspect="auto", color_continuous_scale="Viridis", width=900, height=600
                        )
        fig_HeatMap.update_xaxes(side="top")
        tab3.subheader("Matriz de Riesgos")
        st.plotly_chart(fig_HeatMap, theme="streamlit", use_container_width=True)
    with tab4:
        st.plotly_chart(fig4, theme="streamlit")
            

Home()
graphs_1()


df_humanos_prob = df_selection[['DOMINIO', 'Elementos de riesgo', 'Valores centrados en el ser humano y equidad - Valor Probabilidad']].dropna(subset=['Valores centrados en el ser humano y equidad - Valor Probabilidad'])
df_humanos_prob.rename(columns={"Valores centrados en el ser humano y equidad - Valor Probabilidad": "Value"}, inplace=True)
df_humanos_prob['Categoria Riesgo'] = 'Valores centrados en el ser humano y equidad'
df_humanos_prob['Riesgo'] = 'Probabilidad'

df_humanos_impa = df_selection[['DOMINIO', 'Elementos de riesgo', 'Valores centrados en el ser humano y equidad - Valor Impacto']].dropna(subset=['Valores centrados en el ser humano y equidad - Valor Impacto'])
df_humanos_impa.rename(columns={"Valores centrados en el ser humano y equidad - Valor Impacto": "Value"}, inplace=True)
df_humanos_impa['Categoria Riesgo'] = 'Valores centrados en el ser humano y equidad'
df_humanos_impa['Riesgo'] = 'Impacto'

df_seg_prob = df_selection[['DOMINIO', 'Elementos de riesgo', 'Robustez y seguridad - Valor Probabilidad']].dropna(subset=['Robustez y seguridad - Valor Probabilidad'])
df_seg_prob.rename(columns={"Robustez y seguridad - Valor Probabilidad": "Value"}, inplace=True)
df_seg_prob['Categoria Riesgo'] = 'Robustez y seguridad'
df_seg_prob['Riesgo'] = 'Probabilidad'

df_seg_impa = df_selection[['DOMINIO', 'Elementos de riesgo', 'Robustez y seguridad - Valor Impacto']].dropna(subset=['Robustez y seguridad - Valor Impacto'])
df_seg_impa.rename(columns={"Robustez y seguridad - Valor Impacto": "Value"}, inplace=True)
df_seg_impa['Categoria Riesgo'] = 'Robustez y seguridad'
df_seg_impa['Riesgo'] = 'Impacto'

df_resp_prob = df_selection[['DOMINIO', 'Elementos de riesgo', 'Responsabilidad - Valor Probabilidad']].dropna(subset=['Responsabilidad - Valor Probabilidad'])
df_resp_prob.rename(columns={"Responsabilidad - Valor Probabilidad": "Value"}, inplace=True)
df_resp_prob['Categoria Riesgo'] = 'Responsabilidad'
df_resp_prob['Riesgo'] = 'Probabilidad'

df_resp_impa = df_selection[['DOMINIO', 'Elementos de riesgo', 'Responsabilidad - Valor Impacto']].dropna(subset=['Responsabilidad - Valor Impacto'])
df_resp_impa.rename(columns={"Responsabilidad - Valor Impacto": "Value"}, inplace=True)
df_resp_impa['Categoria Riesgo'] = 'Responsabilidad'
df_resp_impa['Riesgo'] = 'Impacto'

df_trans_prob = df_selection[['DOMINIO', 'Elementos de riesgo', 'Transparencia y explicabilidad - Valor Probabilidad']].dropna(subset=['Transparencia y explicabilidad - Valor Probabilidad'])
df_trans_prob.rename(columns={"Transparencia y explicabilidad - Valor Probabilidad": "Value"}, inplace=True)
df_trans_prob['Categoria Riesgo'] = 'Transparencia y explicabilidad'
df_trans_prob['Riesgo'] = 'Probabilidad'

df_trans_impa = df_selection[['DOMINIO', 'Elementos de riesgo', 'Transparencia y explicabilidad - Valor Impacto']].dropna(subset=['Transparencia y explicabilidad - Valor Impacto'])
df_trans_impa.rename(columns={"Transparencia y explicabilidad - Valor Impacto": "Value"}, inplace=True)
df_trans_impa['Categoria Riesgo'] = 'Transparencia y explicabilidad'
df_trans_impa['Riesgo'] = 'Impacto'

df_soc_prob = df_selection[['DOMINIO', 'Elementos de riesgo', 'Bienestar social y ambiental - Valor Probabilidad']].dropna(subset=['Bienestar social y ambiental - Valor Probabilidad'])
df_soc_prob.rename(columns={"Bienestar social y ambiental - Valor Probabilidad": "Value"}, inplace=True)
df_soc_prob['Categoria Riesgo'] = 'Bienestar social y ambiental'
df_soc_prob['Riesgo'] = 'Probabilidad'

df_soc_impa = df_selection[['DOMINIO', 'Elementos de riesgo', 'Bienestar social y ambiental - Valor Impacto']].dropna(subset=['Bienestar social y ambiental - Valor Impacto'])
df_soc_impa.rename(columns={"Bienestar social y ambiental - Valor Impacto": "Value"}, inplace=True)
df_soc_impa['Categoria Riesgo'] = 'Bienestar social y ambiental'
df_soc_impa['Riesgo'] = 'Impacto'

df_priv_prob = df_selection[['DOMINIO', 'Elementos de riesgo', 'Privacidad y data governance - Valor Probabilidad']].dropna(subset=['Privacidad y data governance - Valor Probabilidad'])
df_priv_prob.rename(columns={"Privacidad y data governance - Valor Probabilidad": "Value"}, inplace=True)
df_priv_prob['Categoria Riesgo'] = 'Privacidad y data governance'
df_priv_prob['Riesgo'] = 'Probabilidad'

df_priv_impa = df_selection[['DOMINIO', 'Elementos de riesgo', 'Privacidad y data governance - Valor Impacto']].dropna(subset=['Privacidad y data governance - Valor Impacto'])
df_priv_impa.rename(columns={"Privacidad y data governance - Valor Impacto": "Value"}, inplace=True)
df_priv_impa['Categoria Riesgo'] = 'Privacidad y data governance'
df_priv_impa['Riesgo'] = 'Impacto'

df_filter_risk = pd.concat([df_humanos_prob, df_humanos_impa, df_seg_prob, df_seg_impa, df_resp_prob, df_resp_impa, df_trans_prob, df_trans_impa, df_soc_prob, df_soc_impa, df_priv_prob, df_priv_impa])
st.dataframe(filter_dataframe(df_filter_risk))

# Pintamos las graficas
def graphs_2():
    tab1, tab2= st.tabs(["Boxplot Categoria Riesgos IA", "Matriz de Riesgos"])
    with tab1:
        fig = px.box(df_filter_risk, y="Categoria Riesgo", x="Value", color="Riesgo", orientation='h')
        st.plotly_chart(fig)
    with tab2:
        # sunburst plot
        fig = px.line_polar(df_filter_risk, r="Value", theta="Categoria Riesgo", color="Riesgo", color_discrete_sequence=px.colors.sequential.Plasma_r)
        st.plotly_chart(fig)

graphs_2()
#theme
hide_st_style=""" 

<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""