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

st.set_page_config(
    page_title="Dashboard Experiencias",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
    )

# Obtener contraseña ingresada por el usuario
businessnumber = st.text_input('Password:')
# Función principal
def main():

    db_username = st.secrets["DB_USERNAME"]
    db_password = st.secrets["DB_PASSWORD"]
    db_host = st.secrets["DB_HOST"]
    db_token = st.secrets["DB_TOKEN"]
        # Creamos la conexión
    conexion_string = f"mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_token}"
    engine = create_engine(conexion_string,pool_pre_ping=True)
    query = """
            SELECT DISTINCT businessPhoneNumber
            FROM clientes ;
    """
    df_password = pd.read_sql(query, engine)

    # Función para verificar la contraseña ingresada
    def verificar_contraseña(businessnumber):
        for elemento in df_password["businessPhoneNumber"]:
            if (businessnumber == str(elemento)):
                return True
            else:
                pass
        return False  
    
    # Página de inicio
    def pagina_inicio():
        st.title("Página de Inicio")
        st.write("Bienvenido a la página de inicio. Por favor, ingrese su business number.")
        st.write("passwords = 15550199539 , 56992717910 , 56945904447 ")

        # Verificar la contraseña
        if businessnumber and verificar_contraseña(businessnumber):
            st.success("Contraseña válida. Acceso concedido.")
            # Establecer el estado de autenticación de la sesión
            st.session_state.autenticado = True
            # Creamos la conexión
        else:
            st.error('Password no válido. Intente nuevamente con un número válido.')

    # FEEDBACK
    def mostrar_feedback():
        # Verificar si el usuario está autenticado
        if not st.session_state.get('autenticado'):
            st.error("Debe ingresar una contraseña válida en la página de inicio para acceder a esta página.")
            st.stop()
        st.title("Dashboard Feedback")
        db_username = st.secrets["DB_USERNAME"]
        db_password = st.secrets["DB_PASSWORD"]
        db_host = st.secrets["DB_HOST"]
        db_token = st.secrets["DB_TOKEN"]
        # Creamos la conexión
        conexion_string = f"mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_token}"
        engine = create_engine(conexion_string,pool_pre_ping=True)
        # Query de Feedback
        query = f"""
            SELECT e.* , c.businessPhoneNumber, c.clientName
            FROM experiencias e
            JOIN clientes c ON (e.idCliente = c.idCliente)
            WHERE e.journeyClassName = 'EcommerceFeedbackCompra' AND c.businessPhoneNumber = {businessnumber} ;
        """
        df_feedback = pd.read_sql(query, engine)
        df_feedback.drop("hora",axis=1,inplace=True)
        st.write("Dataframe")
        st.dataframe(df_feedback)
        st.write("---")

        reviews = {"Positivo":     df_feedback[df_feedback["msgBody"].str.contains("\+")].shape[0] ,
                    "Neutro" :      df_feedback[df_feedback["msgBody"].str.contains("\=")].shape[0] ,
                    "Negativo":    df_feedback[df_feedback["msgBody"].str.contains("\-")].shape[0]
                    }
        # Reemplazamos para el gráfico de lineas
        df_feedback.loc[df_feedback["msgBody"].str.contains("\+"), "msgBody"] = "Positivo"
        df_feedback.loc[df_feedback["msgBody"].str.contains("\="), "msgBody"] = "Neutro"
        df_feedback.loc[df_feedback["msgBody"].str.contains("\-"), "msgBody"] = "Negativo"
        df_filtered = df_feedback[
            df_feedback["msgBody"].str.contains("Positivo") |
            df_feedback["msgBody"].str.contains("Neutro") |
            df_feedback["msgBody"].str.contains("Negativo")
        ].copy()

        # Tarjetas
        cantidad_clientes = len(df_feedback["idCliente"].unique())


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
        </style>
        """

        # Agregar el estilo CSS personalizado utilizando st.markdown
        st.markdown(custom_css, unsafe_allow_html=True)

        hola = "gatito azul"
        # Variable de ejemplo con estilos en línea
        tarjeta1 = f'<div class="tarjeta" style="font-size: 30px; color: #00008B;">{cantidad_clientes}</div>'
        tarjeta2 = f'<div class="tarjeta" style="font-size: 30px; color: #00008B;">{hola}</div>'
        tarjeta3 = f'<div class="tarjeta" style="font-size: 30px; color: #00008B;">{hola}</div>'
        tarjeta4 = f'<div class="tarjeta" style="font-size: 30px; color: #00008B;">{hola}</div>'
        tarjeta5 = f'<div class="tarjeta" style="font-size: 30px; color: #00008B;">{hola}</div>'

        # Contenido de las tarjetas
        with col1:
            st.markdown('<div class="subheader">Cantidad de conversaciones</div>', unsafe_allow_html=True)
            st.markdown(tarjeta1, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="subheader">Conversaciones terminadas</div>', unsafe_allow_html=True)
            st.markdown(tarjeta2, unsafe_allow_html=True)
            st.markdown('</div></div>', unsafe_allow_html=True)

        with col3:
            st.markdown('<div class="subheader">Conversaciones incompletas</div>', unsafe_allow_html=True)
            st.markdown(tarjeta3, unsafe_allow_html=True)
            st.markdown('</div></div>', unsafe_allow_html=True)

        with col4:
            st.markdown('<div class="subheader">Feedbacks positivos</div>', unsafe_allow_html=True)
            st.markdown(tarjeta4, unsafe_allow_html=True)
            st.markdown('</div></div>', unsafe_allow_html=True)

        with col5:
            st.markdown('<div class="subheader">Comentarios recibidos</div>', unsafe_allow_html=True)
            st.markdown(tarjeta5, unsafe_allow_html=True)
            st.markdown('</div></div>', unsafe_allow_html=True)
            ver_comentarios = st.checkbox("Mostrar comentarios")

        st.write("---")

        col6, col7  = st.columns([2,1])

        with col6 :
            df_filtered['fecha'] = pd.to_datetime(df_filtered['fecha'])
            reviews_por_dia = df_filtered[['fecha',"msgBody"]].value_counts().reset_index()
            reviews_por_dia1 = reviews_por_dia[reviews_por_dia["msgBody"].str.contains("Positivo")]
            reviews_por_dia2 = reviews_por_dia[reviews_por_dia["msgBody"].str.contains("Negativo")]
            fig, ax = plt.subplots()
            fig.set_size_inches(6, 3)  
            sns.set(style="whitegrid")
            ax = sns.lineplot(x="fecha", y="count", marker='o', color='green',data=reviews_por_dia1, label="Positivo",linewidth=4)
            plt.plot(reviews_por_dia2['fecha'], reviews_por_dia2['count'], marker='o', color='blue', label='Negativo',linewidth=4)
            plt.xlabel('')
            plt.ylabel('')
            plt.legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0)
            date_form = DateFormatter("%d/%m")
            ax.xaxis.set_major_formatter(date_form)
            #plt.tight_layout() 
            gráfico1 = plt.gcf()
            st.write("### **Total de reviews**")
            st.pyplot(gráfico1)

        with col7:
            # Extrae las etiquetas y los valores del diccionario
            etiquetas = list(reviews.keys())
            valores = list(reviews.values())
            # Colores para el gráfico
            colores = ['tab:green', 'tab:grey', 'tab:blue']
            plt.figure(figsize=(6, 4))  
            sns.set(style="whitegrid")
            # Crea el gráfico de torta
            plt.pie(valores, labels=etiquetas, colors=colores, autopct='%1.1f%%', startangle=90)
            plt.axis('equal')  # Hace que el gráfico sea circular
            gráfico11 = plt.gcf()
            st.write("### **Porcentaje de reviews**")
            st.pyplot(gráfico11)
      
        st.write("---")
        
        if ver_comentarios:
            st.markdown("Comentarios:")
            st.write("acá los escribimos")

    

    # RECOMPRA
    def mostrar_recompra():
        # Verificar si el usuario está autenticado
        if not st.session_state.get('autenticado'):
            st.error("Debe ingresar una contraseña válida en la página de inicio para acceder a esta página.")
            st.stop()
        st.title("Dashboard Recompra")    
        db_username = st.secrets["DB_USERNAME"]
        db_password = st.secrets["DB_PASSWORD"]
        db_host = st.secrets["DB_HOST"]
        db_token = st.secrets["DB_TOKEN"]
        conexion_string = f"mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_token}"
        engine = create_engine(conexion_string,pool_pre_ping=True)
        query = f"""
                SELECT e.*, c.businessPhoneNumber, c.clientName
                FROM experiencias e
                JOIN clientes c ON (e.idCliente = c.idCliente)
                WHERE e.journeyClassName IN ('EcommerceRecompraDeProducto' ,'EcommerceRecompraParaHoy') AND c.businessPhoneNumber = {businessnumber} ;
                """
        df_recompra = pd.read_sql(query, engine)
        df_recompra.drop("hora",axis=1,inplace=True)
        st.write("Dataframe")
        st.dataframe(df_recompra)

        

        # Tarjetas
        cantidad_clientes = len(df_recompra["idCliente"].unique())
        intencion_recompra = len(df_recompra.loc[(df_recompra["journeyClassName"] == "EcommerceRecompraDeProducto") & (df_recompra["journeyStep"] == "RespuestaMensajeInicial") & (df_recompra["msgBody"] == "Sí, necesito comprarlo de nuevo")]) 

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
        hola = "gatito azul"
        # Variable de ejemplo con estilos en línea
        tarjeta1 = f'<div class="tarjeta" style="font-size: 30px; color: #00008B;">{cantidad_clientes}</div>'
        tarjeta2 = f'<div class="tarjeta" style="font-size: 30px; color: #00008B;">{hola}</div>'
        tarjeta3 = f'<div class="tarjeta" style="font-size: 30px; color: #00008B;">{hola}</div>'
        tarjeta4 = f'<div class="tarjeta" style="font-size: 30px; color: #00008B;">{intencion_recompra}</div>'
        tarjeta5 = f'<div class="tarjeta" style="font-size: 30px; color: #00008B;">{hola}</div>'

        # Contenido de las tarjetas
        with col1:
            st.markdown(tarjeta1, unsafe_allow_html=True)
            st.markdown('<div class="subheader">Cantidad de conversaciones</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown(tarjeta2, unsafe_allow_html=True)
            st.markdown('<div class="subheader">Conversaciones terminadas</div>', unsafe_allow_html=True)  # Utilizar la clase "mi-variable"
            st.markdown('</div></div>', unsafe_allow_html=True)

        with col3:
            st.markdown(tarjeta3, unsafe_allow_html=True)
            st.markdown('<div class="subheader">Conversaciones pendientes</div>', unsafe_allow_html=True)
            st.markdown('</div></div>', unsafe_allow_html=True)

        with col4:
            st.markdown(tarjeta4, unsafe_allow_html=True)
            st.markdown('<div class="subheader">Intención de recompra</div>', unsafe_allow_html=True)
            st.markdown('</div></div>', unsafe_allow_html=True)

        with col5:
            st.markdown(tarjeta5, unsafe_allow_html=True)
            st.markdown('<div class="subheader">Disposición de recibir ofertas</div>', unsafe_allow_html=True)
            st.markdown('</div></div>', unsafe_allow_html=True)

        # gráfico de cantidad de conversaciones por fecha
        df_recompra['fecha'] = pd.to_datetime(df_recompra['fecha'])
        registros_por_dia = df_recompra['fecha'].value_counts().reset_index()
        registros_por_dia.columns = ['fecha', 'cantidad']
        fig, ax = plt.subplots()
        fig.set_size_inches(6, 3) 
        sns.set(style="whitegrid")
        ax = sns.lineplot(x="fecha", y="cantidad", marker='o', color='b',data=registros_por_dia,linewidth=4)
        plt.xlabel('')
        plt.ylabel('')
        date_form = DateFormatter("%d/%m")
        ax.xaxis.set_major_formatter(date_form)
        #plt.tight_layout() 
        plt.show()
        gráfico2 = plt.gcf()
        st.write("# Total de conversaciones")
        st.pyplot(gráfico2)


        col9, col10  = st.columns(2)

        # Nube de palabras
        #with col9:

        # Gráfico de torta   
        #with col10:

    # Opciones del sidebar para seleccionar página
    opciones_paginas = ["Inicio", "Feedback", "Recompra"]
    pagina_seleccionada = st.sidebar.selectbox("Selecciona una página:", opciones_paginas)

    # Mostrar el contenido de la página seleccionada
    if pagina_seleccionada == "Inicio":
        pagina_inicio()
    if pagina_seleccionada == "Feedback" :
        mostrar_feedback()
    elif pagina_seleccionada == "Recompra":
        mostrar_recompra()
  


# Iniciar la aplicación
if __name__ == "__main__":
    main()