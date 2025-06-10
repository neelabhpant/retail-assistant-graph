# utils/llm_loader.py
from langchain_openai import ChatOpenAI
from config.config import settings

def load_llm():
    """Loads and returns the language model instance."""
    return ChatOpenAI(
        api_key=settings.openai_api_key,
        model=settings.openai_model_name,
        temperature=0
    )

llm = load_llm()