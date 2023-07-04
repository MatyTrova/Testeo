# Librerias a utilizar
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


# Carga de datos
df = pd.read_csv("Datasets_sql/df_final.csv")
df["incomeValue"] = df["incomeValue"].str.strip()
df.drop(["idIncome", "idPopulation"], axis=1, inplace=True)

# Presentación
st.write("---")
st.write("# *Análisis de dispersión entre GDP y Happiness Score*")
st.write("---")
st.write("En este análisis, exploraremos la relación entre el Producto Interno Bruto (GDP) y el puntaje de felicidad.")

# Selección del año
years = [2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015]
selected_year = st.selectbox('Selecciona un año:', years)
df_filtrado_año = df[df["year"] == selected_year]

# Gráfico de dispersión
plt.figure(figsize=(10, 8))
sns.scatterplot(data=df_filtrado_año, y='gdpPerCapita', x='score', color='brown', alpha=1, s=40)
plt.ylabel('GDP Per Capita', fontsize=12)
plt.xlabel('Happiness Score (Felicidad)', fontsize=12)
plt.title('¿El dinero da la felicidad?', fontsize=14)
plt.grid(True)
scatter_plot = plt.gcf()
st.pyplot(scatter_plot)

# Mensajes explicativos
st.write("+ Se puede observar que hay una alta correlación entre ambas variables.")
st.write("+ Esto sugiere que a mayor GDP, mayor Happiness Score (Felicidad).")
st.write("---")

# Presentación 2do gráfico
st.write("# *Análisis de la evolución de variables por país*")
st.write("---")

# Selección de país
countries_list = sorted(df["country"].unique().tolist())
selected_country = st.selectbox("Selecciona un país:", countries_list)
df_filtrado_pais = df[df["country"] == selected_country]
# Instanciamos en "None", lo utilizaremos más adelante
selected_country2 = None

# Checkbox para comparar países
if st.checkbox("Comparar países"):
    selected_country2 = st.selectbox("Selecciona un segundo país", countries_list)
    df_filtrado_pais2 = df[df["country"] == selected_country2]

# Variable a observar
variables = ["Felicidad", "GDP", "Esperanza de vida", "Libertad", "Confianza", "Generosidad", "Población"]
selected_variable = st.radio("Variable a observar:", variables,horizontal=True)
aux = ""
color = ""
# Establecemos el color y el aux según la variable seleccionada
if selected_variable == "Felicidad" :
    aux = "score"
    color = "#FFD700"
elif selected_variable == "GDP" :
    aux = "gdpPerCapita"
    color = "blue"
if selected_variable == "Esperanza de vida" :
    aux = "lifeExpectancy"
    color = "green"
if selected_variable == "Libertad" :
    aux = "freedom"
    color = "skyblue"
if selected_variable == "Confianza" :
    aux = "trust"
    color = "purple"
if selected_variable == "Generosidad" :
    aux = "generosity"
    color = "#FFC0CB"
if selected_variable == "Población" :
    aux = "population"
    color = "#FF0000"


# Si no se selecciono para comparar países mostrará este gráfico
if selected_country2 == None:
    # Gráfico de líneas
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.set_palette('Dark2')
    sns.lineplot(data=df_filtrado_pais, x='year', y=aux, marker='o', markersize=7, linewidth=4, ci=None, ax=ax,color=color)
    ax.set_xlabel('Año',fontsize=12)
    ax.set_ylabel('Valor')
    ax.set_title(f'Evolución de la variable "{selected_variable}" a lo largo de los años')
    ax.grid(True)
    st.pyplot(fig)

# Sinó mostrará este gráfico    
else:
     # Gráfico de líneas (comparación)
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.set_palette('Dark2')
    # País 1
    sns.lineplot(data=df_filtrado_pais, x='year', y=aux, marker='o', markersize=7,label = selected_country, linewidth=4, ci=None, ax=ax,color="blue")
    # País 2
    sns.lineplot(data=df_filtrado_pais2, x='year', y=aux, marker='o', markersize=7,label = selected_country2, linewidth=4, ci=None, ax=ax, color='green')
    ax.set_xlabel('Año',fontsize=12)
    ax.set_ylabel('Valor')
    ax.set_title(f'Evolución de la variable "{selected_variable}" a lo largo de los años')
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    ax.grid(True)
    st.pyplot(fig)