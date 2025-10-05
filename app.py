import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_csv("finanzas_hogar.csv")
    return df

df = load_data()

st.title("Finanzas de Hogares en Colombia")
st.write("""
Bienvenido a la aplicación de análisis de finanzas de hogares. 
Se analizo un dataset para georeferenciar acerca de las finanzas de los hogares en
Colombia. 

En el menú lateral podrás navegar entre:
- **Dashboard** con análisis descriptivo.
- **Mapa** interactivo de georreferenciación.
""")

st.subheader("Vista previa de los datos")
st.dataframe(df.head())