from backend.utils.config import OPENAI_API_KEY
from langchain_openai import ChatOpenAI


def get_llm():
    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=OPENAI_API_KEY
    )
