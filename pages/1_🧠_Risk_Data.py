import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
import altair as alt

#from query import *
import time

st.set_page_config(page_title="Riesgos de IA",page_icon="🧠",layout="wide")
# Title
st.title('🧠 Risk_Data')

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

def Home():
    with st.expander("⏰ Evaluación de Riesgos WorkBook"):
        #showData=st.multiselect('Filter: ',df_selection.columns,default=["Ámbito"])
        #showData=st.multiselect('Filter: ',df_selection.columns)
        st.dataframe(df_selection, use_container_width=True)
        
        #st.dataframe(df_selection[showData],use_container_width=True)
    st.markdown("""---""")


group_ponderación= pd.DataFrame(df_selection.groupby(['DOMINIO', 'Ámbito'])['Ponderación'].sum())
group_ponderación.reset_index(inplace=True)

# Horizontal stacked bar chart 1
chart = (
    alt.Chart(group_ponderación)
    .mark_bar()
    .encode(
        x=alt.X("Ponderación", type="quantitative", title="Ponderación sum()"),
        y=alt.Y("DOMINIO", type="nominal", title="DOMINIO"),
        color=alt.Color("Ámbito", type="nominal", title="Ámbito"),
        order=alt.Order("Ámbito", sort="descending"),
    )
)
st.altair_chart(chart, use_container_width=True)


group_ponderación_count= pd.DataFrame(df_selection.groupby(['DOMINIO', 'Ámbito'])['Ponderación'].count())
group_ponderación_count.reset_index(inplace=True)

# Horizontal stacked bar chart 2
chart2 = (
    alt.Chart(group_ponderación_count)
    .mark_bar()
    .encode(
        x=alt.X("Ponderación", type="quantitative", title="Ponderación count()"),
        y=alt.Y("DOMINIO", type="nominal", title="DOMINIO"),
        color=alt.Color("Ámbito", type="nominal", title="Ámbito"),
        order=alt.Order("Ámbito", sort="descending"),
    )
)
st.altair_chart(chart2, use_container_width=True)

# sunburst plot
group_subdominio_count= pd.DataFrame(df_selection.groupby(['DOMINIO', 'SUBDOMINIO', 'RIESGO'])['RIESGO'].count())
group_subdominio_count.rename(columns = {'RIESGO':'valor'}, inplace = True)
group_subdominio_count.reset_index(inplace=True)
fig = px.sunburst(group_subdominio_count, path=["DOMINIO", "SUBDOMINIO", "RIESGO"], values="valor", branchvalues = 'total', 
                  title='Categorias bloques de preguntas en la Evaluación de Riesgos',
                  width=750, height=750)
st.plotly_chart(fig)


hide_st_style=""" 
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""