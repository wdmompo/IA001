from datetime import datetime
from dotenv import load_dotenv
import os
from pathlib import Path
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
import re
import tomllib
from typing import Any, Dict

# from helpers.decorators import medir_tiempo_ms


# detectar entorno
load_dotenv(override=True)
APP_ENV = os.getenv("APP_ENV", "DEV").upper()

# elegir archivo .env dinámicamente
env_file = Path(f".env.{APP_ENV.lower()}") if Path(f".env.{APP_ENV.lower()}").exists() else Path(".env")
# print(f"Cargando variables de entorno desde: {env_file}")


# @medir_tiempo_ms
def load_config_from_toml() -> Dict[str, Any]:
    """
    Carga la configuración desde un archivo TOML.

    Args:

    Returns:
        Dict[str, Any]: Un diccionario con la configuración cargada.
    """
    config_path = Path("config.toml")
    if not config_path.exists():
        raise FileNotFoundError(f"El archivo de configuración {config_path} no existe.")

    with open(config_path, "rb") as f:
        config_data = tomllib.load(f)
    
    return config_data


def convert_text(text: str) -> str:
    """
    Convierte el texto a un formato seguro para usar en nombres de archivos.

    Args:
        text (str): El texto a convertir.

    Returns:
        str: El texto convertido.
    """
    # Reemplazar variables en el texto
    safe_text = text
    safe_text = safe_text.replace("{DATE}", datetime.now().strftime("%Y%m%d"))             # Reemplaza {DATE} con la fecha actual
    safe_text = safe_text.replace("{TIME}", datetime.now().strftime("%H%M%S"))             # Reemplaza {TIME} con la hora actual
    safe_text = safe_text.replace("{DATETIME}", datetime.now().strftime("%Y%m%d_%H%M%S"))  # Reemplaza {DATETIME} con la fecha y hora actual
    return safe_text


class Settings(BaseSettings):
    LOGGING_MODE: str                           # config.toml
    LOGGING_FILENAME: str                       # config.toml
    LOGGING_FORMAT: str                         # config.toml
    LOGGING_ENCODING: str                       # config.toml
    LOGGING_FILEMODE: str                       # config.toml
    LOGGING_LEVEL: str                          # config.toml
    LOGGING_DATABASE_URL: str                   # config.toml
    LOGGING_DATABASE_TABLE: str                 # config.toml

    MODEL_NAME: str                             # config.toml

    INPUTS_EXPRESIONES_A_DESCARTAR: str         # config.toml
    INPUTS_FRASES_DE_REFERENCIA: str            # config.toml
    INPUTS_OPINIONES: str                       # config.toml

    LOGGING_DATABASE_USER: str = "user"         # .ENV
    LOGGING_DATABASE_PASSWORD: str = "password" # .ENV
    LOGGING_DATABASE_HOST: str = "host"         # .ENV
    LOGGING_DATABASE_PORT: str = "port"         # .ENV
    LOGGING_DATABASE_NAME: str = "name"         # .ENV

    @property
    def safe_db_url(self):
        return re.sub(
            r"(^[^:]+:\/\/)([^:]+):([^@]+)@",
            r"\1*****:*****@",
            self.LOGGING_DATABASE_URL,
        )

    @property
    def database_url_resolved(self):
        """
        Devuelve la URL de la base de datos con las variables de entorno reemplazadas.
        """
        safe_text = self.LOGGING_DATABASE_URL
        safe_text = convert_text(safe_text)
        variables = re.findall(r"\{([A-Z_]+)\}", safe_text)
        variables_valores = {variable: getattr(self, variable) for variable in variables}
        for var in variables_valores:
            safe_text = safe_text.replace(f"{{{var}}}", variables_valores[var])
        return safe_text
    
    # Configuración de Pydantic para cargar variables de entorno desde un archivo .env
    model_config = SettingsConfigDict(
        env_file=env_file if env_file.exists() else None,
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # @medir_tiempo_ms
    @classmethod
    def load_from_toml(cls):
        config_data = load_config_from_toml()
        logging_config = config_data.get("logging", {})
        model_config = config_data.get("model", {})
        inputs_config = config_data.get("inputs", {})

        return cls(
            LOGGING_MODE=logging_config.get("mode", "file"),
            LOGGING_FILENAME=convert_text(logging_config.get("filename", "AnalizadorDeOpiniones.log")),
            LOGGING_FORMAT=logging_config.get(
                "format",
                "%(asctime)s [%(levelname)s] (%(name)s) (%(filename)s:%(lineno)d) %(message)s",
            ),
            LOGGING_ENCODING=logging_config.get("encoding", "utf-8"),
            LOGGING_FILEMODE=logging_config.get("filemode", "a"),
            LOGGING_LEVEL=logging_config.get("level", "DEBUG"),
            LOGGING_DATABASE_URL=logging_config.get("database_url", "sqlite:///./{LOGGING_DATABASE_NAME}.db"),
            LOGGING_DATABASE_TABLE=logging_config.get("database_table", "log_analizador_de_opiniones"),

            MODEL_NAME=model_config.get("name", "default-model"),

            INPUTS_EXPRESIONES_A_DESCARTAR=inputs_config.get("expresiones_a_descartar", "expresiones_a_descartar.txt"),
            INPUTS_FRASES_DE_REFERENCIA=inputs_config.get("frases_de_referencia", "frases_de_referencia.txt"),
            INPUTS_OPINIONES=inputs_config.get("opiniones", "opiniones.txt"),
        )

settings = Settings.load_from_toml()
