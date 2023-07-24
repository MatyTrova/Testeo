import streamlit as st

st.set_page_config(
    page_title="Dashboard Experiencias",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
    )

# Título de la página
st.title("**Dashboard Experiencias**")

st.markdown("---")
# Imagen
#st.image("", use_column_width=True)
# Línea divisoria
st.markdown("---")

# Encabezado
st.header("¡Bienvenido, ... !")

# Texto descriptivo
st.write("Te damos la bienvenida a ....")

# Sección de información
st.subheader("¿Qué puedes encontrar aquí?")
st.write("En esta aplicación, descubrirás 4 secciones:")
st.write("+ **Feedback**: ...")
st.write("+ **Recompra**: ...")
st.write("+ **Vacunas**: ...")
st.write("+ **Cirugia**: ...")

# Línea divisoria
st.markdown("---")