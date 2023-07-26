import streamlit as st
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from wordcloud import WordCloud
import pymysql
from matplotlib.dates import DateFormatter, DayLocator

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
        WHERE journeyClassName IN ('EcommerceRecompraDeProducto' ,'EcommerceRecompraParaHoy') ;
        """
df_sql = pd.read_sql(query, engine)
df_sql.drop("hora",axis=1,inplace=True)
st.dataframe(df_sql)

# Tarjetas
cantidad_clientes = len(df_sql["idCliente"].unique())


intencion_recompra = len(df_sql.loc[(df_sql["journeyClassName"] == "EcommerceRecompraDeProducto") & (df_sql["journeyStep"] == "RespuestaMensajeInicial") & (df_sql["msgBody"] == "Sí, necesito comprarlo de nuevo")]) 



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


# Importar la biblioteca de Streamlit
import streamlit as st

# Crear 5 tarjetas en la primera fila
col1, col2, col3, col4, col5 = st.columns(5)

# Estilos CSS personalizados
custom_css = """
<style>
    .tarjeta {
        padding: 20px;
        border-radius: 5px;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
        background-color: #f9f9f9;
        text-align: center;
    }
    .subheader {
        font-size: 20px;
        font-weight: bold;
        color: #333;
    }
    .contenido {
        font-size: 24px;
        color: #555;
    }
</style>
"""

# Agregar el estilo CSS personalizado utilizando st.markdown
st.markdown(custom_css, unsafe_allow_html=True)

# Contenido de las tarjetas
with col1:
    st.markdown('<div class="tarjeta">', unsafe_allow_html=True)
    st.subheader('Cantidad de conversaciones')
    st.markdown('<div class="contenido">', unsafe_allow_html=True)
    st.write(cantidad_clientes)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="tarjeta">', unsafe_allow_html=True)
    st.subheader('Conversaciones terminadas')
    st.markdown('<div class="contenido">', unsafe_allow_html=True)
    st.write("")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="tarjeta">', unsafe_allow_html=True)
    st.subheader('Conversaciones pendientes')
    st.markdown('<div class="contenido">', unsafe_allow_html=True)
    st.write("")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="tarjeta">', unsafe_allow_html=True)
    st.subheader('Intención de recompra')
    st.markdown('<div class="contenido">', unsafe_allow_html=True)
    st.write(intencion_recompra)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col5:
    st.markdown('<div class="tarjeta">', unsafe_allow_html=True)
    st.subheader('Disposición de recibir ofertas')
    st.markdown('<div class="contenido">', unsafe_allow_html=True)
    st.write("")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# gráfico de cantidad de conversaciones por fecha
df_sql['fecha'] = pd.to_datetime(df_sql['fecha'])
registros_por_dia = df_sql['fecha'].value_counts().reset_index()
registros_por_dia.columns = ['fecha', 'cantidad']
plt.figure(figsize=(6, 4))  
sns.set(style="whitegrid")
ax = sns.lineplot(x="fecha", y="cantidad", marker='o', color='b',data=registros_por_dia)
plt.xlabel('')
plt.ylabel('')
date_form = DateFormatter("%d/%m")
ax.xaxis.set_major_formatter(date_form)
plt.tight_layout() 
plt.show()
gráfico1 = plt.gcf()
st.write("# Total de conversaciones")
st.pyplot(gráfico1)


col9, col10  = st.columns(2)

# Nube de palabras
#with col9:

# Gráfico de torta   
#with col10:
    
