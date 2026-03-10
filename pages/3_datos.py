"""Página 3: Datos crudos y exportación.

Ilustra: st.dataframe con Polars, st.download_button, st.number_input,
         st.radio, conversión Polars → CSV/Parquet.
"""

import polars as pl
import streamlit as st

from src.datos import generar_ventas

st.set_page_config(page_title="Datos", page_icon="📥", layout="wide")
st.title("📥 Datos crudos")


@st.cache_data
def cargar_datos():
    return generar_ventas()


df = cargar_datos()

# ── Controles ─────────────────────────────────────────────────────────────────
st.sidebar.title("🎛️ Opciones")
n_filas = st.sidebar.number_input(
    "Filas a mostrar",
    min_value=10,
    max_value=len(df),
    value=50,
    step=10,
)
formato = st.sidebar.radio("Formato de descarga", ["CSV", "Parquet"])
orden = st.sidebar.selectbox(
    "Ordenar por",
    options=df.columns,
    index=df.columns.index("fecha"),
)
descendente = st.sidebar.checkbox("Descendente", value=False)

# ── Tabla ─────────────────────────────────────────────────────────────────────
df_ordenado = df.sort(orden, descending=descendente)

st.subheader(f"Mostrando {n_filas} de {len(df)} registros")
st.dataframe(df_ordenado.head(n_filas), use_container_width=True)

st.markdown("---")

# ── Descarga ──────────────────────────────────────────────────────────────────
st.subheader("Exportar datos")

col1, col2 = st.columns(2)

with col1:
    st.info(
        f"**Formato seleccionado:** {formato}\n\n"
        "Polars escribe directamente a bytes sin conversión intermedia a Pandas."
    )

with col2:
    if formato == "CSV":
        datos = df.write_csv().encode("utf-8")
        nombre = "ventas.csv"
        mime = "text/csv"
    else:
        import io
        buf = io.BytesIO()
        df.write_parquet(buf)
        datos = buf.getvalue()
        nombre = "ventas.parquet"
        mime = "application/octet-stream"

    st.download_button(
        label=f"⬇️ Descargar {formato}",
        data=datos,
        file_name=nombre,
        mime=mime,
        use_container_width=True,
    )

# ── Schema ────────────────────────────────────────────────────────────────────
with st.expander("Schema del DataFrame (Polars)"):
    schema_df = pl.DataFrame(
        {
            "columna": df.columns,
            "tipo": [str(t) for t in df.dtypes],
            "nulos": df.null_count().row(0),
        }
    )
    st.dataframe(schema_df, use_container_width=True)
