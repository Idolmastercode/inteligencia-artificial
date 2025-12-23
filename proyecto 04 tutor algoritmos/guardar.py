from unsloth import FastLanguageModel
import os

# Tu checkpoint
ADAPTADORES = "checkpoints/checkpoint-295" 
CARPETA_RAW = "tutor_lora_raw"

print("🔥 Cargando checkpoint...")
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = ADAPTADORES,
    max_seq_length = 2048,
    dtype = None,
    load_in_4bit = True, 
)

print(f"⚡ Guardando archivos crudos en '{CARPETA_RAW}'...")
# Guardamos solo el adaptador en formato HuggingFace estándar
model.save_pretrained(CARPETA_RAW)
tokenizer.save_pretrained(CARPETA_RAW)

print("✅ ¡Listo! Paso 1 completado.")
