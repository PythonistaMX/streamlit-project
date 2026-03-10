import polars as pl

from src.datos import (
    REGIONES,
    generar_ventas,
    resumen_por_producto,
    resumen_por_region,
)


class TestGenerarVentas:
    def test_shape_defecto(self):
        df = generar_ventas()
        assert df.shape == (365, 5)

    def test_columnas(self):
        df = generar_ventas()
        assert set(df.columns) == {"fecha", "region", "producto", "ventas", "clientes"}

    def test_tipos(self):
        df = generar_ventas()
        assert df["fecha"].dtype == pl.Date
        assert df["ventas"].dtype in (pl.Int32, pl.Int64)
        assert df["clientes"].dtype in (pl.Int32, pl.Int64)
        assert df["region"].dtype == pl.String
        assert df["producto"].dtype == pl.String

    def test_rango_ventas(self):
        df = generar_ventas()
        assert df["ventas"].min() >= 1_000
        assert df["ventas"].max() <= 10_000

    def test_rango_clientes(self):
        df = generar_ventas()
        assert df["clientes"].min() >= 10
        assert df["clientes"].max() <= 200

    def test_regiones_validas(self):
        df = generar_ventas()
        valores = set(df["region"].unique().to_list())
        assert valores.issubset(set(REGIONES))

    def test_reproducible(self):
        df1 = generar_ventas(seed=0)
        df2 = generar_ventas(seed=0)
        assert df1.equals(df2)

    def test_seed_diferente(self):
        df1 = generar_ventas(seed=1)
        df2 = generar_ventas(seed=2)
        assert not df1.equals(df2)

    def test_n_personalizado(self):
        df = generar_ventas(n=10)
        assert df.shape[0] == 10

    def test_sin_nulos(self):
        df = generar_ventas()
        assert df.null_count().sum_horizontal().item() == 0


class TestResumenPorRegion:
    def test_columnas(self):
        df = resumen_por_region(generar_ventas())
        assert set(df.columns) == {
            "region",
            "ventas_total",
            "ventas_promedio",
            "clientes_total",
            "registros",
        }

    def test_ordenado_descendente(self):
        df = resumen_por_region(generar_ventas())
        totales = df["ventas_total"].to_list()
        assert totales == sorted(totales, reverse=True)

    def test_sin_nulos(self):
        df = resumen_por_region(generar_ventas())
        assert df.null_count().sum_horizontal().item() == 0


class TestResumenPorProducto:
    def test_columnas(self):
        df = resumen_por_producto(generar_ventas())
        assert set(df.columns) == {"producto", "ventas_total", "ventas_promedio"}

    def test_ordenado_descendente(self):
        df = resumen_por_producto(generar_ventas())
        totales = df["ventas_total"].to_list()
        assert totales == sorted(totales, reverse=True)
