# WhatsApp LangChain API POC

Este proyecto es una **Prueba de Concepto (POC)** que implementa una API basada en **FastAPI** que utiliza **LangChain**, **OpenAI GPT-3.5**, y **FAISS** para construir una solución que responde a consultas de clientes de forma dinámica y contextualizada, simulando un sistema de atención automatizada.

---

## **Arquitectura**

### **Diagrama básico de la arquitectura**
Cliente WhatsApp → 
FastAPI API | LangChain (Contexto + LLM) | Vector Store (FAISS) 
↔ Base de Conocimientos


### **Componentes principales**

1. **Cliente WhatsApp**:
   - Representa el usuario final enviando preguntas o solicitudes al sistema.

2. **FastAPI**:
   - Expone un endpoint `/webhook/whatsapp` para recibir solicitudes HTTP POST.
   - Gestiona la lógica de validación, orquestación, y manejo de errores.

3. **LangChain**:
   - **LangChain** actúa como el núcleo de procesamiento:
     - **Recuperación de contexto**: Busca en la base de conocimientos información relevante utilizando FAISS.
     - **Clasificación de intención**: Identifica qué quiere el usuario.
     - **Generación de respuesta**: Utiliza un modelo de lenguaje (LLM) para generar una respuesta personalizada.

4. **Vector Store (FAISS)**:
   - **Almacén de documentos**: Contiene una base de conocimientos (por ejemplo, políticas de devolución, horarios, preguntas frecuentes).
   - **Búsqueda basada en embeddings**: Utiliza `OpenAIEmbeddings` para convertir mensajes y documentos en vectores, lo que permite encontrar información relevante mediante similitud.

5. **OpenAI GPT-3.5**:
   - Clasifica intenciones y genera respuestas basadas en el contexto recuperado y los prompts predefinidos.

---

## **Flujo del sistema**

1. **Entrada del Usuario**:
   - El usuario envía un mensaje desde WhatsApp.
   - Ejemplo: "¿Cuál es el horario de atención al cliente?"

2. **Procesamiento en la API**:
   - El mensaje es recibido por FastAPI y procesado de la siguiente manera:
     - Se selecciona un **agente** (por ejemplo, `default`, `creative`, o `analytical`) basado en el parámetro `agent`.
     - Se procesan parámetros adicionales como `temperature` y `additional_conditions`.

3. **Recuperación del Contexto (LangChain + FAISS)**:
   - El mensaje del usuario es convertido a un vector de embedding.
   - FAISS busca el documento más relevante en la base de conocimientos.
   - Se calcula una **confianza** (de 0 a 100) basada en la similitud entre el mensaje y el documento encontrado.

4. **Clasificación de Intención (LangChain + LLM)**:
   - Un **PromptTemplate** le pide al modelo clasificar la intención del usuario.
   - Ejemplo de intención: `"Consultar horario de atención al cliente"`.

5. **Generación de Respuesta (LangChain + LLM)**:
   - Un segundo prompt combina:
     - La intención detectada.
     - El contexto recuperado.
     - Condiciones adicionales (por ejemplo, "sé amable").
   - El modelo genera una respuesta personalizada para el usuario.

6. **Salida del Sistema**:
   - Se devuelve un JSON con:
     - `status`: Éxito o error.
     - `confidence`: Confianza basada en la similitud del contexto.
     - `content`: Respuesta generada por el modelo.

---

## **Uso de LangChain**

LangChain se utiliza en tres capas principales:

1. **Recuperación de Contexto**:
   - **Vector Store**: FAISS almacena los documentos en forma de embeddings.
   - **Búsqueda por similitud**: Se utiliza `similarity_search_with_score` para recuperar el documento más relevante.

2. **Clasificación de Intención**:
   - **PromptTemplate**: El mensaje del usuario se envía al LLM con un prompt que solicita clasificar la intención.

3. **Generación de Respuesta**:
   - **PromptTemplate**: Combina intención, contexto y parámetros adicionales para generar una respuesta personalizada.

---

## **Ventajas de la Arquitectura**

1. **Escalabilidad**:
   - Soporta múltiples agentes (`default`, `creative`, `analytical`).
   - Se pueden añadir nuevos agentes o modelos con diferentes configuraciones de `temperature` y `top_p`.

2. **Modularidad**:
   - Los componentes (FastAPI, LangChain, FAISS, OpenAI) están desacoplados, lo que facilita su mantenimiento y expansión.

3. **Personalización**:
   - Los prompts son altamente configurables y permiten ajustar el estilo y tono de las respuestas.

4. **Recuperación Dinámica de Contexto**:
   - Utiliza embeddings para buscar información relevante en tiempo real, lo que garantiza respuestas basadas en el conocimiento más actualizado.

5. **Fiabilidad**:
   - La confianza en la respuesta se calcula a partir de la similitud de embeddings, ofreciendo un indicador objetivo de calidad.

---

## **Cómo usar este proyecto**

### **1. Configuración Inicial**

1. Clona el repositorio:
   ```bash
   git clone https://github.com/antoniarco/whatsapp-langchain-api-poc.git
   cd whatsapp-langchain-api-poc

2. Instala las dependencias:
pip install -r requirements.txt

3. Configura tu archivo .env con tu clave de OpenAI:
   OPENAI_API_KEY=tu-clave-de-openai


Claro, aquí tienes el contenido formateado como un archivo README.md. Solo copia y pega esto en tu archivo:

markdown
Copiar
# WhatsApp LangChain API POC

Este proyecto es una **Prueba de Concepto (POC)** que implementa una API basada en **FastAPI** que utiliza **LangChain**, **OpenAI GPT-3.5**, y **FAISS** para construir una solución que responde a consultas de clientes de forma dinámica y contextualizada, simulando un sistema de atención automatizada.

---

## **Arquitectura**

### **Diagrama básico de la arquitectura**
Cliente WhatsApp → FastAPI API | LangChain (Contexto + LLM) | Vector Store (FAISS) ↔ Base de Conocimientos

markdown
Copiar

### **Componentes principales**

1. **Cliente WhatsApp**:
   - Representa el usuario final enviando preguntas o solicitudes al sistema.

2. **FastAPI**:
   - Expone un endpoint `/webhook/whatsapp` para recibir solicitudes HTTP POST.
   - Gestiona la lógica de validación, orquestación, y manejo de errores.

3. **LangChain**:
   - **LangChain** actúa como el núcleo de procesamiento:
     - **Recuperación de contexto**: Busca en la base de conocimientos información relevante utilizando FAISS.
     - **Clasificación de intención**: Identifica qué quiere el usuario.
     - **Generación de respuesta**: Utiliza un modelo de lenguaje (LLM) para generar una respuesta personalizada.

4. **Vector Store (FAISS)**:
   - **Almacén de documentos**: Contiene una base de conocimientos (por ejemplo, políticas de devolución, horarios, preguntas frecuentes).
   - **Búsqueda basada en embeddings**: Utiliza `OpenAIEmbeddings` para convertir mensajes y documentos en vectores, lo que permite encontrar información relevante mediante similitud.

5. **OpenAI GPT-3.5**:
   - Clasifica intenciones y genera respuestas basadas en el contexto recuperado y los prompts predefinidos.

---

## **Flujo del sistema**

1. **Entrada del Usuario**:
   - El usuario envía un mensaje desde WhatsApp.
   - Ejemplo: "¿Cuál es el horario de atención al cliente?"

2. **Procesamiento en la API**:
   - El mensaje es recibido por FastAPI y procesado de la siguiente manera:
     - Se selecciona un **agente** (por ejemplo, `default`, `creative`, o `analytical`) basado en el parámetro `agent`.
     - Se procesan parámetros adicionales como `temperature` y `additional_conditions`.

3. **Recuperación del Contexto (LangChain + FAISS)**:
   - El mensaje del usuario es convertido a un vector de embedding.
   - FAISS busca el documento más relevante en la base de conocimientos.
   - Se calcula una **confianza** (de 0 a 100) basada en la similitud entre el mensaje y el documento encontrado.

4. **Clasificación de Intención (LangChain + LLM)**:
   - Un **PromptTemplate** le pide al modelo clasificar la intención del usuario.
   - Ejemplo de intención: `"Consultar horario de atención al cliente"`.

5. **Generación de Respuesta (LangChain + LLM)**:
   - Un segundo prompt combina:
     - La intención detectada.
     - El contexto recuperado.
     - Condiciones adicionales (por ejemplo, "sé amable").
   - El modelo genera una respuesta personalizada para el usuario.

6. **Salida del Sistema**:
   - Se devuelve un JSON con:
     - `status`: Éxito o error.
     - `confidence`: Confianza basada en la similitud del contexto.
     - `content`: Respuesta generada por el modelo.

---

## **Uso de LangChain**

LangChain se utiliza en tres capas principales:

1. **Recuperación de Contexto**:
   - **Vector Store**: FAISS almacena los documentos en forma de embeddings.
   - **Búsqueda por similitud**: Se utiliza `similarity_search_with_score` para recuperar el documento más relevante.

2. **Clasificación de Intención**:
   - **PromptTemplate**: El mensaje del usuario se envía al LLM con un prompt que solicita clasificar la intención.

3. **Generación de Respuesta**:
   - **PromptTemplate**: Combina intención, contexto y parámetros adicionales para generar una respuesta personalizada.

---

## **Ventajas de la Arquitectura**

1. **Escalabilidad**:
   - Soporta múltiples agentes (`default`, `creative`, `analytical`).
   - Se pueden añadir nuevos agentes o modelos con diferentes configuraciones de `temperature` y `top_p`.

2. **Modularidad**:
   - Los componentes (FastAPI, LangChain, FAISS, OpenAI) están desacoplados, lo que facilita su mantenimiento y expansión.

3. **Personalización**:
   - Los prompts son altamente configurables y permiten ajustar el estilo y tono de las respuestas.

4. **Recuperación Dinámica de Contexto**:
   - Utiliza embeddings para buscar información relevante en tiempo real, lo que garantiza respuestas basadas en el conocimiento más actualizado.

5. **Fiabilidad**:
   - La confianza en la respuesta se calcula a partir de la similitud de embeddings, ofreciendo un indicador objetivo de calidad.

---

## **Cómo usar este proyecto**

### **1. Configuración Inicial**

1. Clona el repositorio:
   ```bash
   git clone https://github.com/antoniarco/whatsapp-langchain-api-poc.git
   cd whatsapp-langchain-api-poc
Instala las dependencias:

bash
Copiar
pip install -r requirements.txt
Configura tu archivo .env con tu clave de OpenAI:

plaintext
Copiar
OPENAI_API_KEY=tu-clave-de-openai


##2. Ejecución del Proyecto
1. Ejecuta el servidor FastAPI:
uvicorn main:app --reload

2. Prueba el endpoint /webhook/whatsapp con un cliente como Postman o curl:
curl -X POST http://127.0.0.1:8000/webhook/whatsapp \
-H "Content-Type: application/json" \
-d '{
  "sender": "123456789",
  "agent": "default",
  "parameters": {
    "temperature": 0.7,
    "additional_conditions": "Sé amable y claro"
  },
  "conversation_history": [
    {
      "role": "user",
      "message": "¿Cuál es el horario de atención al cliente?"
    }
  ]
}'

3. Respuesta esperada
El sistema devuelve un JSON como:
{
  "status": "success",
  "confidence": 89.34,
  "content": "El horario de atención al cliente es de 9 a 18 horas. ¡No dudes en contactarnos durante ese tiempo!"
}

