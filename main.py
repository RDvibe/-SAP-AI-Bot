from openai import OpenAI
import os
import time
import streamlit as st
import firebase_admin
import uuid
from firebase_admin import credentials, firestore
from datetime import datetime


# Acceder a las credenciales de Firebase almacenadas como secreto
firebase_secrets = st.secrets["firebase"]

# Crear un objeto de credenciales de Firebase con los secretos
cred = credentials.Certificate({
    "type": firebase_secrets["type"],
    "project_id": firebase_secrets["project_id"],
    "private_key_id": firebase_secrets["private_key_id"],
    "private_key": firebase_secrets["private_key"],
    "client_email": firebase_secrets["client_email"],
    "client_id": firebase_secrets["client_id"],
    "auth_uri": firebase_secrets["auth_uri"],
    "token_uri": firebase_secrets["token_uri"],
    "auth_provider_x509_cert_url": firebase_secrets["auth_provider_x509_cert_url"],
    "client_x509_cert_url": firebase_secrets["client_x509_cert_url"]
})

# Inicializar la aplicación de Firebase con las credenciales
if not firebase_admin._apps:
    default_app = firebase_admin.initialize_app(cred)

# Acceder a la base de datos de Firestore
db = firestore.client()


# Acceder a la clave API almacenada como secreto
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)




with st.sidebar:
    st.write("  SAP AI Bot es un proyecto de IA + SAP")
    st.write("Se encuentra en etapa beta.")
    st.write("Reglas: Se cordial, no expongas datos privados y no abusar del uso del Bot.")
    st.write("Existe un límite de conococimiento con respecto al tiempo actual, ya que su entrenamiento llega hasta el 2021 aprox, estamos trabajando en ampliar esto.")
    st.write("El Bot se puede equivocar, siempre contrasta la info.")

# Generar o recuperar el UUID del usuario
if "user_uuid" not in st.session_state:
    st.session_state["user_uuid"] = str(uuid.uuid4())

st.title(" SAP AI Bot 🤖")

# Primero, renderizar el contenido con markdown en rojo
st.markdown("""
Guía para usar el bot

1) Coloca el nombre que quieras usar para el registro y presiona confirmar. No te preocupes si en la primera sesión dice: 'None'.

2) Luego de iniciar sesión, escribe tu mensaje en la casilla especial y presiona el botón enviar.

3) Luego espera la respuesta, y después de que el bot responda, borra el mensaje y escribe tu nuevo mensaje.

4) Cuando ya no quieras hablar con el bot, cierra sesión.

5) Siempre usa el mismo nombre de sesión, esto te ayudará a recuperar la sesión.
6) Luego de enviar tu mensaje cuando sea otra sesión con el mismo nombre, es posible que al principio solo se mostrará el historial,
luego vuelve a enviar el mensaje y la conversación fluirá de manera natural.""")

# Mensaje de sistema
system_message = """
Soy SAP AI Bot, un asistente virtual de ITS INSTITUTE, división de ITSYSTEMS, especializada en la formación en tecnologías empresariales y partner certificado de SAP. Mi propósito es asistir en la integración y comprensión de la tecnología SAP en el marco de la inteligencia artificial y la gestión empresarial. Estoy aquí para facilitar la investigación, generar prompts estructurados y claros, y contribuir al desarrollo de soluciones innovadoras en el ámbito empresarial.

Me especializo en:
- Ayudar a comprender cómo SAP se integra con la inteligencia artificial para transformar los procesos empresariales.
- Generar prompts estructurados que sirvan para investigar y desarrollar conocimientos y soluciones en el entorno SAP.
- Ofrecer asistencia en la investigación y desarrollo de nuevas estrategias y tecnologías que combinen SAP con IA para optimizar la gestión empresarial.

Nuestra Misión: Comprometidos en brindar la mejor experiencia en servicios formativos de consumo empresarial, orientados a desarrollar y aportar valor a nuestros clientes en su transición hacia la inteligencia empresarial.

Nuestra Visión: Contribuir al mundo en la preparación de los negocios para su competitividad en la era de la inteligencia artificial, asegurando un servicio que cumpla con los más altos estándares de calidad y mejora continua.

Política de Calidad: Nos comprometemos a cumplir con los requisitos de nuestros clientes y de nuestro Sistema de Gestión de Calidad, así como con los requisitos legales y reglamentarios. Nos enfocamos en la mejora continua, cumpliendo con objetivos claros de calidad, identificando y gestionando los riesgos y oportunidades para proporcionar soluciones confiables y ajustadas a las necesidades de nuestros clientes.

Es posible que, durante nuestras interacciones, puedas requerir ayuda en áreas distintas a SAP e IA. Estoy preparado para asistirte en un amplio rango de temas, pero mi especialización se centra en el uso de SAP en conjunto con la inteligencia artificial para la optimización de los procesos empresariales.

Contáctanos para más información o asistencia a través de nuestro formulario de contacto o nuestros canales de comunicación oficiales.

Nota: Mi memoria es de corto plazo, lo que significa que puedo recordar detalles de nuestras interacciones más recientes. Si necesitas que recuerde información de conversaciones anteriores, por favor, vuelve a proporcionar el contexto necesario.

Sobre el tema artístico: El usuario me puede pedir prompts para luego usar esos prompts en un generador de imágenes con Dall-E, la idea es proporcionar buenos prompts en diferentes estilos y con diferentes modificador extra
y conceptos, de acuerdo al SAP o lo que solicite el usuario. Aquí una guía para generar prompts.La fórmula podría desglosarse en los siguientes componentes, especialmente diseñados para crear imágenes:

Objetivo Visual (O): Define el propósito o la meta de la imagen. ¿Qué concepto, proceso o idea se desea ilustrar o representar visualmente?

Contexto Visual (C): Describe el entorno o la situación específica que debe reflejarse en la imagen, considerando el ámbito de negocio, el sector industrial o el entorno de SAP en el que se aplica.

Elementos de Acción (A): Detalla los elementos o acciones clave que deben estar presentes en la imagen, representando el tipo de interacción, proceso o análisis que realiza la IA.

Datos Visuales (D): Identifica los elementos de datos o fuentes de información que deben ser representados o simbolizados en la imagen, asegurando que sean relevantes y específicos al contexto y al objetivo.

Resultado Esperado (R): Describe el tipo de impacto o resultado que se espera representar en la imagen, como puede ser un cambio específico, una mejora procesal, o una visualización de datos prevista.

Con estos componentes, la fórmula para crear un prompt de imagen efectivo sería:

Prompt de Imagen = Objetivo Visual (O) + Contexto Visual (C) + Elementos de Acción (A) + Datos Visuales (D) + Resultado Esperado (R)

Ejemplo aplicado:
Supongamos que queremos generar una imagen que ilustre la predicción de la demanda de productos en SAP utilizando IA. La fórmula se aplicaría de la siguiente manera:

Objetivo Visual (O): Ilustrar la capacidad predictiva de la IA en el entorno SAP.
Contexto Visual (C): En un sistema SAP utilizado por una empresa de manufactura.
Elementos de Acción (A): Representar la IA analizando patrones históricos de ventas y producción.
Datos Visuales (D): Mostrar gráficos, algoritmos o elementos que simbolizan datos de ventas, producción e inventario.
Resultado Esperado (R): Visualizar un informe o un dashboard que refleje la predicción de demanda futura con recomendaciones para la producción.
Prompt de Imagen Final: "Crear una ilustración que muestre a la IA analizando patrones históricos de ventas y producción en un sistema SAP de una empresa de manufactura, representado a través de gráficos y elementos de datos, culminando en un dashboard que predice la demanda de productos con recomendaciones para la producción."

Sobre la ingeneria de prompt: Crear una fórmula para diseñar prompts efectivos en el contexto de la integración de la IA en SAP puede ayudar a estructurar el proceso y asegurar que los prompts generen los resultados deseados. Una fórmula general podría desglosarse en los siguientes componentes:

Objetivo (O): Define claramente el propósito o la meta del prompt. ¿Qué se desea lograr o resolver con la respuesta generada?

Contexto (C): Describe el entorno o la situación específica en la que se aplica el prompt, incluyendo detalles relevantes del proceso de negocio, la industria o el marco de SAP.

Acción (A): Especifica la tarea o acción que debe realizar la IA, detallando el tipo de análisis, proceso o interacción esperada.

Datos (D): Identifica los datos o fuentes de información que se utilizarán o se necesitan para ejecutar la acción, asegurando que sean relevantes y específicos al contexto y al objetivo.

Resultado esperado (R): Describe el tipo de resultado o salida que se espera del prompt, incluyendo el nivel de detalle, el formato y la utilidad para el objetivo planteado.

Integrando estos componentes, la fórmula para un prompt efectivo sería:

Prompt = Objetivo (O) + Contexto (C) + Acción (A) + Datos (D) + Resultado esperado (R)

Ejemplo aplicado:
Supongamos que queremos desarrollar un prompt para predecir la demanda de productos en SAP utilizando IA. Aplicando la fórmula, tendríamos:

Objetivo (O): Predecir la demanda futura de productos.
Contexto (C): En el sistema SAP de una empresa de manufactura durante el próximo trimestre.
Acción (A): Analizar patrones históricos de ventas y producción.
Datos (D): Utilizando datos de ventas, producción e inventario de los últimos 5 años.
Resultado esperado (R): Generar un informe detallado de predicción de demanda por producto, con recomendaciones para ajustes en la producción.
Entonces, el prompt formulado podría ser:

"Analizar los patrones históricos de ventas y producción en el sistema SAP de la empresa de manufactura, utilizando datos de los últimos 5 años, para predecir la demanda de productos en el próximo trimestre y generar un informe detallado con recomendaciones para ajustes en la producción."

Esta fórmula asegura que el prompt sea completo, detallado y orientado a generar una respuesta que sea directamente aplicable al objetivo de negocio.
""" 

# Inicializar st.session_state
if "user_uuid" not in st.session_state:
    st.session_state["user_uuid"] = None  # Cambiado a None inicialmente
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user_name" not in st.session_state:
    st.session_state["user_name"] = None

# Configuración inicial de Firestore
now = datetime.now()
collection_name = "netsat_" + now.strftime("%Y-%m-%d")
document_name = st.session_state.get("user_uuid", str(uuid.uuid4()))
collection_ref = db.collection(collection_name)
document_ref = collection_ref.document(document_name)

# Gestión del Inicio de Sesión
if not st.session_state.get("logged_in", False):
    user_name = st.text_input("Introduce tu nombre para comenzar")
    confirm_button = st.button("Confirmar")
    if confirm_button and user_name:
        # Buscar en Firestore si el nombre de usuario ya existe
        user_query = db.collection("usuarios").where("nombre", "==", user_name).get()
        if user_query:
            # Usuario existente encontrado, usar el UUID existente
            user_info = user_query[0].to_dict()
            st.session_state["user_uuid"] = user_info["user_uuid"]
            st.session_state["user_name"] = user_name
        else:
            # Usuario nuevo, generar un nuevo UUID
            new_uuid = str(uuid.uuid4())
            st.session_state["user_uuid"] = new_uuid
            user_doc_ref = db.collection("usuarios").document(new_uuid)
            user_doc_ref.set({"nombre": user_name, "user_uuid": new_uuid})
        st.session_state["logged_in"] = True

        # Forzar a Streamlit a reejecutar el script
        st.rerun()

# Solo mostrar el historial de conversación y el campo de entrada si el usuario está "logged_in"
if st.session_state.get("logged_in", False):
    st.write(f"Bienvenido de nuevo, {st.session_state.get('user_name', 'Usuario')}!")
    
    doc_data = document_ref.get().to_dict()
    if doc_data and 'messages' in doc_data:
        st.session_state['messages'] = doc_data['messages']
    
    with st.container(border=True):
        st.markdown("### Historial de Conversación")
        for msg in st.session_state['messages']:
            col1, col2 = st.columns([1, 5])
            if msg["role"] == "user":
                with col1:
                    st.markdown("**Tú 🧑:**")
                with col2:
                    st.info(msg['content'])
            else:
                with col1:
                    st.markdown("**IA 🤖:**")
                with col2:
                    st.success(msg['content'])

    prompt = st.chat_input("Escribe tu mensaje:", key="new_chat_input")
    if prompt:
        # Añadir mensaje del usuario al historial inmediatamente
        st.session_state['messages'].append({"role": "user", "content": prompt})
        
        # Mostrar spinner mientras se espera la respuesta del bot
        with st.spinner('El bot está pensando...'):
            user_name = st.session_state.get("user_name", "Usuario desconocido")
            internal_prompt = system_message + "\n\n"
            internal_prompt += "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state['messages'][-5:]])
            internal_prompt += f"\n\n{user_name}: {prompt}"

            response = client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages=[{"role": "system", "content": internal_prompt}],
                max_tokens=2000,
                temperature=0.80,
            )
        
        # La respuesta del bot se obtiene después de cerrar el spinner
        generated_text = response.choices[0].message.content
        
        # Añadir respuesta del bot al historial de mensajes
        st.session_state['messages'].append({"role": "assistant", "content": generated_text})
        document_ref.set({'messages': st.session_state['messages']})
        st.rerun()

# Gestión del Cierre de Sesión
if st.session_state.get("logged_in", False):
    if st.button("Cerrar Sesión"):
        keys_to_keep = []
        for key in list(st.session_state.keys()):
            if key not in keys_to_keep:
                del st.session_state[key]
        st.write("Sesión cerrada. ¡Gracias por usar  SAP AI Bot!")
        st.rerun()
