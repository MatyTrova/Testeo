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

st.set_page_config(
    page_title="Dashboard Experiencias",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
    )


db_username = st.secrets["DB_USERNAME"]
db_password = st.secrets["DB_PASSWORD"]
db_host = st.secrets["DB_HOST"]
db_token = st.secrets["DB_TOKEN"]
# Creamos la conexión
conexion_string = f"mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_token}"
engine = create_engine(conexion_string,pool_pre_ping=True)

query = """
    SELECT * 
    FROM experiencias
    WHERE journeyClassName = 'EcommerceFeedbackCompra';
"""
df_sql = pd.read_sql(query, engine)
df_sql.drop("hora",axis=1,inplace=True)
st.dataframe(df_sql)


# Obtener registros positivos, negativo y neutros (para gráfico de torta)
reviews = {"Positivo":     df_sql[df_sql["msgBody"].str.contains("\+")].shape[0] ,
            "Neutro" :      df_sql[df_sql["msgBody"].str.contains("\=")].shape[0] ,
            "Negativo":    df_sql[df_sql["msgBody"].str.contains("\-")].shape[0]
            }

# Reemplazamos para el gráfico de lineas
df_sql.loc[df_sql["msgBody"].str.contains("\+"), "msgBody"] = "Positivo"
df_sql.loc[df_sql["msgBody"].str.contains("\="), "msgBody"] = "Neutro"
df_sql.loc[df_sql["msgBody"].str.contains("\-"), "msgBody"] = "Negativo"
df_filtered = df_sql[
    df_sql["msgBody"].str.contains("Positivo") |
    df_sql["msgBody"].str.contains("Neutro") |
    df_sql["msgBody"].str.contains("Negativo")
].copy()

# Para nube de palabras filtras donde mandan comentario ..


# Tarjetas
cantidad_clientes = len(df_sql["idCliente"].unique())




# Título de la página
st.title("Experiencia de Feedback")

# Imagen
#st.image("ruta/a/tu/imagen.jpg", caption="Imagen de ejemplo", use_column_width=True)
# Línea divisoria
st.markdown("---")
# Encabezado
st.header("Bienvenido :)")
# Sección de información
st.subheader("Explora y descubre")
# Línea divisoria
st.markdown("---")

# Contraseña
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


# Crear 5 tarjetas en la primera fila
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.subheader('Cantidad de conversaciones')
    st.write(cantidad_clientes)
        # Contenido de la tarjeta 1

with col2:
    st.subheader('Conversaciones terminadas')
    st.write("")
        # Contenido de la tarjeta 2

with col3:
    st.subheader('Conversaciones pendientes')
    st.write("")
        # Contenido de la tarjeta 3

with col4:
    st.subheader('Feedbacks positivos')
    st.write("")
        # Contenido de la tarjeta 4

with col5:
    st.subheader('Tarjeta 5')
    st.write("tarjeta5")
        # Contenido de la tarjeta 5

# gráfico de cantidad de conversaciones por fecha
# aquí


col9, col10  = st.columns(2)

# Nube de palabras
#with col9:

# Gráfico de torta   
#with col10:
    
