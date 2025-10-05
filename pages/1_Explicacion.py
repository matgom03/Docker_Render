import streamlit as st
import pandas as pd
st.image("finanzas.jpg", caption="Visualización general de finanzas en Colombia", use_container_width=True)

st.title("Descripción del Dataset")

st.markdown("""
Este dataset contiene información sobre **finanzas de hogares** en distintos departamentos.
Incluye variables como:
- `ID`: Identificacion del Hogar 
- `Departamento`: Ubicación geográfica del hogar. Se tomo informacion de solo algunos departamentos tales como Bólivar, 
Atlántico, Magdalena,Santander,Valle del cauca, etc
- `Ingreso_Mensual`: Ingreso total mensual de los hogares en el departamento .
- `Gasto_Alimentacion` : Gasto que se realizo para la alimentacion en el hogar.
- `Gasto_Educacion` : Gasto que se realizo para la educación en el hogar. 
- `Ahorro_Mensual`: Cantidad ahorrada en el hogar cada mes.
- `Latitud` y `Longitud`: Coordenadas para visualización geográfica. Se utilizan para la creacion del mapa y su visualizacion.
""")

st.markdown("""
**Fuente de los datos:**  
[https://github.com/Kalbam/Datos_DATAVIZ/blob/main/finanzas_hogar.csv](https://github.com/Kalbam/Datos_DATAVIZ/blob/main/finanzas_hogar.csv)
""")

st.markdown("""
**Fuente de la imagen:**  
[https://www.ceupe.ec/blog/finanzas-familiares.html](https://www.ceupe.ec/blog/finanzas-familiares.html)
""")