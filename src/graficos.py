"""Funciones de visualización con Plotly.

Todas las funciones reciben un DataFrame de Polars y devuelven un Figure de Plotly.
No importan streamlit, lo que permite testarlas de forma aislada.
"""

import plotly.express as px
import plotly.graph_objects as go
import polars as pl


def linea_ventas(df: pl.DataFrame) -> go.Figure:
    """Gráfico de línea de ventas diarias por región."""
    return px.line(
        df.sort("fecha").to_pandas(),
        x="fecha",
        y="ventas",
        color="region",
        title="Ventas diarias por región",
        labels={"fecha": "Fecha", "ventas": "Ventas ($)", "region": "Región"},
    )


def barras_region(df: pl.DataFrame) -> go.Figure:
    """Gráfico de barras del total de ventas por región."""
    resumen = (
        df.group_by("region")
        .agg(pl.col("ventas").sum().alias("ventas_total"))
        .sort("ventas_total", descending=True)
    )
    return px.bar(
        resumen.to_pandas(),
        x="region",
        y="ventas_total",
        color="region",
        title="Ventas totales por región",
        labels={"region": "Región", "ventas_total": "Ventas ($)"},
    )


def barras_producto(df: pl.DataFrame) -> go.Figure:
    """Gráfico de barras del total de ventas por producto."""
    resumen = (
        df.group_by("producto")
        .agg(pl.col("ventas").sum().alias("ventas_total"))
        .sort("ventas_total", descending=True)
    )
    return px.bar(
        resumen.to_pandas(),
        x="producto",
        y="ventas_total",
        color="producto",
        title="Ventas totales por producto",
        labels={"producto": "Producto", "ventas_total": "Ventas ($)"},
    )


def scatter_ventas_clientes(df: pl.DataFrame) -> go.Figure:
    """Dispersión de ventas vs clientes, coloreado por región."""
    return px.scatter(
        df.to_pandas(),
        x="clientes",
        y="ventas",
        color="region",
        symbol="producto",
        title="Ventas vs Clientes",
        labels={
            "clientes": "Clientes",
            "ventas": "Ventas ($)",
            "region": "Región",
            "producto": "Producto",
        },
        trendline="ols",
    )


def histograma_ventas(df: pl.DataFrame) -> go.Figure:
    """Histograma de distribución de ventas."""
    return px.histogram(
        df.to_pandas(),
        x="ventas",
        color="region",
        nbins=30,
        title="Distribución de ventas",
        labels={"ventas": "Ventas ($)", "count": "Frecuencia"},
        barmode="overlay",
        opacity=0.7,
    )
