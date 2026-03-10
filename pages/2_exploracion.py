"""Página 2: Exploración interactiva de datos.

Ilustra: st.tabs, st.expander, st.selectbox, st.checkbox,
         st.pyplot con Matplotlib/Seaborn, st.dataframe con Polars.
"""

import polars as pl
import streamlit as st

from src.datos import generar_ventas, resumen_por_producto, resumen_por_region
from src.graficos import histograma_ventas, scatter_ventas_clientes

st.set_page_config(page_title="Exploración", page_icon="🔍", layout="wide")
st.title("🔍 Exploración de datos")


@st.cache_data
def cargar_datos():
    return generar_ventas()


df = cargar_datos()

# ── Barra lateral ─────────────────────────────────────────────────────────────
st.sidebar.title("🎛️ Filtros")
region = st.sidebar.selectbox(
    "Región",
    options=["Todas"] + sorted(df["region"].unique().to_list()),
)

df_f = df if region == "Todas" else df.filter(pl.col("region") == region)

# ── Pestañas ──────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["Dispersión", "Distribución", "Resúmenes"])

with tab1:
    st.subheader("Ventas vs Clientes")
    st.pyplot(scatter_ventas_clientes(df_f))

with tab2:
    st.subheader("Distribución de ventas")
    st.pyplot(histograma_ventas(df_f))

    with st.expander("Estadísticas descriptivas"):
        st.dataframe(df_f.select("ventas", "clientes").describe(), use_container_width=True)

with tab3:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Por región")
        st.dataframe(resumen_por_region(df_f), use_container_width=True)

    with col2:
        st.subheader("Por producto")
        st.dataframe(resumen_por_producto(df_f), use_container_width=True)
