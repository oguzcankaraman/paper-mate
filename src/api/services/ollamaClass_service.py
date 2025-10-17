from langchain_core.messages import BaseMessage, AIMessage
from langchain_ollama import ChatOllama
from typing import List, Any, Coroutine
from src.ollama import OllamaClient

class ollamaClientService:
    def __init__(self):
        self.ollama_client = OllamaClient()
        print("OllamaClientService başlatıldı")


    async def invokeOllama(self, messages: List[BaseMessage]) -> dict[str, str | bool] | dict[str, str]:
        try:
            self.ollama_client.invoke(messages=messages)
            return{
                "success": True,
                "messages": "'messages' promptu başarıyla girildi "
            }
        except Exception as e:
            return {
                "success": False,
                "messages": "'messages' promptu başarısız oldu"

                    }