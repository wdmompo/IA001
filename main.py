from app.calculate_embeddings import calculate_embeddings
from app.data_cleaning import opinions_cleaning
from app.files_load import files_load
from app.model_load import model_load
from helpers.config import settings
from helpers.decorators import medir_tiempo_ms
from helpers.ia import get_model_device, model_load, model_encode, model_similarity
from logger import get_logger


logger = get_logger(__name__)


@medir_tiempo_ms
def main():


    print(f"Starting the script with model: {settings.MODEL_NAME}")
    logger.info(f"Starting the script with model", extra={'model': settings.MODEL_NAME})

    device = get_model_device()

    # Proceso general
    expresiones_a_descartar, frases_de_referencia, opiniones = files_load()
    opiniones = opinions_cleaning(opiniones)
    model = model_load(settings.MODEL_NAME, device)
    embeddings_frases_de_referencia, embeddings_opiniones = calculate_embeddings(model, frases_de_referencia, opiniones, device)

    # Calcular la similitud entre los vectores
    print("\nCalculating similarities...")
    # 4. Verificar qué métrica matemática utiliza el modelo por defecto
    print(f"Métrica de comparación interna del modelo: '{model.similarity_fn_name}'")
    logger.info(f"Métrica de comparación interna del modelo.", extra={'model.similarity_fn_name': model.similarity_fn_name})
    similarities = model_similarity(model, embeddings_frases_de_referencia, embeddings_opiniones)
    logger.info(f"Similarities calculated.", extra={'model.device': model.device})
    # if DEBUG:
    #     print("Similarities:")
    #     for i in range(len(similarities)):
    #         for j in range(len(similarities[i])):
    #             print(f"Similarity between sentence {i+1} and sentence {j+1}: {similarities[i][j]:.4f}")


    logger.info("Script completed.")
    print("Script completed.")


if __name__ == "__main__":
    main()
