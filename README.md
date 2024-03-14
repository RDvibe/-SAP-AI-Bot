# SAP AI Bot

## Descripción
Este proyecto implementa un chatbot de inteligencia artificial llamado "SAP AI Bot", utilizando Streamlit para la interfaz de usuario y Firebase para el almacenamiento de datos. El bot está diseñado para asistir en la integración y comprensión de la tecnología SAP en el contexto de la inteligencia artificial y la gestión empresarial.

## Características
- Interfaz de usuario amigable construida con Streamlit.
- Integración con Firebase Firestore para el almacenamiento y gestión de sesiones y mensajes.
- Generación de identificadores únicos (UUID) para las sesiones de usuario.
- Utilización de la API de OpenAI para generar respuestas del bot.
- Políticas y guías de uso integradas en la interfaz para los usuarios.

## Requisitos
Para ejecutar este proyecto, necesitarás:
- Python 3.6 o superior.
- Credenciales de Firebase (archivo JSON de configuración) para autenticar y acceder a Firestore.
- Clave API de OpenAI para interactuar con los servicios de inteligencia artificial.

## Configuración
1. Clona este repositorio en tu entorno local.
2. Instala las dependencias requeridas usando `pip install -r requirements.txt`.
3. Configura las variables de entorno o los secretos de Streamlit con tus credenciales de Firebase y la clave API de OpenAI.
4. Ejecuta el comando `streamlit run <archivo>.py` para iniciar la aplicación.

## Uso
1. Accede a la interfaz de Streamlit en tu navegador.
2. Sigue las instrucciones en la barra lateral para iniciar sesión o registrarte.
3. Interactúa con el SAP AI Bot a través del campo de entrada de chat.
4. Puedes cerrar sesión cuando hayas terminado tu conversación.

## Contribuir
Si estás interesado en contribuir a este proyecto, por favor considera:
- Enviar un pull request con nuevas características o correcciones.
- Reportar problemas o sugerir mejoras a través de la sección de issues.

## Licencia
MIT
