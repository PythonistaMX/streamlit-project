"""Página 1: Dashboard completo con filtros.

Ilustra: st.sidebar, st.multiselect, st.slider, st.metric, st.pyplot,
         st.columns, @st.cache_data, Polars + Matplotlib/Seaborn.
"""

import streamlit as st

from src.datos import generar_ventas
from src.graficos import barras_producto, barras_region, linea_ventas

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
st.title("📊 Dashboard")


@st.cache_data
def cargar_datos():
    return generar_ventas()


df = cargar_datos()

# ── Barra lateral ─────────────────────────────────────────────────────────────
st.sidebar.title("🎛️ Filtros")

regiones = st.sidebar.multiselect(
    "Región",
    options=sorted(df["region"].unique().to_list()),
    default=sorted(df["region"].unique().to_list()),
)

productos = st.sidebar.multiselect(
    "Producto",
    options=sorted(df["producto"].unique().to_list()),
    default=sorted(df["producto"].unique().to_list()),
)

min_ventas = int(df["ventas"].min())
max_ventas = int(df["ventas"].max())
rango_ventas = st.sidebar.slider(
    "Rango de ventas ($)",
    min_value=min_ventas,
    max_value=max_ventas,
    value=(min_ventas, max_ventas),
)

# ── Filtrado con Polars ───────────────────────────────────────────────────────
import polars as pl  # noqa: E402

df_f = df.filter(
    pl.col("region").is_in(regiones)
    & pl.col("producto").is_in(productos)
    & pl.col("ventas").is_between(rango_ventas[0], rango_ventas[1])
)

if df_f.is_empty():
    st.warning("No hay datos para los filtros seleccionados.")
    st.stop()

# ── Métricas ──────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total ventas",    f"${df_f['ventas'].sum():,.0f}")
c2.metric("Promedio ventas", f"${df_f['ventas'].mean():,.0f}")
c3.metric("Total clientes",  f"{df_f['clientes'].sum():,}")
c4.metric("Registros",       f"{len(df_f):,}")

st.markdown("---")

# ── Gráficos ──────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.pyplot(linea_ventas(df_f))

with col2:
    st.pyplot(barras_region(df_f))

st.pyplot(barras_producto(df_f))
