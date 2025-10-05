import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

@st.cache_data
def load_data():
    return pd.read_csv("finanzas_hogar.csv")

df = load_data()

st.title("Dashboard de Finanzas")
st.sidebar.header("Filtros del Dashboard")

# Filtro múltiple por departamentos
depto = st.sidebar.multiselect(
    "Selecciona Departamentos:",
    df["Departamento"].unique(),
    default=df["Departamento"].unique()
)

df_filtrado = df[df["Departamento"].isin(depto)]

# ========================
# Resumen estadístico
# ========================
st.subheader("Resumen estadístico")
st.write(df_filtrado.describe())

# ========================
# Boxplots dinámicos
# ========================
st.subheader("Boxplots de Variables Clave")

variables_numericas = ["Ingreso_Mensual", "Ahorro_Mensual", "Gasto_Alimentacion", "Gasto_Educacion"]
var_box = st.selectbox("Selecciona variable para boxplot:", variables_numericas)

fig, ax = plt.subplots(figsize=(12, 6))  # más ancho para dar espacio
df_filtrado.boxplot(column=var_box, by="Departamento", ax=ax, grid=False)

ax.set_title(f"Distribución de {var_box} por Departamento")
ax.set_ylabel(var_box)
ax.set_xlabel("Departamento")

# Rotar nombres para que se lean bien
plt.xticks(rotation=45, ha="right")
st.pyplot(fig)
# ========================
# Histograma dinámico
# ========================
st.subheader("Distribución con Histogramas")

var_hist = st.selectbox("Selecciona variable para histograma:", variables_numericas, index=0)

fig, ax = plt.subplots()
df_filtrado[var_hist].hist(ax=ax, bins=20, color="skyblue", edgecolor="black")
ax.set_xlabel(var_hist)
ax.set_ylabel("Frecuencia")
st.pyplot(fig)

# ========================
# Scatterplot dinámico
# ========================
st.subheader("Relación entre Variables (Scatterplot)")

x_var = st.selectbox("Variable en eje X:", variables_numericas, index=0)
y_var = st.selectbox("Variable en eje Y:", variables_numericas, index=1)
size_var = st.selectbox("Variable para tamaño de puntos:", variables_numericas, index=2)

fig2 = px.scatter(
    df_filtrado,
    x=x_var,
    y=y_var,
    color="Departamento",
    size=size_var,
    hover_data=["Departamento"]
)
st.plotly_chart(fig2)