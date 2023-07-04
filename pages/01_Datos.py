import streamlit as st
import pandas as pd

# Leemos el archivo
df = pd.read_csv("Datasets_sql/df_final.csv")
# Hacemos unas últimas transformaciones
df["incomeValue"] = df["incomeValue"].str.strip()
df.drop(["idIncome", "idPopulation"], axis=1, inplace=True)

# Título de la página
st.title("Análisis de datos con Streamlit")
st.write("---")

# Visualización de la tabla
st.subheader("Tabla de datos")
st.dataframe(df)

# Dimensión a mostrar (Filas o Columnas)
dim = st.radio("Dimensión a mostrar:", ("Filas", "Columnas"), index=0)

if dim == "Filas":
    st.write(f"Cantidad de registros: {df.shape[0]}")
else:
    st.write(f"Cantidad de columnas: {df.shape[1]}")

st.write("---")

# Vista de datos (Head o Tail)
st.subheader("Vista de datos")

show_head = st.checkbox("Mostrar Head")
show_tail = st.checkbox("Mostrar Tail")

if show_head:
    st.write("Head:")
    st.dataframe(df.head())

if show_tail:
    st.write("Tail:")
    st.dataframe(df.tail())

st.write("---")

# Filtrado por país
countries_list = sorted(df["country"].unique().tolist())
selected_country = st.selectbox("Filtrar por país:", countries_list)
df_filtered = df[df["country"] == selected_country]

st.subheader("Datos filtrados por país")
st.dataframe(df_filtered)

st.write("---")

# Variable a observar: Top 5 Países con mayor y menor score
df_grouped_max = df[["country", "score"]].groupby(["country"]).mean().sort_values(by="score", ascending=False)
df_rounded_max = df_grouped_max.applymap(lambda x: round(x, 2))

df_grouped_min = df[["country", "score"]].groupby(["country"]).mean().sort_values(by="score", ascending=True)
df_rounded_min = df_grouped_min.applymap(lambda x: round(x, 2))

# Mostrar en columnas
col1, col2 = st.columns(2)
col1.write("Top 5 países con el mayor puntaje de felicidad")
col1.dataframe(df_rounded_max.head())
col2.write("Top 5 países con el menor puntaje de felicidad")
col2.dataframe(df_rounded_min.head())

st.write("---")

# Top 5 Países con mayor y menor población
df_population_max = df[["country", "population"]].groupby(["country"]).mean().sort_values(by="population", ascending=False).reset_index()
df_population_min = df[["country", "population"]].groupby(["country"]).mean().sort_values(by="population", ascending=True).reset_index()
df_population_max.index += 1
df_population_min.index += 1

col3, col4 = st.columns(2)
col3.write("Top 5 países con la mayor población")
col3.dataframe(df_population_max["country"].head())
col4.write("Top 5 países con la menor población")
col4.dataframe(df_population_min["country"].head())

st.write("---")

