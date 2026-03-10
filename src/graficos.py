"""Funciones de visualización con Matplotlib y Seaborn.

Todas las funciones reciben un DataFrame de Polars y devuelven un
matplotlib.figure.Figure, compatible con st.pyplot().
No importan streamlit, lo que permite testarlas de forma aislada.
"""

import matplotlib.figure
import matplotlib.pyplot as plt
import polars as pl
import seaborn as sns

sns.set_theme(style="whitegrid")


def linea_ventas(df: pl.DataFrame) -> matplotlib.figure.Figure:
    """Gráfico de línea de ventas diarias por región."""
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(
        data=df.sort("fecha").to_pandas(),
        x="fecha", y="ventas", hue="region", ax=ax,
    )
    ax.set_title("Ventas diarias por región")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Ventas ($)")
    fig.autofmt_xdate()
    fig.tight_layout()
    return fig


def barras_region(df: pl.DataFrame) -> matplotlib.figure.Figure:
    """Gráfico de barras del total de ventas por región."""
    resumen = (
        df.group_by("region")
        .agg(pl.col("ventas").sum().alias("ventas_total"))
        .sort("ventas_total", descending=True)
    )
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=resumen.to_pandas(), x="region", y="ventas_total", ax=ax)
    ax.set_title("Ventas totales por región")
    ax.set_xlabel("Región")
    ax.set_ylabel("Ventas ($)")
    fig.tight_layout()
    return fig


def barras_producto(df: pl.DataFrame) -> matplotlib.figure.Figure:
    """Gráfico de barras del total de ventas por producto."""
    resumen = (
        df.group_by("producto")
        .agg(pl.col("ventas").sum().alias("ventas_total"))
        .sort("ventas_total", descending=True)
    )
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=resumen.to_pandas(), x="producto", y="ventas_total", ax=ax)
    ax.set_title("Ventas totales por producto")
    ax.set_xlabel("Producto")
    ax.set_ylabel("Ventas ($)")
    fig.tight_layout()
    return fig


def scatter_ventas_clientes(df: pl.DataFrame) -> matplotlib.figure.Figure:
    """Dispersión de ventas vs clientes, coloreado por región."""
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(
        data=df.to_pandas(),
        x="clientes", y="ventas", hue="region", style="producto", ax=ax,
    )
    ax.set_title("Ventas vs Clientes")
    ax.set_xlabel("Clientes")
    ax.set_ylabel("Ventas ($)")
    fig.tight_layout()
    return fig


def histograma_ventas(df: pl.DataFrame) -> matplotlib.figure.Figure:
    """Histograma de distribución de ventas por región."""
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(
        data=df.to_pandas(),
        x="ventas", hue="region", bins=30, alpha=0.7, ax=ax,
    )
    ax.set_title("Distribución de ventas")
    ax.set_xlabel("Ventas ($)")
    ax.set_ylabel("Frecuencia")
    fig.tight_layout()
    return fig
