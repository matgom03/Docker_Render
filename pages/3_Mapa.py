import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster, Fullscreen, MiniMap, MeasureControl
from streamlit_folium import st_folium
import plotly.express as px

# ===============================
# Carga de datos
# ===============================
@st.cache_data
def load_data():
    return pd.read_csv("finanzas_hogar.csv")

df = load_data()

# ===============================
# Título y descripción
# ===============================
st.title("Mapa Interactivo de Finanzas del Hogar")

st.markdown("""
Explora la distribución de los hogares según su **ingreso** y **ahorro mensual**.  
Usa los filtros laterales para ajustar el análisis por departamento o rangos de valores.  
Los puntos en el mapa están ligeramente desplazados para mejorar la visualización cuando varios hogares comparten las mismas coordenadas.
""")

# ===============================
# Filtros en sidebar
# ===============================
st.sidebar.header("Filtros del Mapa")

depto = st.sidebar.selectbox("Selecciona un Departamento:", sorted(df["Departamento"].unique()))

min_ing, max_ing = int(df["Ingreso_Mensual"].min()), int(df["Ingreso_Mensual"].max())
rango_ing = st.sidebar.slider("Rango de Ingreso Mensual:", min_ing, max_ing, (min_ing, max_ing))

min_ahorro, max_ahorro = int(df["Ahorro_Mensual"].min()), int(df["Ahorro_Mensual"].max())
rango_ahorro = st.sidebar.slider("Rango de Ahorro Mensual:", min_ahorro, max_ahorro, (min_ahorro, max_ahorro))

# ===============================
# Filtro dinámico
# ===============================
df_filtro = df[
    (df["Departamento"] == depto) &
    (df["Ingreso_Mensual"].between(*rango_ing)) &
    (df["Ahorro_Mensual"].between(*rango_ahorro))
]

st.subheader(f" Datos filtrados - {len(df_filtro)} hogares en {depto}")
st.dataframe(df_filtro)

# ===============================
# Creación del mapa (con jitter)
# ===============================
if not df_filtro.empty:
    # Copiar y generar jitter reproducible (basado en índice)
    df_filtro = df_filtro.copy()
    np.random.seed(42)  # Fijamos la semilla para mantener la posición estable
    jitter_lat = np.random.uniform(-0.002, 0.002, size=len(df_filtro))
    jitter_lon = np.random.uniform(-0.002, 0.002, size=len(df_filtro))
    df_filtro["Latitud_jitter"] = df_filtro["Latitud"] + jitter_lat
    df_filtro["Longitud_jitter"] = df_filtro["Longitud"] + jitter_lon

    # Crear mapa base
    m = folium.Map(
        location=[df_filtro["Latitud"].mean(), df_filtro["Longitud"].mean()],
        zoom_start=7,
        tiles="CartoDB positron"
    )

    # Controles interactivos del mapa
    Fullscreen(position="topleft").add_to(m)
    MiniMap(toggle_display=True).add_to(m)
    MeasureControl(primary_length_unit='kilometers').add_to(m)
    marker_cluster = MarkerCluster(name="Hogares agrupados", disableClusteringAtZoom=10).add_to(m)

    # Escala de color según ingreso
    q33, q66 = df["Ingreso_Mensual"].quantile([0.33, 0.66])
    def color_ingreso(valor):
        if valor < q33:
            return "#2ecc71"  # verde
        elif valor < q66:
            return "#f39c12"  # naranja
        else:
            return "#e74c3c"  # rojo

    # Añadir marcadores
    for i, row in df_filtro.iterrows():
        popup_html = f"""
        <div style="font-size:14px;">
            <b> Hogar ID:</b> {i}<br>
            <b> Departamento:</b> {row['Departamento']}<br>
            <b> Ingreso Mensual:</b> ${row['Ingreso_Mensual']:,}<br>
            <b> Ahorro Mensual:</b> ${row['Ahorro_Mensual']:,}
        </div>
        """
        folium.CircleMarker(
            location=[row["Latitud_jitter"], row["Longitud_jitter"]],
            radius=6,
            popup=popup_html,
            tooltip=f"Hogar {i}",
            color=color_ingreso(row["Ingreso_Mensual"]),
            fill=True,
            fill_color=color_ingreso(row["Ingreso_Mensual"]),
            fill_opacity=0.85
        ).add_to(marker_cluster)

    # Ajustar vista al rango filtrado
    m.fit_bounds(m.get_bounds())

    # Mostrar mapa interactivo
    map_data = st_folium(m, width=900, height=550)

    # ===============================
    # Interacción con clics en el mapa
    # ===============================
    if map_data and map_data.get("last_object_clicked"):
        lat = map_data["last_object_clicked"]["lat"]
        lon = map_data["last_object_clicked"]["lng"]

        # Buscar hogar más cercano al punto clickeado
        seleccionado = df_filtro.loc[
            ((df_filtro["Latitud_jitter"] - lat).abs() < 0.0005) &
            ((df_filtro["Longitud_jitter"] - lon).abs() < 0.0005)
        ]

        if not seleccionado.empty:
            st.success(f"Hogar seleccionado en {depto}")

            # Transformar datos
            df_bar = seleccionado.melt(
                id_vars=["Departamento"],
                value_vars=["Ingreso_Mensual", "Ahorro_Mensual"]
            )
            df_bar["value_fmt"] = df_bar["value"].apply(lambda x: f"${x:,.0f}")

            # Crear gráfico
            fig = px.bar(
            df_bar,
            x="variable",
            y="value",
            color="variable",
            text="value_fmt",
            title="Comparación: Ingreso vs Ahorro del Hogar Seleccionado",
            )

            fig.update_traces(
            textposition="outside",   # Mueve las etiquetas fuera de la barra
            textfont=dict(size=12),   # Tamaño de fuente más pequeño
            )

            fig.update_layout(
                showlegend=False,
                xaxis_title="",
                yaxis_title="Valor en $",
                template="plotly_white",
                margin=dict(t=60, b=40, l=40, r=40),
                uniformtext_minsize=10,
                uniformtext_mode="hide"   # Evita sobreposición de texto
            )

            st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("No hay datos que cumplan con los filtros seleccionados.")