"""Carga y generación de datos con Polars.

Este módulo no importa streamlit, lo que permite testearlo de forma aislada.
"""

from datetime import date, timedelta

import numpy as np
import polars as pl

REGIONES = ["Norte", "Sur", "Este", "Oeste"]
PRODUCTOS = ["Producto A", "Producto B", "Producto C"]
N_DIAS = 365


def generar_ventas(seed: int = 42, n: int = N_DIAS) -> pl.DataFrame:
    """Genera un DataFrame de ventas diarias sintéticas.

    Args:
        seed: Semilla para reproducibilidad.
        n:    Número de registros.

    Returns:
        DataFrame con columnas: fecha, region, producto, ventas, clientes.
    """
    rng = np.random.default_rng(seed)
    start = date(2024, 1, 1)

    return pl.DataFrame(
        {
            "fecha": [(start + timedelta(days=i)).isoformat() for i in range(n)],
            "region": rng.choice(REGIONES, n).tolist(),
            "producto": rng.choice(PRODUCTOS, n).tolist(),
            "ventas": rng.integers(1_000, 10_000, n).tolist(),
            "clientes": rng.integers(10, 200, n).tolist(),
        }
    ).with_columns(pl.col("fecha").str.to_date())


def resumen_por_region(df: pl.DataFrame) -> pl.DataFrame:
    """Agrega ventas y clientes totales por región."""
    return (
        df.group_by("region")
        .agg(
            pl.col("ventas").sum().alias("ventas_total"),
            pl.col("ventas").mean().round(0).alias("ventas_promedio"),
            pl.col("clientes").sum().alias("clientes_total"),
            pl.len().alias("registros"),
        )
        .sort("ventas_total", descending=True)
    )


def resumen_por_producto(df: pl.DataFrame) -> pl.DataFrame:
    """Agrega ventas totales por producto."""
    return (
        df.group_by("producto")
        .agg(
            pl.col("ventas").sum().alias("ventas_total"),
            pl.col("ventas").mean().round(0).alias("ventas_promedio"),
        )
        .sort("ventas_total", descending=True)
    )
