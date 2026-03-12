"""Página de inicio del dashboard de ventas.

Ilustra los conceptos del notebook N39: Introducción a Streamlit.

Para ejecutar:
    streamlit run app.py
"""

import streamlit as st

from src.datos import generar_ventas, resumen_por_region
from src.graficos import barras_region

st.set_page_config(
    page_title="Dashboard de Ventas",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Dashboard de Ventas")
st.markdown(
    """
Aplicación de ejemplo que ilustra el notebook **N39 — Introducción a Streamlit** del
curso **py311**.

Demuestra los conceptos clave:
- Carga y procesamiento con **Polars** (rápido, sin conversión innecesaria)
- Visualizaciones con **Matplotlib** y **Seaborn**
- *Widgets* de *Streamlit*: `slider`, `multiselect`, `metric`, `dataframe`
- *Caching* con `@st.cache_data`
- *Layout* con columnas y barra lateral

Usa el menú lateral para navegar entre las páginas.
"""
)

st.markdown("---")


@st.cache_data
def cargar_datos():
    return generar_ventas()


df = cargar_datos()

# Métricas globales
st.subheader("Resumen global")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total ventas", f"${df['ventas'].sum():,.0f}")
c2.metric("Promedio diario", f"${df['ventas'].mean():,.0f}")
c3.metric("Total clientes", f"{df['clientes'].sum():,}")
c4.metric("Días registrados", str(len(df)))

st.markdown("---")

# Gráfico de resumen
col1, col2 = st.columns(2)

with col1:
    st.pyplot(barras_region(df))

with col2:
    st.subheader("Resumen por región")
    st.dataframe(resumen_por_region(df), use_container_width=True)
