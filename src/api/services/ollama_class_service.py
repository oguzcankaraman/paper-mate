from langchain_core.messages import BaseMessage
from typing import List
from src.ollama import OllamaClient

class ollamaClientService:
    def __init__(self):
        self.ollama_client = OllamaClient()
        print("OllamaClientService başlatıldı")



    async def api_summerizer(self, text_to_summarize: List[BaseMessage], length: str = "kısa ve öz") -> dict[str, str | bool] | dict[str, str]:
        try:
            await self.ollama_client.summerizer(text_to_summarize=text_to_summarize, length=length)
            return{
                "success": True,
                "text_to_summarize": "'text_to_summarize' başarılı oldu"
            }
        except Exception as e:
            return {
                "success": False,
                "text_to_summarize": "'text_to_summarize' başarısız oldu"
            }