import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# --- CONFIGURACIÓN ---
DIRECTORIO_DB = "chroma_db"
MODELO_LLM = "llama3.1"  # Asegúrate de haber hecho 'ollama pull llama3'

# 1. Cargar la Memoria (Tu base de datos)
print("🧠 Cargando cerebro (ChromaDB)...")
embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vectorstore = Chroma(
    persist_directory=DIRECTORIO_DB, 
    embedding_function=embedding_function
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 5}) # Trae los 5 fragmentos más relevantes

# 2. Configurar el LLM (El Orador)
llm = ChatOllama(model=MODELO_LLM, temperature=0.3) # Temperature baja para que sea preciso

# 3. El Prompt (La personalidad de tu IA)
# Aquí le decimos cómo debe responder usando los documentos.
template = """
Eres un experto filósofo y sociólogo digital analizando la crisis de la Generación Z.
Tu tarea es responder a la pregunta basándote EXCLUSIVAMENTE en el contexto proporcionado.

Instrucciones:
1. Analiza los testimonios (Reddit Gen Z) para encontrar evidencia empírica de dolor, ansiedad o patrones.
2. Contrasta esa evidencia con la teoría filosófica (Han, Bauman, Sartre, etc.) presente en el contexto.
3. Cita las fuentes implícitamente (ej: "Como se observa en los testimonios de Reddit..." o "Según la teoría de la sociedad del cansancio...").
4. Si la información no está en el contexto, di "No tengo información suficiente en el corpus para responder esto".

Contexto:
{context}

Pregunta del usuario:
{question}

Respuesta estructurada y profunda:
"""

prompt = ChatPromptTemplate.from_template(template)

# 4. Crear la cadena de pensamiento (Pipeline RAG)
def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# --- BUCLE DE PREGUNTAS ---
print(f"\n✅ Sistema listo con modelo {MODELO_LLM}. ¡Pregúntale a tu Tesis!")
print("Escribe 'salir' para terminar.\n")

while True:
    pregunta = input("\n🔎 Pregunta: ")
    if pregunta.lower() in ["salir", "exit", "quit"]:
        break
    
    print("\n🤔 Pensando y consultando documentos...")
    try:
        # Aquí ocurre la magia
        respuesta = rag_chain.invoke(pregunta)
        print("\n" + "="*60)
        print("🎓 RESPUESTA GENERADA:")
        print(respuesta)
        print("="*60)
    except Exception as e:
        print(f"❌ Error: {e}")
