from langchain_core.messages import BaseMessage, AIMessage
from langchain_ollama import ChatOllama
from typing import List, Any, Coroutine
from src.ollama import OllamaClient

class ollamaClientService:
    def __init__(self):
        self.ollama_client = OllamaClient()
        print("OllamaClientService başlatıldı")



    async def prompt_summerizer(self, text_to_summarize: str, length: str = "kısa ve öz") -> dict[str, str | bool] | dict[str, str]:
        try:
            self.ollama_client.summarize_prompt(text_to_summarize=text_to_summarize, length=length)
            return{
                "success": True,
                "text_to_summarize": "'text_to_summarize' başarılı oldu"
            }
        except Exception as e:
            return {
                "success": False,
                "text_to_summarize": "'text_to_summarize' başarısız oldu"
            }