import plotly.graph_objects as go
import pytest

from src.datos import generar_ventas
from src.graficos import (
    barras_producto,
    barras_region,
    histograma_ventas,
    linea_ventas,
    scatter_ventas_clientes,
)


@pytest.fixture(scope="module")
def df():
    return generar_ventas(n=50)


class TestLinea:
    def test_retorna_figura(self, df):
        assert isinstance(linea_ventas(df), go.Figure)

    def test_tiene_trazas(self, df):
        fig = linea_ventas(df)
        assert len(fig.data) > 0

    def test_titulo(self, df):
        fig = linea_ventas(df)
        assert "ventas" in fig.layout.title.text.lower()


class TestBarrasRegion:
    def test_retorna_figura(self, df):
        assert isinstance(barras_region(df), go.Figure)

    def test_tiene_trazas(self, df):
        fig = barras_region(df)
        assert len(fig.data) > 0


class TestBarrasProducto:
    def test_retorna_figura(self, df):
        assert isinstance(barras_producto(df), go.Figure)

    def test_tiene_trazas(self, df):
        fig = barras_producto(df)
        assert len(fig.data) > 0


class TestScatter:
    def test_retorna_figura(self, df):
        assert isinstance(scatter_ventas_clientes(df), go.Figure)

    def test_tiene_trazas(self, df):
        fig = scatter_ventas_clientes(df)
        assert len(fig.data) > 0


class TestHistograma:
    def test_retorna_figura(self, df):
        assert isinstance(histograma_ventas(df), go.Figure)

    def test_tiene_trazas(self, df):
        fig = histograma_ventas(df)
        assert len(fig.data) > 0
