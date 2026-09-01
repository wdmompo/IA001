from functools import wraps
import logging
from os import path
import pandas as pd
import re
from sentence_transformers import SentenceTransformer
import time
import torch
import truststore


DEBUG = False
MODELO = 'paraphrase-multilingual-MiniLM-L12-v2'  # Modelo preentrenado para obtener embeddings de oraciones
         # Otros modelos: 'all-MiniLM-L6-v2'


logging.basicConfig(
    filename="IA001.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
    level=logging.INFO,
)


def medir_tiempo_ms(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        duracion_ms = (time.perf_counter() - inicio) * 1000
        logging.info(f"Proccess Time: ({func.__name__}) {duracion_ms:.2f} ms")
        if DEBUG:
            print(f"Proccess Time: ({func.__name__}) {duracion_ms:.2f} ms")
        return resultado
    return wrapper


# @medir_tiempo_ms
def limpiar_texto(texto) -> str:
    if pd.isna(texto):
        return ""
    texto = str(texto)
    texto = texto.lower()
    texto = re.sub(r'<.*?>', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto)
    texto = texto.strip()
    texto = re.sub('[áÁ]', 'a', texto)
    texto = re.sub('[éÉ]', 'e', texto)
    texto = re.sub('[íÍ]', 'i', texto)
    texto = re.sub('[óÓ]', 'o', texto)
    texto = re.sub('[úÚ]', 'u', texto)
    texto = re.sub('[ñÑ]', 'n', texto)
    texto = re.sub('[^a-zA-Z]', ' ', texto)
    return texto


@medir_tiempo_ms
def cargar_datos_desde_txt(nombre_archivo):
    try:
        with open(path.join(path.dirname(__file__), nombre_archivo), 'r', encoding='utf-8') as f:
                return [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"File not found: {nombre_archivo}")
        return []


@medir_tiempo_ms
def model_encode(model, sentences, device):
    return model.encode(
        inputs=sentences,
        device=device,
        show_progress_bar=True,
        convert_to_tensor=True,
        normalize_embeddings=True,
    )


@medir_tiempo_ms
def get_model_device() -> str:
    # Detectar automáticamente el mejor dispositivo disponible
    # device = "cuda" if torch.cuda.is_available() else "cpu"
    # 1. Verificar si hay GPU de NVIDIA (CUDA)
    if torch.cuda.is_available():
        device = "cuda"
    # 2. Verificar si hay GPU de Apple Silicon (M1/M2/M3)
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        device = "mps"
    # 3. Verificar si hay GPU de Intel (XPU) - Común en arquitecturas modernas
    elif hasattr(torch, "xpu") and torch.xpu.is_available():
        device = "xpu"
    # 4. Si ninguna opción está disponible, usar el procesador principal
    else:
        device = "cpu"
    return device


@medir_tiempo_ms
def main():
    # Carga de expresiones a descartar
    print("\nLoading expressions to discard...")
    logging.info(f"Loading expressions to discard...")
    expresiones_a_descartar = cargar_datos_desde_txt('expresiones_a_descartar.txt')
    expresiones_a_descartar.append("")
    logging.info(f"Loaded {len(expresiones_a_descartar)} expressions to discard.")
    print(f"Loaded {len(expresiones_a_descartar)} expressions to discard.")
    if DEBUG:
        print(f"Expressions to discard:")
        for i, expresion in enumerate(expresiones_a_descartar):
            print(f"Expression {i+1}: {expresion}")


    # Carga de frases de referencia
    print("\nLoading reference sentences...")
    logging.info(f"Loading reference sentences...")
    frases_de_referencia = cargar_datos_desde_txt('frases_de_referencia.txt')
    logging.info(f"Loaded {len(frases_de_referencia)} reference sentences.")
    print(f"Loaded {len(frases_de_referencia)} reference sentences.")
    if DEBUG:
        print(f"Reference sentences:")
        for i, sentence in enumerate(frases_de_referencia):
            print(f"Sentence {i+1}: {sentence}")


    # Carga de opiniones
    print("\nLoading opinions...")
    logging.info(f"Loading opinions...")
    opiniones = cargar_datos_desde_txt('opiniones.txt')
    logging.info(f"Loaded {len(opiniones)} opinions.")
    print(f"Loaded {len(opiniones)} opinions.")
    if DEBUG:
        print(f"Opinions:")
        for i, opinion in enumerate(opiniones):
            print(f"Opinion {i+1}: {opinion}")


    # Limpiar opiniones
    print("\nCleaning opinions...")
    logging.info(f"Cleaning opinions...")
    opiniones = [opinion for opinion in opiniones if opinion.strip()]
    print(f"Opinions after removing empty lines: {len(opiniones)}")
    opiniones = [limpiar_texto(opinion) for opinion in opiniones if limpiar_texto(opinion)]
    logging.info(f"Cleaned opinions: {len(opiniones)}")
    print(f"Cleaned opinions: {len(opiniones)}")


    # Cargar un modelo preentrenado
    print(f"\nLoading model {MODELO}...")
    logging.info(f"Loading model {MODELO}...")
    truststore.inject_into_ssl()
    logging.info(f"Truststore set.")
    # Detectar automáticamente el mejor dispositivo disponible
    device = get_model_device()
    try:
        model = SentenceTransformer(
            model_name_or_path=MODELO, 
            device=device  # "cuda", "cpu", "mps", "npu"
        )
    except Exception as e:
        logging.info(f"Error loading model {e}.")
        print(f"Error loading model {e}.")
    else:
        logging.info(f"Model loaded successfully in {model.device}.")
        print(f"Model loaded successfully in {model.device}.")


    # Codificar oraciones para obtener sus embeddings
    print(f"\nEncoding sentences (frases de referencia)...")
    embeddings_frases_de_referencia = model_encode(model, frases_de_referencia, device)
    print(f"Sentences encoded in {model.device}.")
    if DEBUG:
        print("Embeddings:")
        for i, embedding in enumerate(embeddings_frases_de_referencia):
            print(f"Sentence {i+1} embedding: {embedding[:5]}...")  # Mostrar solo los primeros 5 valores del embedding


    # Codificar oraciones para obtener sus embeddings
    print("\nEncoding sentences (opiniones)...")
    embeddings_opiniones = model_encode(model, opiniones, device)
    print(f"Sentences encoded in {model.device}.")
    if DEBUG:
        print("Embeddings:")
        for i, embedding in enumerate(embeddings_opiniones):
            print(f"Sentence {i+1} embedding: {embedding[:5]}...")  # Mostrar solo los primeros 5 valores del embedding


    # Calcular la similitud entre los vectores
    print("\nCalculating similarities...")
    # 4. Verificar qué métrica matemática utiliza el modelo por defecto
    print(f"Métrica de comparación interna del modelo: '{model.similarity_fn_name}'")
    similarities = model.similarity(embeddings_frases_de_referencia, embeddings_opiniones)
    print("Similarities calculated.")
    if DEBUG:
        print("Similarities:")
        for i in range(len(similarities)):
            for j in range(len(similarities[i])):
                print(f"Similarity between sentence {i+1} and sentence {j+1}: {similarities[i][j]:.4f}")


if __name__ == "__main__":
    print(f"Starting the script with model: {MODELO}")
    logging.info(f"Starting the script with model: {MODELO}")
    main()
    logging.info("Script completed.")
    print("Script completed.")
