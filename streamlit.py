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
import streamlit as st

# Contraseña válida (reemplaza con tu contraseña)
contraseña_valida = "mi_contraseña_secreta"

# Función para verificar la contraseña ingresada
def verificar_contraseña(contraseña_ingresada):
    return contraseña_ingresada == contraseña_valida

# Página de inicio
def pagina_inicio():
    st.title("Página de Inicio")
    st.write("Bienvenido a la página de inicio. Por favor, ingrese su contraseña.")

    # Obtener contraseña ingresada por el usuario
    cliente_id = st.text_input('Ingrese su ID de cliente:')

    # Verificar la contraseña
    if cliente_id and verificar_contraseña(cliente_id):
        st.success("Contraseña válida. Acceso concedido.")
        # Establecer el estado de autenticación de la sesión
        st.session_state.autenticado = True
    else:
        st.error('ID de cliente no válido. Intente nuevamente con un ID válido.')

# Página protegida que solo se mostrará si el usuario está autenticado
def pagina_protegida():
    # Verificar si el usuario está autenticado
    if not st.session_state.get('autenticado'):
        st.error("Debe ingresar una contraseña válida en la página de inicio para acceder a esta página.")
        st.stop()

    st.title("Página Protegida")
    st.write("Esta es una página protegida que solo se muestra si el usuario ha ingresado la contraseña válida en la página de inicio.")

# Mostrar la página correspondiente según la ruta de la URL
pagina = st.sidebar.selectbox("Seleccione una página", ["Inicio", "Página Protegida"])

if pagina == "Inicio":
    pagina_inicio()
elif pagina == "Página Protegida":
    pagina_protegida()

# Sección de información
st.subheader("¿Qué puedes encontrar aquí?")
st.write("En esta aplicación, descubrirás 4 secciones:")
st.write("+ **Feedback**: ...")
st.write("+ **Recompra**: ...")
st.write("+ **Vacunas**: ...")
st.write("+ **Cirugia**: ...")

# Línea divisoria
st.markdown("---")
