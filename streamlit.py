import streamlit as st

st.set_page_config(
    page_title="Dashboard Experiencias",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
    )

import streamlit as st

# Contraseña válida (reemplaza con tu contraseña)
contraseña_valida = "mi_contraseña_secreta"

# Función para verificar la contraseña ingresada
def verificar_contraseña(contraseña_ingresada):
    return contraseña_ingresada == contraseña_valida

# Función para mostrar el contenido de la página Feedback
def mostrar_feedback():
    st.title("Página de Feedback")
    # Aquí puedes agregar el contenido específico de la página Feedback

# Función para mostrar el contenido de la página Recompra
def mostrar_recompra():
    st.title("Página de Recompra")
    # Aquí puedes agregar el contenido específico de la página Recompra

# Función principal
def main():

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

    # Opciones del sidebar para seleccionar página
    opciones_paginas = ["Inicio", "Feedback", "Recompra"]
    pagina_seleccionada = st.sidebar.selectbox("Selecciona una página:", opciones_paginas)

    # Mostrar el contenido de la página seleccionada
    if pagina_seleccionada == "Inicio":
        pagina_inicio()
    elif pagina_seleccionada == "Feedback":
        pagina_protegida()
        mostrar_feedback()
    elif pagina_seleccionada == "Recompra":
        pagina_protegida()
        mostrar_recompra()

# Iniciar la aplicación
if __name__ == "__main__":
    main()

