from src.api.services.prompt_service import PromptService
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
from langchain_core.documents import Document
from langchain_ollama import ChatOllama
from typing import List
import asyncio

prompt_service = PromptService(file_path="prompts/promptOllama.json")

class OllamaClient:
    def __init__(self, model_name: str ="llama3:8b"):
        print(f"{model_name} başlatılıyor")
        self.chat_model = ChatOllama(model="llama3:8b")

        print("Başlatıldı")

    async def ainvoke(self, messages: List[BaseMessage]) -> BaseMessage:
        """Asenkron temel invoke metodu."""
        try:
            # Burası LangChain'in kendi ainvoke metodudur
            return await self.chat_model.ainvoke(messages)
        except Exception as e:
            return AIMessage(content=f"Bir hata oluştu: {e}")

    async def summarizer(self, text_to_summarize: List[Document], length: str = "kısa ve öz") -> dict:
        """
        Asenkron olarak verilen metni özetleyen ve yanıtı bir AIMessage nesnesi olarak döndüren metot.

        Args:
            text_to_summarize (str): Özetlenmesi istenen metin.
            length (str): Özetin uzunluğu/tarzı.

        Returns:
            BaseMessage: Modelden gelen özet yanıtı (AIMessage).
        """
        print(f"\n--- Asenkron Özetleme İşlemi Başladı ---")
        service = PromptService(file_path="prompts/promptOllama.json")
        await service.load_prompts()
        # 1. Sistem Mesajı (Modeli Yönlendirme)
        system_instruction = prompt_service.get_prompt(
            category="SYSTEM_INSTRUCTIONS",
            key="SUMMARY_EXPERT",
            # Prompt'taki {length} alanını doldurmak için kwargs kullanılıyor
            length=length
        )
        if not system_instruction:
            # Yedek prompt kullan (hata durumunda)
            system_instruction = "Lütfen metni kısaca özetle. Metin içeriğinin dışına çıkma ve herhangi bir ek bilgi kullanma"

        system_message = SystemMessage(content=system_instruction)
        combined_text = "\n\n".join([doc["content"] for doc in text_to_summarize])
        print("ŞU ANDA BURADASINIZ !!!!!!!!!!!!!!!!!!")
        print(f"{combined_text}")

        # 2. Kullanıcı Mesajı (Özetlenecek Metin)
        human_message = HumanMessage(content=combined_text)

        # 3. Mesaj Listesi
        messages_for_summary = [
            system_message,
            human_message
        ]

        # 4. Asenkron Invoke Metodunu Çağırma
        # await anahtar kelimesi, ainvoke işleminin tamamlanmasını asenkron olarak bekler.
        summary_response = await self.ainvoke(messages_for_summary)

        print("--- Asenkron Özetleme İşlemi Tamamlandı ---")

        # BaseMessage (AIMessage) nesnesini döndür
        return summary_response.content


