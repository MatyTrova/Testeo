import streamlit as st
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pymysql


db_username = st.secrets["DB_USERNAME"]
db_password = st.secrets["DB_PASSWORD"]
db_host = st.secrets["DB_HOST"]
db_token = st.secrets["DB_TOKEN"]
# Creamos la conexión
conexion_string = f"mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_token}"
engine = create_engine(conexion_string,pool_pre_ping=True)

query = """
    SELECT *
    FROM clientes;
"""
df_sql = pd.read_sql(query, engine)


st.dataframe(df_sql)


# Título de la página
st.title("****")

# Imagen
#st.image("ruta/a/tu/imagen.jpg", caption="Imagen de ejemplo", use_column_width=True)
# Línea divisoria
st.markdown("---")
# Encabezado
st.header("Bienvenido :)")

# Texto descriptivo
st.write("")

# Sección de información
st.subheader("")
st.write("")
st.write("+")
st.write("+")

st.subheader("Explora y descubre")

# Línea divisoria
st.markdown("---")

# Créditos
st.text("D")

# Query de prueba 


# Simulación de datos y configuración de clientes
# Puedes reemplazar esta simulación con una base de datos o algún otro mecanismo de almacenamiento real
clientes = {
    'cliente1': {
        'nombre': 'Cliente 1',
        'datos': [1, 2, 3, 4, 5],
        'configuracion': {
            'color': 'blue',
            'mostrar_grafico': True
        }
    },
    'cliente2': {
        'nombre': 'Cliente 2',
        'datos': [6, 7, 8, 9, 10],
        'configuracion': {
            'color': 'green',
            'mostrar_grafico': False
        }
    }
}

# Autenticación del cliente
cliente_id = st.text_input('Ingrese su ID de cliente:')
if cliente_id not in clientes:
    st.error('ID de cliente no válido. Intente nuevamente con un ID válido.')
    st.stop()

# Obtener datos y configuración del cliente autenticado
cliente_actual = clientes[cliente_id]
nombre_cliente = cliente_actual['nombre']
datos_cliente = cliente_actual['datos']
configuracion_cliente = cliente_actual['configuracion']

# Mostrar el dashboard personalizado
st.title(f'Dashboard de {nombre_cliente}')

#funcion para hacer df, usando size para la cantidad en los metodos de numpy
def hacerDf(size):
    df = pd.DataFrame()
    df["numero"] = np.random.choice(["123","4345","75375423","1243e125","624532","67453","3543512","523523"],size)
    df["edad"] = np.random.randint(1,21,size)
    df["nube de palabras"] = np.random.choice(["muy bueno","si","me gusta","muy buen producto","me gustó","me gustó", "mal producto" ,"buen producto" ,"sin mensaje", "me gustó", "excelente" ,"buenísimo" ,"no se"],size)
    dates = pd.date_range("01-01-2023","07-01-2023")
    df["fecha"] = np.random.choice(dates,size)
    return df
df = hacerDf(200)

# Crear 5 tarjetas en la primera fila
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.subheader('Tarjeta 1')
    st.write("tarjeta1")
        # Contenido de la tarjeta 1

with col2:
    st.subheader('Tarjeta 2')
    st.write("tarjeta2")
        # Contenido de la tarjeta 2

with col3:
    st.subheader('Tarjeta 3')
    st.write("tarjeta3")
        # Contenido de la tarjeta 3

with col4:
    st.subheader('Tarjeta 4')
    st.write("tarjeta4")
        # Contenido de la tarjeta 4

with col5:
    st.subheader('Tarjeta 5')
    st.write("tarjeta5")
        # Contenido de la tarjeta 5

# Agregar el gráfico de líneas en la segunda fila, centrado
st.write('---')
st.subheader('Gráfico de Líneas')
# query
# Filtrar utilizando expresiones regulares
filtro_bueno1 = df["nube de palabras"].str.contains("buen", regex=True)
filtro_bueno2 = df["nube de palabras"].str.contains("me gust", regex=True)
filtro_bueno3 = df["nube de palabras"] == "si"
filtro_bueno4 = df["nube de palabras"].str.contains("excelente", regex=True)
resultados1 = df[filtro_bueno1]
resultados2 = df[filtro_bueno2]
resultados3 = df[filtro_bueno3]
resultados4 = df[filtro_bueno4]
bueno = pd.concat([resultados1,resultados2,resultados3,resultados4])
filtro_neutro = df["nube de palabras"].str.contains("no se", regex=True)
filtro_neutro2= df["nube de palabras"].str.contains("sin mensaje", regex=True)
resultados6 = df[filtro_neutro]
resultados7 = df[filtro_neutro2]
neutro = pd.concat([resultados6, resultados7])
# Filtrar utilizando expresiones regulares
filtro_malo = df["nube de palabras"].str.contains("mal", regex=True)
resultados5 = df[filtro_malo]
bad = resultados5
bueno["nube de palabras"] = "Positivo"
bad["nube de palabras"] = "Negativo"
neutro["nube de palabras"] = "Neutro"
df_time = pd.concat([bueno,bad])
df_time["fecha"] =  df_time["fecha"].dt.month_name()
xx = df_time[["nube de palabras","fecha"]].groupby(["fecha","nube de palabras"]).value_counts().reset_index()
# Crear un gráfico de líneas utilizando Seaborn
sns.set()
sns.set_palette("Set1")
sns.lineplot(data=xx, x='fecha', y='count', hue='nube de palabras', linewidth=5)
# Configurar el título y etiquetas de los ejes
plt.title('Reviews Mensuales')
plt.xlabel('')
plt.ylabel('')
# Rotar las etiquetas del eje x para una mejor visualización
plt.xticks(rotation=45)
plt.legend(title='Categorías', title_fontsize='12', loc='center left', bbox_to_anchor=(1, 1), fontsize='12')
# Mostrar el gráfico de líneas
st.pyplot(plt)

# Agregar el gráfico pequeño en el centro de la tercera fila
#col6, col7, col8 = st.columns([1, 4, 1])

#with col6:
 #   st.write('')

#with col7:
#    st.subheader('Gráfico Pequeño')
#    st.pyplot(plt)
    # Contenido del gráfico pequeño

#with col8:
 #   st.write('')

# Agregar los 3 gráficos cuadrados en la cuarta fila
col9, col10  = st.columns(2)

with col9:
    st.subheader('Nube de palabras')
    

        # Crear una lista de palabras
        # Unir todos los textos en una sola cadena
    texto_completo = ' '.join(df["nube de palabras"])
        # Crear el objeto WordCloud con fondo blanco
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(texto_completo)

        # Configurar el gráfico
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')

        # Mostrar el gráfico de nube de palabras
    st.pyplot(plt)
        # Contenido del gráfico cuadrado 1

with col10:
    st.subheader('Gráfico Cuadrado 2')
        # Contenido del gráfico cuadrado 2
