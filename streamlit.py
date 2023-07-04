import streamlit as st
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine



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
conexion_string = mysql+pymysql://root:1234@127.0.0.1:3306/world
engine = create_engine(conexion_string)
query = """
    SELECT cc.Name as pais, count(c.ID) as cantidad_ciudades 
    FROM city c
    JOIN country cc ON (c.CountryCode = cc.Code)
    GROUP BY pais
    HAVING cantidad_ciudades > 100
    ORDER BY 2 DESC;
"""
df_sql = pd.read_sql(query, engine)
# Mostrar el dataframe
st.dataframe(df_sql)
