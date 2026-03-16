import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Base Directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

class Settings(BaseSettings):
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # LangChain / LangSmith Tracing
    LANGCHAIN_TRACING_V2: str = os.getenv("LANGCHAIN_TRACING_V2", "false")
    LANGCHAIN_API_KEY: str = os.getenv("LANGCHAIN_API_KEY", "")
    LANGCHAIN_PROJECT: str = os.getenv("LANGCHAIN_PROJECT", "duy-tan-chatbox")
    LANGCHAIN_ENDPOINT: str = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
    
    # Path configuration
    DATA_PATH: Path = BASE_DIR / "data"
    SOURCES_PATH: Path = DATA_PATH / "sources"
    CHROMA_PATH: Path = DATA_PATH / "chromadb"
    
    # ChromaDB Configuration
    CHROMA_COLLECTION_NAME: str = "admission_data"
    
    # Model Configuration
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    CHAT_MODEL: str = "gpt-4o-mini"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
