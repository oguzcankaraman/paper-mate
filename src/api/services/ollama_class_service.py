from langchain_core.messages import BaseMessage
from langchain_core.documents import Document
from typing import List
from src.ollama import OllamaClient
from src.ollama.ollamaClass import prompt_service


class OllamaClientService:
    def __init__(self):
        self.ollama_client = OllamaClient()
        print("OllamaClientService başlatıldı")



    async def api_summarizer(self, text_to_summarize: List[Document], length: str = "kısa ve öz") -> dict:
        try:
            if not prompt_service.prompts:
                await prompt_service.load_prompts()
            summary_message: BaseMessage = await self.ollama_client.summarizer(text_to_summarize=text_to_summarize, length=length)

            return{
                "success": True,
                "summary": summary_message.content
            }
        except Exception as e:
            return {

                "success": False,
                "text_to_summarize": "'text_to_summarize' başarısız oldu:" + str(e)
            }