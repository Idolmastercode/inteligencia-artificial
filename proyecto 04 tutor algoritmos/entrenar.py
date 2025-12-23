from unsloth import FastLanguageModel
import torch
from trl import SFTTrainer
from transformers import TrainingArguments
from datasets import load_dataset

# --- CONFIGURACIÓN ---
# Como no lo tienes descargado, usamos el ID de Hugging Face directamente.
# Unsloth lo descargará solo.
MODELO_ID = "unsloth/Llama-3.2-1B-Instruct-bnb-4bit"

DATASET_FILE = "./dataset_final.jsonl"
OUTPUT_DIR = "tutor_algoritmos_v1" # Aquí se guardará tu IA

# Configuración de memoria
max_seq_length = 2048 
load_in_4bit = True 

# 1. CARGAR MODELO (DESCARGA AUTOMÁTICA SI NO EXISTE)
print(f"⏳ Cargando (o descargando) modelo base: {MODELO_ID}...")

# NOTA: Si es la primera vez, esto tardará unos minutos dependiendo de tu internet
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = MODELO_ID,
    max_seq_length = max_seq_length,
    dtype = None,
    load_in_4bit = load_in_4bit,
)

# 2. CONFIGURAR ADAPTADORES (LoRA)
model = FastLanguageModel.get_peft_model(
    model,
    r = 16,
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                      "gate_proj", "up_proj", "down_proj",],
    lora_alpha = 16,
    lora_dropout = 0, 
    bias = "none",
    use_gradient_checkpointing = "unsloth", 
    random_state = 3407,
)

# 3. CARGAR TU DATASET
print(f"📂 Cargando datos de: {DATASET_FILE}")
dataset = load_dataset("json", data_files=DATASET_FILE, split="train")

def formatting_prompts_func(examples):
    convos = examples["messages"]
    texts = [tokenizer.apply_chat_template(convo, tokenize = False, add_generation_prompt = False) for convo in convos]
    return { "text" : texts, }

dataset = dataset.map(formatting_prompts_func, batched = True,)

# 4. ENTRENAR (MODO PRODUCCIÓN CON RTX 5070)
print("💪 Iniciando Entrenamiento...")

trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = dataset,
    dataset_text_field = "text",
    max_seq_length = max_seq_length,
    dataset_num_proc = 2,
    packing = False, 
    
    args = TrainingArguments(
        per_device_train_batch_size = 2, 
        gradient_accumulation_steps = 4, 
        warmup_steps = 5,
        num_train_epochs = 1, 
        learning_rate = 2e-4,
        fp16 = not torch.cuda.is_bf16_supported(),
        bf16 = torch.cuda.is_bf16_supported(), 
        logging_steps = 10,
        optim = "adamw_8bit",
        weight_decay = 0.01,
        lr_scheduler_type = "linear",
        seed = 3407,
        output_dir = "checkpoints", 
    ),
)

trainer_stats = trainer.train()

print("🎉 ¡Entrenamiento finalizado exitosamente!")

# 5. EXPORTAR A GGUF (Para Ollama)
print(f"💾 Guardando tu modelo final en carpeta '{OUTPUT_DIR}'...")
# Usamos q8_0 porque el modelo es pequeño (1B) y queremos máxima calidad
model.save_pretrained_gguf(OUTPUT_DIR, tokenizer, quantization_method = "q8_0")

print("✅ ¡LISTO! Todo ha terminado. Revisa la carpeta:", OUTPUT_DIR)