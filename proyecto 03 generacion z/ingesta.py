import os
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document  # <--- AQUÍ ESTABA EL ERROR
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import shutil

# --- CONFIGURACIÓN ---
# Ajusta la ruta si en Linux se llama diferente, pero debería ser igual si estás en la misma carpeta
CARPETA_PDFS = "pdfs"
ARCHIVO_CSV = "corpus_tesis_final.csv"
DIRECTORIO_DB = "chroma_db"

# Modelo de Embeddings
modelo_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def cargar_pdfs():
    docs_pdfs = []
    if not os.path.exists(CARPETA_PDFS):
        print(f"⚠️ La carpeta {CARPETA_PDFS} no existe. Crea la carpeta y mete tus PDFs.")
        return []
        
    archivos = [f for f in os.listdir(CARPETA_PDFS) if f.endswith('.pdf')]
    print(f"📚 Encontrados {len(archivos)} PDFs de teoría.")
    
    for archivo in archivos:
        path = os.path.join(CARPETA_PDFS, archivo)
        try:
            loader = PyPDFLoader(path)
            pages = loader.load_and_split()
            print(f"   -> Procesado: {archivo} ({len(pages)} fragmentos)")
            docs_pdfs.extend(pages)
        except Exception as e:
            print(f"   ❌ Error en {archivo}: {e}")
            
    return docs_pdfs

def cargar_csv_reddit():
    docs_reddit = []
    if not os.path.exists(ARCHIVO_CSV):
        print("⚠️ No encuentro el CSV de Reddit. Asegúrate de que esté en la carpeta.")
        return []
        
    print("🧠 Cargando testimonios de Reddit...")
    try:
        df = pd.read_csv(ARCHIVO_CSV)
        for _, row in df.iterrows():
            # Ajuste de robustez: buscamos 'final_rag_text' o 'text'
            texto = row.get('final_rag_text', row.get('text', '')) 
            origen = row.get('subreddit', 'unknown')
            
            if len(str(texto)) > 50:
                doc = Document(
                    page_content=str(texto),
                    metadata={"source": "reddit", "subreddit": origen, "type": "empirical"}
                )
                docs_reddit.append(doc)
                
        print(f"   -> {len(docs_reddit)} testimonios cargados.")
    except Exception as e:
        print(f"   ❌ Error leyendo CSV: {e}")
        
    return docs_reddit

def main():
    if os.path.exists(DIRECTORIO_DB):
        shutil.rmtree(DIRECTORIO_DB)
        
    print("--- 1. CARGANDO DATOS ---")
    pdfs = cargar_pdfs()
    reddit = cargar_csv_reddit()
    
    todos_los_docs = pdfs + reddit
    
    if not todos_los_docs:
        print("❌ No hay datos. Revisa tus carpetas.")
        return

    print(f"\n--- 2. GENERANDO EMBEDDINGS ---")
    print(f"Total de fragmentos a procesar: {len(todos_los_docs)}")
    print("   ...Iniciando motor vectorial (Chroma)...")

    # ChromaDB creará la base de datos localmente
    vectorstore = Chroma.from_documents(
        documents=todos_los_docs,
        embedding=modelo_embeddings,
        persist_directory=DIRECTORIO_DB
    )
    
    print("\n✅ ¡LISTO! Cerebro creado con éxito.")
    print(f"💾 Guardado en carpeta: './{DIRECTORIO_DB}'")

if __name__ == "__main__":
    main()
