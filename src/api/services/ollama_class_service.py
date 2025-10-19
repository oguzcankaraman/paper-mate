from langchain_core.messages import BaseMessage
from typing import List
from src.ollama import OllamaClient

class ollamaClientService:
    def __init__(self):
        self.ollama_client = OllamaClient()
        print("OllamaClientService başlatıldı")



    async def api_summarizer(self, text_to_summarize: List[BaseMessage], length: str = "kısa ve öz") -> dict:
        try:
            summary_message: BaseMessage = await self.ollama_client.summarizer(text_to_summarize=text_to_summarize, length=length)

            return{
                "summary": summary_message.content
            }
        except Exception as e:
            return {

                "success": False,
                "text_to_summarize": "'text_to_summarize' başarısız oldu"
            }