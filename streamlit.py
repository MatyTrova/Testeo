# Importamos las librerias a utilizar
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


# Configuramos la página
st.set_page_config(
    page_title="Dashboard Desarrollos PEC",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
    )

def hide_password_input(input_label):
    password = st.text_input(input_label, type="password", key=input_label)
    return password

st.write("---")

colA, colB, colC = st.columns(3)
with colA :
    st.image("imgs_exp/desarrollospec2.png", use_column_width=True, width=600)
# Imagen común a todas las páginas ya que esta por fuera de las funciones
with colB : 
    businessnumber = hide_password_input("Coloque su número de negocio:")
    
with colC :
    st.write("")    

st.write("---")
if businessnumber:
    st.empty()

# Obtener contraseña ingresada por el usuario
#businessnumber = st.text_input('Password:')
businessnumber = businessnumber.strip()

# Función principal
def main():

    # Conexión a la base de datos
    db_username = st.secrets["DB_USERNAME"]
    db_password = st.secrets["DB_PASSWORD"]
    db_host = st.secrets["DB_HOST"]
    db_token = st.secrets["DB_TOKEN"]
    # Creamos la conexión
    conexion_string = f"mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_token}"
    engine = create_engine(conexion_string,pool_pre_ping=True)
    # Query de consulta para la contraseña
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
        # Conexión a la base de datos
        db_username = st.secrets["DB_USERNAME"]
        db_password = st.secrets["DB_PASSWORD"]
        db_host = st.secrets["DB_HOST"]
        db_token = st.secrets["DB_TOKEN"]
        # Creamos la conexión
        conexion_string = f"mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_token}"
        engine = create_engine(conexion_string,pool_pre_ping=True)
        # Query de Feedback
        query = f"""
            SELECT e.* , c.businessPhoneNumber, c.clientName, c.userPhoneNumber
            FROM experiencias e
            JOIN clientes c ON (e.idCliente = c.idCliente)
            WHERE e.journeyClassName = 'EcommerceFeedbackCompra' AND c.businessPhoneNumber = {businessnumber} ;
        """
        df_feedback = pd.read_sql(query, engine)
        df_feedback.drop("hora",axis=1,inplace=True)
        # Ocultamos el DF ya que lo utilizamos para ver si todo esta correcto
        #st.write("Dataframe")
        #st.dataframe(df_feedback)
        st.title("Dashboard Feedback")
        if (len(df_feedback) > 0) :
            cliente_pec = df_feedback['clientName'].unique().tolist()
            st.subheader(f"Bienvenido {cliente_pec[0]}")
        st.write("---")

        # Contamos la cantidad de reviews
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
        # Cantidad conversaciones
        cantidad_clientes = len(df_feedback["idCliente"].unique())
        # Conversaciones terminadas
        conteo_terminadas = df_feedback["idCliente"].value_counts().reset_index()
        conteo_terminadas = len(conteo_terminadas[conteo_terminadas["count"] >= 2])
        # Conversaciones incompletas
        conteo_incompletas = df_feedback["idCliente"].value_counts().reset_index()
        conteo_incompletas = len(conteo_incompletas[conteo_incompletas["count"] == 1])
        # Feedbacks positivos
        if (len(df_feedback)) > 0 :
            feedbacks_positivos = reviews["Positivo"]
            valores = list(reviews.values())
            total = sum(valores)
            feedbacks_positivos = f"{(feedbacks_positivos / total ) * 100} %"
        else:
            feedbacks_positivos = 0    
        # Comentarios recibidos
        cantidad_comentarios = df_feedback.loc[(df_feedback["journeyStep"] == "RecepcionMensajeDeMejora") | (df_feedback["journeyStep"] == "EnvioComentarioDeMejora") ,"userPhoneNumber"].reset_index()
        cantidad_comentarios = len(cantidad_comentarios)

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

        # Variable de ejemplo con estilos en línea
        tarjeta1 = f'<div class="tarjeta" style="font-size: 30px; color: #00008B;">{cantidad_clientes}</div>'
        tarjeta2 = f'<div class="tarjeta" style="font-size: 30px; color: #00008B;">{conteo_terminadas}</div>'
        tarjeta3 = f'<div class="tarjeta" style="font-size: 30px; color: #00008B;">{conteo_incompletas}</div>'
        tarjeta4 = f'<div class="tarjeta" style="font-size: 30px; color: #00008B;">{feedbacks_positivos}</div>'
        tarjeta5 = f'<div class="tarjeta" style="font-size: 30px; color: #00008B;">{cantidad_comentarios}</div>'

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
        # Gráfico de líneas
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
            plt.legend(loc='upper left', bbox_to_anchor=(1.02, 1))
            date_form = DateFormatter("%d/%m")
            ax.xaxis.set_major_formatter(date_form)
            #plt.tight_layout() 
            gráfico1 = plt.gcf()
            st.write("#### **Total de reviews**")
            st.pyplot(gráfico1)

        # Gráfico de torta
        with col7:
            if len(df_feedback) > 0 :
                # Extrae las etiquetas y los valores del diccionario
                etiquetas = list(reviews.keys())
                valores = list(reviews.values())
                total = sum(valores)
                # Colores para el gráfico
                colores = ['tab:green', 'tab:grey', 'tab:blue']
                plt.figure(figsize=(6, 4))  
                sns.set(style="whitegrid")
                # Crea el gráfico de torta
                plt.pie(valores, labels=etiquetas, colors=colores, autopct=lambda p: '{:.0f} ({:.1f}%)'.format(p * total / 100, p), startangle=90)
                plt.axis('equal')  # Hace que el gráfico sea circular
                gráfico11 = plt.gcf()
                st.write("#### **Porcentaje de reviews**")
                st.pyplot(gráfico11)
            else:
                st.write("sin datos")

        st.write("---")

        # Para ver los comentarios
        if ver_comentarios:
            st.markdown("## **Comentarios**:")
            clientes_feedback = df_feedback.loc[(df_feedback["journeyStep"] == "RecepcionMensajeDeMejora") | (df_feedback["journeyStep"] == "EnvioComentarioDeMejora") ,"userPhoneNumber"].reset_index()
            clientes_feedback = sorted(clientes_feedback["userPhoneNumber"].unique().tolist())
            clientes_feedback.insert(0, "Todos")
            seleccion_cliente = st.selectbox("Clientes", clientes_feedback)
            if (seleccion_cliente == "Todos"):
                msgbody_feedback1 = df_feedback.loc[(df_feedback["journeyStep"] == "RecepcionMensajeDeMejora") | (df_feedback["journeyStep"] == "EnvioComentarioDeMejora") ,"msgBody"].str.capitalize()
                for elemento1 in msgbody_feedback1 :
                    st.write(f"+ {elemento1}")
            else:
                msgbody_feedback = df_feedback.loc[(df_feedback["journeyStep"].isin(["RecepcionMensajeDeMejora", "EnvioComentarioDeMejora"])) & (df_feedback["userPhoneNumber"] == seleccion_cliente), "msgBody"].str.capitalize()
                for elemento in msgbody_feedback :
                    st.write(f"+ {elemento}")

    # RECOMPRA
    def mostrar_recompra():
        # Verificar si el usuario está autenticado
        if not st.session_state.get('autenticado'):
            st.error("Debe ingresar una contraseña válida en la página de inicio para acceder a esta página.")
            st.stop() 
        # Conexión a la base de datos
        db_username = st.secrets["DB_USERNAME"]
        db_password = st.secrets["DB_PASSWORD"]
        db_host = st.secrets["DB_HOST"]
        db_token = st.secrets["DB_TOKEN"]
        conexion_string = f"mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_token}"
        engine = create_engine(conexion_string,pool_pre_ping=True)
        # Query de recompra
        query = f"""
                SELECT e.*, c.businessPhoneNumber, c.clientName, c.userPhoneNumber
                FROM experiencias e
                JOIN clientes c ON (e.idCliente = c.idCliente)
                WHERE e.journeyClassName IN ('EcommerceRecompraDeProducto' ,'EcommerceRecompraParaHoy') AND c.businessPhoneNumber = {businessnumber} ;
                """
        df_recompra = pd.read_sql(query, engine)
        df_recompra.drop("hora",axis=1,inplace=True)
        # Aquí también ocultamos el DF
        #st.write("Dataframe")
        #st.dataframe(df_recompra)
        st.title("Dashboard Recompra")
        if (len(df_recompra) > 0 ):
            cliente_pec = df_recompra['clientName'].unique().tolist()
            st.subheader(f"Bienvenido {cliente_pec[0]}")
        st.write("---")

        # Tarjetas
        # Cantidad de conversaciones
        cantidad_clientes = len(df_recompra["idCliente"].unique())
        # Conversaciones terminadas
        conteo_terminadas = df_recompra["idCliente"].value_counts().reset_index()
        conteo_terminadas = len(conteo_terminadas[conteo_terminadas["count"] >= 2])
        # Conversaciones incompletas
        conteo_incompletas = df_recompra["idCliente"].value_counts().reset_index()
        conteo_incompletas = len(conteo_incompletas[conteo_incompletas["count"] == 1])
        # Intencion de recompra
        intencion_recompra = len(df_recompra.loc[(df_recompra["journeyClassName"] == "EcommerceRecompraDeProducto") & (df_recompra["journeyStep"] == "RespuestaMensajeInicial") & (df_recompra["msgBody"] == "Sí, necesito comprarlo de nuevo")]) 

        # Crear 5 tarjetas en la primera fila
        col1, col2, col3, col4 = st.columns(4)

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
    
        # Variable de ejemplo con estilos en línea
        tarjeta1 = f'<div class="tarjeta" style="font-size: 30px; color: #00008B;">{cantidad_clientes}</div>'
        tarjeta2 = f'<div class="tarjeta" style="font-size: 30px; color: #00008B;">{conteo_terminadas}</div>'
        tarjeta3 = f'<div class="tarjeta" style="font-size: 30px; color: #00008B;">{conteo_incompletas}</div>'
        tarjeta4 = f'<div class="tarjeta" style="font-size: 30px; color: #00008B;">{intencion_recompra}</div>'
        #tarjeta5 = f'<div class="tarjeta" style="font-size: 30px; color: #00008B;">{hola}</div>'

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
            st.markdown('<div class="subheader">Intención de recompra</div>', unsafe_allow_html=True)
            st.markdown(tarjeta4, unsafe_allow_html=True)
            st.markdown('</div></div>', unsafe_allow_html=True)
            ver_intenciones = st.checkbox("Mostrar clientes")
        #with col5:
        #    st.markdown(tarjeta5, unsafe_allow_html=True)
        #    st.markdown('<div class="subheader">Disposición de recibir ofertas</div>', unsafe_allow_html=True)
        #    st.markdown('</div></div>', unsafe_allow_html=True)

        st.write("---")
        # gráfico de cantidad de conversaciones por fecha
        col5, col6 = st.columns([2,1])

        # Gráfico de líneas
        with col5 :
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
            st.write("#### **Total de mensajes**")
            st.pyplot(gráfico2)

        with col6:
            st.write("gráfico de torta para ver '%' de recompra positiva y negrativa")
       
        st.write("---")

        # Ver clientes que tienen intención de compra
        if ver_intenciones:
            st.markdown("## **Clientes con intención de recompra**:")
            clientes_recompra = df_recompra.loc[(df_recompra["journeyStep"] == "RespuestaSiQuiereRecomprar") ,"userPhoneNumber"].reset_index()
            clientes_recompra = sorted(clientes_recompra["userPhoneNumber"].unique().tolist())
            clientes_recompra.insert(0, "Todos")
            seleccion_cliente = st.selectbox("Clientes", clientes_recompra)
            if (seleccion_cliente) == "Todos":
                msgbody_recompra1 = df_recompra.loc[(df_recompra["journeyStep"] == "RespuestaSiQuiereRecomprar"),["fecha","userPhoneNumber","msgBody"]]
                msgbody_recompra1['fecha'] = pd.to_datetime(msgbody_recompra1['fecha'])
                msgbody_recompra1['fecha'] = msgbody_recompra1['fecha'].dt.strftime("%d-%m-%Y")
                msgbody_recompra1.rename(columns={"userPhoneNumber" : "número","msgBody": "lapso de tiempo" },inplace=True)
                st.dataframe(msgbody_recompra1,hide_index=True)
            else:
                msgbody_recompra = df_recompra.loc[(df_recompra["journeyStep"] == "RespuestaSiQuiereRecomprar")&(df_recompra["userPhoneNumber"] == seleccion_cliente),["fecha","msgBody"]]
                msgbody_recompra['fecha'] = pd.to_datetime(msgbody_recompra['fecha'])
                msgbody_recompra['fecha'] = msgbody_recompra['fecha'].dt.strftime("%d-%m-%Y")
                msgbody_recompra.rename(columns={"msgBody": "lapso de tiempo" },inplace=True)
                st.dataframe(msgbody_recompra,hide_index=True)
        

    # SNACKYS
    def recompra_snackys():
        # Verificar si el usuario está autenticado
        if not st.session_state.get('autenticado'):
            st.error("Debe ingresar una contraseña válida en la página de inicio para acceder a esta página.")
            st.stop() 
        # Conexión a la base de datos
        db_username = st.secrets["DB_USERNAME"]
        db_password = st.secrets["DB_PASSWORD"]
        db_host = st.secrets["DB_HOST"]
        db_token = st.secrets["DB_TOKEN"]
        conexion_string = f"mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_token}"
        engine = create_engine(conexion_string,pool_pre_ping=True)
        # Query de recompra
        query = f"""
                SELECT e.*, c.businessPhoneNumber, c.clientName, c.userPhoneNumber
                FROM experiencias e
                JOIN clientes c ON (e.idCliente = c.idCliente)
                WHERE e.journeyClassName IN ('GenerarRecompraGenteInactiva' ,'PreguntaSiClientePudoComprar') AND c.businessPhoneNumber = {businessnumber} ;
                """
        df_recompra = pd.read_sql(query, engine)
        df_recompra.drop("hora",axis=1,inplace=True)
        # Aquí también ocultamos el DF
        st.write("Dataframe")
        st.dataframe(df_recompra)
        st.title("Dashboard Recompra")
        if (len(df_recompra) > 0 ):
            cliente_pec = df_recompra['clientName'].unique().tolist()
            st.subheader(f"Bienvenido {cliente_pec[0]}")
        st.write("---")

        # Tarjetas
        # Cantidad de conversaciones
        cantidad_conversaciones = len(df_recompra["idCliente"].unique())
        # Conversaciones terminadas
        conteo_terminadas = df_recompra["idCliente"].value_counts().reset_index()
        conteo_terminadas = len(conteo_terminadas[conteo_terminadas["count"] >= 2])
        # Conversaciones incompletas
        conteo_incompletas = df_recompra["idCliente"].value_counts().reset_index()
        conteo_incompletas = len(conteo_incompletas[conteo_incompletas["count"] == 1])
        # Intencion de recompra
        intencion_recompra = len(df_recompra.loc[(df_recompra["journeyClassName"] == "EcommerceRecompraDeProducto") & (df_recompra["journeyStep"] == "RespuestaMensajeInicial") & (df_recompra["msgBody"] == "Sí, necesito comprarlo de nuevo")]) 
        # Recompra exitosa
        recompra_exitosa = 0

        # Crear 5 tarjetas en la primera fila
        col1, col2, col3, col4 = st.columns(4)

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
    
        # Variable de ejemplo con estilos en línea
        tarjeta1 = f'<div class="tarjeta" style="font-size: 30px; color: #00008B;">{00}</div>'
        tarjeta2 = f'<div class="tarjeta" style="font-size: 30px; color: #00008B;">{00}</div>'
        tarjeta3 = f'<div class="tarjeta" style="font-size: 30px; color: #00008B;">{00}</div>'
        tarjeta4 = f'<div class="tarjeta" style="font-size: 30px; color: #00008B;">{00}</div>'
        tarjeta5 = f'<div class="tarjeta" style="font-size: 30px; color: #00008B;">{00}</div>'

        # Contenido de las tarjetas
        with col1:
            st.markdown('<div class="subheader">Cantidad de conversaciones</div>', unsafe_allow_html=True)
            st.markdown(tarjeta1, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.write(f"Conversaciones terminadas:{00}")
            st.write(f"Conversaciones incompletas:{00}")

        with col2:
            st.markdown('<div class="subheader">Recompra exitosa</div>', unsafe_allow_html=True)
            st.markdown(tarjeta2, unsafe_allow_html=True)
            st.markdown('</div></div>', unsafe_allow_html=True)

        with col3:
            st.markdown('<div class="subheader">Intención de recompra</div>', unsafe_allow_html=True)
            st.markdown(tarjeta3, unsafe_allow_html=True)
            st.markdown('</div></div>', unsafe_allow_html=True)
            ver_intenciones = st.checkbox("Ver clientes")
        with col4:
            st.markdown('<div class="subheader">Tia Snackys</div>', unsafe_allow_html=True)
            st.markdown(tarjeta4, unsafe_allow_html=True)
            st.markdown('</div></div>', unsafe_allow_html=True)
            ver_clientes = st.checkbox("Mostrar clientes")

        st.write("---")

    
        col5, col6 = st.columns([2,1])

        with col5 :
            # gráfico de cantidad de mensajes por fecha
            st.write("gráfico de líneas")

        with col6:
            # gráfico de barras horizontales de categorias 
            st.write("categorias de productos mas seleccionados")
            
        st.write("---")

        col7, col8 = st.columns(2)

        with col7 :
            st.write("gráfico de torta con '%' de recompra + y -")

        with col8 :
            st.write("Acá mostramos los clientes del tia snackys y de las intenciones de recompra")

    # SNACKYS
    def oferta_snackys():
        # Verificar si el usuario está autenticado
        if not st.session_state.get('autenticado'):
            st.error("Debe ingresar una contraseña válida en la página de inicio para acceder a esta página.")
            st.stop() 
        # Conexión a la base de datos
        db_username = st.secrets["DB_USERNAME"]
        db_password = st.secrets["DB_PASSWORD"]
        db_host = st.secrets["DB_HOST"]
        db_token = st.secrets["DB_TOKEN"]
        conexion_string = f"mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_token}"
        engine = create_engine(conexion_string,pool_pre_ping=True)
        # Query de recompra
        query = f"""
                SELECT e.* , c.businessPhoneNumber, c.clientName, c.userPhoneNumber
                FROM experiencias e
                JOIN clientes c ON (e.idCliente = c.idCliente)
                WHERE e.journeyClassName = 'SnackyOfertas' AND c.businessPhoneNumber = {businessnumber} ;
                """
        df_oferta_snackys = pd.read_sql(query, engine)
        df_oferta_snackys.drop("hora",axis=1,inplace=True)
        # Aquí también ocultamos el DF
        st.write("Dataframe")
        st.dataframe(df_oferta_snackys)
        st.title("Dashboard ofertas")
        if (len(df_oferta_snackys) > 0 ):
            cliente_pec = df_oferta_snackys['clientName'].unique().tolist()
            st.subheader(f"Bienvenido {cliente_pec[0]}")
        st.write("---")

        # Tarjetas
        # Cantidad de conversaciones
        cantidad_conversaciones = len(df_oferta_snackys["idCliente"].unique())
        # Conversaciones terminadas
        conteo_terminadas = df_oferta_snackys["idCliente"].value_counts().reset_index()
        conteo_terminadas = len(conteo_terminadas[conteo_terminadas["count"] >= 2])
        # Conversaciones incompletas
        conteo_incompletas = df_oferta_snackys["idCliente"].value_counts().reset_index()
        conteo_incompletas = len(conteo_incompletas[conteo_incompletas["count"] == 1])
        # motivos_clientes_no_interesados
        motivos_clientes_no_interesados = len( df_oferta_snackys.loc[(df_oferta_snackys["journeyStep"] == "RespuestaMotivoClienteParaNoSuscripcion") ,"userPhoneNumber"].reset_index()) 


        # Crear 5 tarjetas en la primera fila
        col1, col2, col3= st.columns(3)

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
    
        # Variable de ejemplo con estilos en línea
        tarjeta1 = f'<div class="tarjeta" style="font-size: 30px; color: #00008B;">{cantidad_conversaciones}</div>'
        tarjeta2 = f'<div class="tarjeta" style="font-size: 30px; color: #00008B;">{00}</div>'
        tarjeta3 = f'<div class="tarjeta" style="font-size: 30px; color: #00008B;">{motivos_clientes_no_interesados}</div>'

        # Contenido de las tarjetas
        with col1:
            st.markdown('<div class="subheader">Cantidad de conversaciones</div>', unsafe_allow_html=True)
            st.markdown(tarjeta1, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            col11, col22 = st.columns(2)
            with col11 :
                st.write(f"Conversaciones terminadas:{00}")
            with col22 :
                st.write(f"Conversaciones incompletas:{00}")

        with col2:
            st.markdown('<div class="subheader">Clientes que se dieron de baja (Dejar de recibir)</div>', unsafe_allow_html=True)
            st.markdown(tarjeta2, unsafe_allow_html=True)
            st.markdown('</div></div>', unsafe_allow_html=True)

        with col3:
            st.markdown('<div class="subheader">Motivos de clientes al no estar interesados</div>', unsafe_allow_html=True)
            st.markdown(tarjeta3, unsafe_allow_html=True)
            st.markdown('</div></div>', unsafe_allow_html=True)
            ver_motivos = st.checkbox("Mostrar comentarios")
            
        st.write("---")

    
        col4, col5 = st.columns([2,1])

        with col4 :
            # gráfico de cantidad de mensajes por fecha
            st.write("gráfico de líneas")
            df_oferta_snackys['fecha'] = pd.to_datetime(df_oferta_snackys['fecha'])
            registros_por_dia = df_oferta_snackys['fecha'].value_counts().reset_index()
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
            st.write("#### **Total de mensajes**")
            st.pyplot(gráfico2)

        with col5:
            # gráfico de torta
            st.write("gráfico de torta con '%' negativo y positivo")
            torta = df_oferta_snackys[(df_oferta_snackys["journeyStep"] == "RespuestaMensajeInicial")]
            # Contamos la cantidad de suscriptos
            subs = {"Suscriptos":     torta[torta["msgBody"].str.contains("\+")].shape[0] ,
                    "No suscriptos":    torta[torta["msgBody"].str.contains("\-")].shape[0]
                    }
            if len(df_oferta_snackys) > 0 :
                # Extrae las etiquetas y los valores del diccionario
                etiquetas = list(subs.keys())
                valores = list(subs.values())
                total = sum(valores)
                # Colores para el gráfico
                colores = ['tab:green', 'tab:blue']
                plt.figure(figsize=(6, 4))  
                sns.set(style="whitegrid")
                # Crea el gráfico de torta
                plt.pie(valores, labels=etiquetas, colors=colores, autopct=lambda p: '{:.0f} ({:.1f}%)'.format(p * total / 100, p), startangle=90)
                plt.axis('equal')  # Hace que el gráfico sea circular
                gráfico11 = plt.gcf()
                st.write("#### **Porcentaje de reviews**")
                st.pyplot(gráfico11)
            else:
                st.write("sin datos")


        st.write("---")

        st.write("acá mnostrar los motivos de los clientes")   
        if ver_motivos:
            st.markdown("## **Comentarios**:")
            motivos_clientes = df_oferta_snackys.loc[(df_oferta_snackys["journeyStep"] == "RespuestaMotivoClienteParaNoSuscripcion") ,"userPhoneNumber"].reset_index()
            motivos_clientes = sorted(motivos_clientes["userPhoneNumber"].unique().tolist())
            motivos_clientes.insert(0, "Todos")
            seleccion_cliente = st.selectbox("Clientes", motivos_clientes)
            if (seleccion_cliente == "Todos"):
                msgbody_feedback1 = df_oferta_snackys.loc[(df_oferta_snackys["journeyStep"] == "RespuestaMotivoClienteParaNoSuscripcion") ,"msgBody"].str.capitalize()
                for elemento1 in msgbody_feedback1 :
                    st.write(f"+ {elemento1}")
            else:
                msgbody_feedback = df_oferta_snackys.loc[(df_oferta_snackys["journeyStep"] == "RespuestaMotivoClienteParaNoSuscripcion") & (df_oferta_snackys["userPhoneNumber"] == seleccion_cliente), "msgBody"].str.capitalize()
                for elemento in msgbody_feedback :
                    st.write(f"+ {elemento}")
        st.write("---")


    # Opciones del sidebar para seleccionar página
    #opciones_paginas = ["Inicio", "Feedback", "Recompra"]
    #pagina_seleccionada = st.sidebar.selectbox("Selecciona una página:", opciones_paginas)
    
    # Mostrar el contenido de la página seleccionada
    #if pagina_seleccionada == "Inicio":
    #    pagina_inicio()
    #if pagina_seleccionada == "Feedback" :
    #    mostrar_feedback()
    #elif pagina_seleccionada == "Recompra":
    #    mostrar_recompra()
  
    # Snackys
    opciones_paginas_snackys = ["Inicio","Ofertas", "Recompra"]
    pagina_seleccionada = st.sidebar.selectbox("Selecciona una página:", opciones_paginas_snackys)

    # Mostrar páginas para Snackys
    if pagina_seleccionada == "Inicio":
        pagina_inicio()
    if pagina_seleccionada == "Recompra":
        recompra_snackys()
    if pagina_seleccionada == "Ofertas" :
        oferta_snackys()
  

# Iniciar la aplicación
if __name__ == "__main__":
    main()