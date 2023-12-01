import streamlit as st
from PIL import Image
import base64

st.set_page_config(page_title="Riesgos de IA",page_icon="🤖",layout="wide")
st.subheader(":blue[Panel de Evaluación de Riesgos de IA]")

def displayPDF(file):
    # Opening file from file path
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    
    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)
    

col1, mid, col2 = st.columns([1, 30, 100])
with col1:
    image = Image.open("data/logo1.png")
    st.image(image, width=300, caption='Modelo de evaluación de Riesgos IA')
with col2:
    st.markdown('''
        :blue[Los riesgos de los sistemas de IA son contextuales, por lo que es necesario garantizar las medidas adoptadas
        para mitigar los riesgos derivados de los sistemas de IA son proporcionales al grado real de riesgo
        o posibles daños que tales sistemas plantean. Las evaluaciones de riesgos e impactos de la IA proporcionan una aproximación estandar y
        estructurada para gestionar los riesgos de la IA. Permiten diferenciar IA en función de sus riesgos, de modo que puedan aplicarse medidas 
        de mitigación proporcionadas por los equipos responsables.
        El objetivo de este panel es la visualización de los riesgos, requisitos y medidas de mitigación asociados a un sistema 
        de Inteligencia Artificial según el Framework elaborado por KPMG y Telefónica en base al cuestionario del sistema de registro y el modelo de evaluación de riesgos de la IA.
        ]''')

st.markdown("""---""")



def tabs_home():
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Definición sistema IA", "Proceso de catalogación de riesgo de IA", "Ámbitos de evaluación del riesgo", "Modelo de evaluación del riesgo", "Modelo de mitigación de riesgos"])
    with tab1:        
        st.subheader(":blue[Definición de sistema de Inteligencia Artificial]")
        st.markdown('''
            :blue[Sistemas capaces de procesar datos e información de una manera que se asemeja a un comportamiento inteligente, y que abarcan generalmente aspectos de razonamiento, aprendizaje, percepción, predicción, planificación o control. abarcan generalmente aspectos de razonamiento, aprendizaje, percepción, predicción, planificación o control.]''')
        st.markdown(":blue[         * Definición más general y global de IA que permite englobar distintos sistemas y futuros avances tecnológicos.de IA que permite englobar distintos sistemas y futuros avances tecnológicos.]")
        st.markdown(":blue[         * Los sistemas de IA son tecnologías de procesamiento de la información que integran modelos y algoritmos que producen una capacidad para aprender y realizar tareas cognitivascapacidad para aprender y realizar tareas cognitivas, dando lugar a resultados como la predicción y la adopción de decisiones en , dando lugar a resultados como la predicción y la adopción de decisiones en entornos materiales y virtuales. entornos materiales y virtuales.]")
        st.markdown(":blue[         * Están diseñados para funcionar con diferentes grados de autonomíadiferentes grados de autonomía, mediante la modelización y representación del conocimiento y , mediante la modelización y representación del conocimiento y la explotación de datos y el cálculo de correlaciones. la explotación de datos y el cálculo de correlaciones.]")
        st.markdown(":blue[         * Las cuestiones éticas relativas a los sistemas de IA atañen todas las etapas del ciclo de vida todas las etapas del ciclo de vida de estos sistemas, desde la investigación, de estos sistemas, desde la investigación, la concepción, el desarrollo hasta el despliegue y la utilización, pasando por el mantenimiento, el funcionamiento, la comercla concepción, el desarrollo hasta el despliegue y la utilización, pasando por el mantenimiento, el funcionamiento, la comercialialización, ización, financiación, el seguimiento, evaluación, validación y fin de la utilización, desmontaje y terminación. financiación, el seguimiento, evaluación, validación y fin de la utilización, desmontaje y terminación.]")
        st.markdown(":blue[         * Los actores de la IA actores de la IA son aquellos que participan en al menos una etapa del ciclo de vida del sistema y pueden ser tanto personas son aquellos que participan en al menos una etapa del ciclo de vida del sistema y pueden ser tanto personas físicas como jurídicas. físicas como jurídicas.]")
        st.markdown(":blue[         * Los sistemas de IA plantean nuevos tipos de cuestiones éticas que incluyen su impacto en cuestiones éticas que incluyen su impacto en la adopción de decisiones, el empleo, la la adopción de decisiones, el empleo, la interacción social, la salud, la educación, los medios de comunicación, el acceso a la información, la brecha digital, la prointeracción social, la salud, la educación, los medios de comunicación, el acceso a la información, la brecha digital, la protectección del ción del consumidor y de los datos personales, el medio ambiente, la democracia, el estado de derecho, la seguridad y el mantenimientoconsumidor y de los datos personales, el medio ambiente, la democracia, el estado de derecho, la seguridad y el mantenimientodedel l orden, el doble uso y los derechos humanos y las libertades fundamentales, incluidas la libertad de expresión, la privacidad orden, el doble uso y los derechos humanos y las libertades fundamentales, incluidas la libertad de expresión, la privacidad y ly la no a no discriminación. discriminación.]")
    with tab2:  
        st.subheader(":blue[Proceso de catalogación de riesgo de IA]")
        st.markdown(''':blue[El objetivo de las preguntas iniciales del sistema de registro será la determinación de si estamos o no ante un sistema de Intelteligencia igencia Artificial según la definición adoptada por Telefónica y que, por lo tanto, deba ser objeto de registro y determinación del rArtificial según la definición adoptada por Telefónica y que, por lo tanto, deba ser objeto de registro y determinación del riesgo.]''')      
        st.markdown(":blue[Para ello, nos basamos en la definición de IA dada por la Unesco y en el propio Reglamento Europeo de IA, desarrollando cuestioniones es como las siguientes:]")
        image = Image.open("data/flujo_global_risk_IA.png")
        st.image(image, width=800,  caption='Proceso de catalogación de riesgo de IA')
        
        st.subheader(":blue[Flujo del la catalogación de riesgo de IA]")
        st.markdown(''':blue[Una vez determinamos que efectivamente se trata de un sistema de IA y que por tanto, debemos registrarlo en la herramienta y anaanalizar lizar su nivel de riesgo, llevamos a cabo una serie de preguntas generales de contexto e identificación del sistema que nos permitasu nivel de riesgo, llevamos a cabo una serie de preguntas generales de contexto e identificación del sistema que nos permitaposteriormente determinar qué niveles de riesgo (y sus correspondientes preguntas) son preceptivas en cada caso.posteriormente determinar qué niveles de riesgo (y sus correspondientes preguntas) son preceptivas en cada caso.]''')      
        st.markdown(''':blue[En función del contexto y la identificación inicial del sistema de IA, se irán abriendo o no determinadas preguntas adicionales es al al usuario. Por ejemplo, en caso de que el sistema de IA no implique el tratamiento de datos personales, no sería necesario recausuario. Por ejemplo, en caso de que el sistema de IA no implique el tratamiento de datos personales, no sería necesario recabarbarinformación adicional sobre este ámbito.información adicional sobre este ámbito.]''')      
        image = Image.open("data/flujo_risk_IA.png")
        st.image(image, width=800,  caption='Flujo del Modelo de Riesgo de IA')
    with tab3: 
        st.subheader(":blue[Ámbitos de evaluación del riesgo]")
        st.markdown(''':blue[Se plantean las siguientes subcategorías o taxonomías sobre las que evaluar el riesgo de los sistemas de IA de formorma que a que facilite posteriormente los procesos de mitigación de riesgos y toma de decisiones:facilite posteriormente los procesos de mitigación de riesgos y toma de decisiones:]''')      
        image = Image.open("data/ambitosevaluacion.png")
        st.image(image, width=1000,  caption='Ambitos de Evaluacion Riesgo de IA')        
    with tab4: 
        st.subheader(":blue[Modelo de evaluación del riesgo]")
        image = Image.open("data/Nivel_riesgo.png")
        st.image(image, width=1000,  caption='Nivel riesgo IA')
        image = Image.open("data/Nivel_riesgo_2.png")
        st.image(image, width=1000,  caption='Matriz de Impacto, Escala Riesgo de IA')
        image = Image.open("data/Nivel_riesgo_3.png")
        st.image(image, width=1000,  caption='Definición niveles de Impacto, Escala')
        
    with tab5: 
        st.subheader(":blue[Modelo de mitigación de riesgos]")
        st.markdown(''':blue[En función de los niveles de riesgo obtenidos con el modelo de evaluación – que a su vez se basa en las respuestas a las distintas preguntas del cuestionario o flujo de análisis descrito – planteamos a continuación una serie de requisitos para mitigar los riesgos identificados en cada uno de los ámbitos anteriores. La taxonomía de requisitos planteada se basa en el área o departamento propietaria del mismo, independientemente del ámbito de origen del riesgo.]''')      
        image = Image.open("data/Modelo_mitigacion.png")
        st.image(image, width=1000,  caption='Ambitos de Evaluacion Riesgo de IA')        
        
        

tabs_home()
st.markdown("""---""")

st.markdown(''':blue[A continuación puede visializar la presentación de la herramienta de Riesgo IA:]''')      
displayPDF("data/FlujoTelefonica.pdf")

theme_plotly = None # None or streamlit
# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

# Content
#c1, c2 = st.columns(2)

#theme
hide_st_style=""" 

<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""



