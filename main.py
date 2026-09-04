# import logging

from app.files_load import files_load
from helpers.config import settings
from helpers.decorators import medir_tiempo_ms
from helpers.file_functions import cargar_datos_desde_txt
from helpers.ia import get_model_device, model_load, model_encode, model_similarity
from helpers.text_functions import limpiar_texto
from logger import get_logger


DEBUG = False
MODELO = settings.MODEL_NAME  # Modelo preentrenado para obtener embeddings de oraciones
         # Otros modelos: 'all-MiniLM-L6-v2'


@medir_tiempo_ms
def main():
    logger = get_logger(__name__)


    print(f"Starting the script with model: {MODELO}")
    logger.info(f"Starting the script with model", extra={'model': MODELO})


    expresiones_a_descartar, frases_de_referencia, opiniones = files_load()


    # Limpiar opiniones
    print("\nCleaning opinions...")
    logger.info(f"Cleaning opinions...")
    opiniones = [opinion for opinion in opiniones if opinion.strip()]
    print(f"Opinions after removing empty lines: {len(opiniones)}")
    opiniones = [limpiar_texto(opinion) for opinion in opiniones if limpiar_texto(opinion)]
    logger.info(f"Cleaned opinions.", extra={'opinions count': len(opiniones)})
    print(f"Cleaned opinions: {len(opiniones)}")


    # Cargar un modelo preentrenado
    print(f"\nLoading model {MODELO}...")
    logger.info(f"Loading model...", extra={'model': MODELO})
    # Detectar automáticamente el mejor dispositivo disponible
    device = get_model_device()
    try:
        model = model_load(MODELO, device)
    except Exception as e:
        logger.info(f"Error loading model {e}.", extra={'model': MODELO})
        print(f"Error loading model {e}.")
    else:
        logger.info(f"Model loaded successfully.", extra={'model.device': model.device})
        print(f"Model loaded successfully in {model.device}.")


    # Codificar oraciones para obtener sus embeddings
    print(f"\nEncoding sentences (frases de referencia)...")
    embeddings_frases_de_referencia = model_encode(model, frases_de_referencia, device)
    logger.info(f"Sentences encoded.", extra={'model.device': model.device})
    if DEBUG:
        print("Embeddings:")
        for i, embedding in enumerate(embeddings_frases_de_referencia):
            print(f"Sentence {i+1} embedding: {embedding[:5]}...")  # Mostrar solo los primeros 5 valores del embedding


    # Codificar oraciones para obtener sus embeddings
    print("\nEncoding sentences (opiniones)...")
    embeddings_opiniones = model_encode(model, opiniones, device)
    logger.info(f"Sentences encoded.", extra={'model.device': model.device})
    if DEBUG:
        print("Embeddings:")
        for i, embedding in enumerate(embeddings_opiniones):
            print(f"Sentence {i+1} embedding: {embedding[:5]}...")  # Mostrar solo los primeros 5 valores del embedding


    # Calcular la similitud entre los vectores
    print("\nCalculating similarities...")
    # 4. Verificar qué métrica matemática utiliza el modelo por defecto
    print(f"Métrica de comparación interna del modelo: '{model.similarity_fn_name}'")
    logger.info(f"Métrica de comparación interna del modelo.", extra={'model.similarity_fn_name': model.similarity_fn_name})
    similarities = model_similarity(model, embeddings_frases_de_referencia, embeddings_opiniones)
    logger.info(f"Similarities calculated.", extra={'model.device': model.device})
    if DEBUG:
        print("Similarities:")
        for i in range(len(similarities)):
            for j in range(len(similarities[i])):
                print(f"Similarity between sentence {i+1} and sentence {j+1}: {similarities[i][j]:.4f}")


    logger.info("Script completed.")
    print("Script completed.")


if __name__ == "__main__":
    main()
