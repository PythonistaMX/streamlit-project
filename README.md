# Dashboard de Ventas — py311 / N38

Aplicación de ejemplo que ilustra el notebook **N38 — Introducción a Streamlit**
del curso [py311](https://github.com/josechval/py311).

## Estructura del proyecto

```
streamlit-project/
├── .github/workflows/
│   ├── ci.yml          # lint (ruff) + pytest en cada push/PR
│   └── cd.yml          # smoke-test antes del despliegue a Streamlit Cloud
├── .streamlit/
│   └── config.toml     # tema y configuración del servidor
├── pages/
│   ├── 1_dashboard.py  # métricas, filtros, gráficos
│   ├── 2_exploracion.py# dispersión, histograma, resúmenes por tabs
│   └── 3_datos.py      # tabla interactiva y descarga CSV/Parquet
├── src/
│   ├── datos.py        # generación de datos con Polars (sin streamlit)
│   └── graficos.py     # figuras Plotly (sin streamlit)
├── tests/
│   ├── test_datos.py
│   └── test_graficos.py
├── app.py              # página Home (entry point)
├── pyproject.toml      # ruff + pytest + coverage config
├── requirements.txt
└── requirements-dev.txt
```

## Ejecución local

```bash
# Instalar dependencias
pip install -r requirements-dev.txt

# Ejecutar la app
streamlit run app.py
```

La app queda disponible en http://localhost:8501.

## Tests y linting

```bash
# Linting
ruff check .

# Tests con cobertura
pytest --cov=src --cov-report=term-missing
```

## Despliegue en Streamlit Cloud

1. Hacer fork/push a un repositorio de GitHub.
2. Ingresar a https://share.streamlit.io/ y conectar el repositorio.
3. Seleccionar `app.py` como archivo principal.
4. Streamlit Cloud detecta cada push a `main` y redesplega automáticamente.

## Conceptos ilustrados (N38)

| Concepto | Dónde |
| :--- | :--- |
| `st.set_page_config` | Todas las páginas |
| `st.metric` | `app.py`, `pages/1_dashboard.py` |
| `st.dataframe` con Polars | `pages/3_datos.py` |
| `st.plotly_chart` | `pages/1_dashboard.py`, `pages/2_exploracion.py` |
| `st.sidebar` + widgets | `pages/1_dashboard.py` |
| `st.tabs` + `st.expander` | `pages/2_exploracion.py` |
| `st.download_button` | `pages/3_datos.py` |
| `@st.cache_data` | Todas las páginas |
| Polars → Plotly → Streamlit | `src/datos.py` + `src/graficos.py` |
