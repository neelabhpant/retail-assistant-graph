# config/config.py
import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # OpenAI API Configuration
    openai_api_key: str
    openai_model_name: str = "gpt-4o"

    # Embedding Model Configuration
    embedding_model_name: str = "all-MiniLM-L6-v2"

    # Neo4j Database Configuration
    neo4j_uri: str
    neo4j_username: str
    neo4j_password: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = 'ignore'

settings = Settings()