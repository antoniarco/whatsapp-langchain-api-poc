from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
from langchain.schema.runnable import RunnableMap, RunnableLambda
from dotenv import load_dotenv
import os
import logging
import numpy as np

# Configurar FastAPI
app = FastAPI()

# Configurar logs
logging.basicConfig(level=logging.INFO)

# Cargar variables de entorno
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configura tu clave de OpenAI
if not OPENAI_API_KEY:
    raise ValueError("La variable de entorno OPENAI_API_KEY no está configurada. Por favor, asegúrate de configurarla en un archivo .env o directamente en el entorno.")

# Clase para el cuerpo de la solicitud
class Message(BaseModel):
    role: str  # Ejemplo: "user" o "assistant"
    message: str  # Contenido del mensaje

class WhatsAppRequest(BaseModel):
    sender: str
    agent: str  # Nombre del agente a utilizar
    parameters: dict = {}  # Parámetros opcionales: temperatura, top_p, etc.
    conversation_history: list[Message]

# Cargar documentos de ejemplo al vector store
documents = [
    Document(page_content="Devoluciones son en 7 días.", metadata={"id": 1}),
    Document(page_content="Los pedidos se envían en 24 horas.", metadata={"id": 2}),
    Document(page_content="El horario de atención al cliente es de 9 a 18 horas.", metadata={"id": 3}),
]

# Configurar embeddings y FAISS
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
vector_store = FAISS.from_documents(documents, embeddings)

# Configurar agentes dinámicos
def create_agent(temperature=0.7):
    return ChatOpenAI(model="gpt-3.5-turbo", temperature=temperature, openai_api_key=OPENAI_API_KEY)

agents = {
    "default": create_agent(temperature=0.7),
    "creative": create_agent(temperature=0.9),
    "analytical": create_agent(temperature=0.2)
}

# Crear prompt templates
intention_prompt = PromptTemplate(
    input_variables=["message"],
    template="Clasifica la intención del siguiente mensaje: {message}"
)

response_prompt = PromptTemplate(
    input_variables=["intention", "context", "message", "additional_conditions"],
    template="Usuario tiene intención '{intention}'. Contexto relevante: {context}. Mensaje del usuario: {message}. Condiciones adicionales: {additional_conditions}. Responde profesionalmente."
)

# Función auxiliar para extraer contexto y calcular confianza
def extract_context_and_confidence(user_message):
    context_results = vector_store.similarity_search_with_score(user_message, k=1)
    if not context_results:
        return "No hay contexto disponible.", 0
    # Obtener el contexto y la puntuación de similitud
    context, similarity_score = context_results[0]
    # Convertir la puntuación a un valor de confianza (de 0 a 100)
    confidence = min(max(similarity_score * 100, 0), 100)  # Normalizar a rango [0, 100]
    return context.page_content, confidence

# Endpoint principal
@app.post("/webhook/whatsapp")
async def handle_whatsapp_message(req: WhatsAppRequest):
    try:
        logging.info(f"Recibiendo mensaje de {req.sender}")

        # Validar el agente solicitado
        if req.agent not in agents:
            raise HTTPException(status_code=400, detail=f"Agente '{req.agent}' no está configurado.")

        # Seleccionar el agente
        temperature = req.parameters.get("temperature", 0.7)
        agent = create_agent(temperature=temperature)

        # Obtener el último mensaje del usuario
        user_message = req.conversation_history[-1].message
        logging.info(f"Último mensaje del usuario: {user_message}")

        # Obtener contexto relevante y calcular confianza
        context, confidence = extract_context_and_confidence(user_message)
        logging.info(f"Contexto recuperado: {context}, Confianza: {confidence}")

        # Procesar intención
        intention_result = agent.invoke(intention_prompt.format_prompt(message=user_message))
        if hasattr(intention_result, "content"):
            intention = intention_result.content.strip()
        else:
            intention = intention_result.strip()

        # Generar respuesta
        response_result = agent.invoke(
            response_prompt.format_prompt(
                intention=intention,
                context=context,
                message=user_message,
                additional_conditions=req.parameters.get("additional_conditions", "")
            )
        )
        if hasattr(response_result, "content"):
            response_content = response_result.content.strip()
        else:
            response_content = response_result.strip()

        # Construir la respuesta final
        response = {
            "status": "success",
            "confidence": round(confidence, 2),
            "content": response_content
        }

        return response

    except Exception as e:
        logging.error(f"Error procesando el mensaje: {str(e)}")
        return {
            "status": "error",
            "confidence": 0,
            "content": f"Error procesando el mensaje: {str(e)}"
        }

# Endpoint básico para probar
@app.get("/")
async def root():
    return {"message": "WhatsApp OpenAI LangChain Responder está activo."}



