from langchain_core.messages import BaseMessage, AIMessage
from langchain_ollama import ChatOllama

from typing import List


class OllamaClient:
    def __init__(self, model_name: str ="llama3:8b"):
        print(f"{model_name} başlatılıyor")
        self.chat_model = ChatOllama(model="llama3:8b")

        print("Başlatıldı")

    def invoke(self, messages: List[BaseMessage]) -> BaseMessage:
        #verilen prompt ile modeli çağırıp yanıtı döndürür
        try:
            # invoke metodunu çağırarak mesaj listesini doğrudan gönderiyoruz
            response = self.chat_model.invoke(messages)
            return response
        except Exception as e:
            return AIMessage(content=f"Bir hata oluştu: {e}")