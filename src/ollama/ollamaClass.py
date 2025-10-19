from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
from langchain_ollama import ChatOllama
from typing import List


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

    async def summerizer(self, text_to_summarize: List[BaseMessage], length: str = "kısa ve öz") -> BaseMessage:
        """
        Asenkron olarak verilen metni özetleyen ve yanıtı bir AIMessage nesnesi olarak döndüren metot.

        Args:
            text_to_summarize (str): Özetlenmesi istenen metin.
            length (str): Özetin uzunluğu/tarzı.

        Returns:
            BaseMessage: Modelden gelen özet yanıtı (AIMessage).
        """
        print(f"\n--- Asenkron Özetleme İşlemi Başladı ---")

        # 1. Sistem Mesajı (Modeli Yönlendirme)
        system_instruction = (
            f"Sen bir özetleme uzmanısın. Görevin, sana verilen metni 'Türkçe' olarak "
            f"'{length}' bir şekilde, en önemli noktaları vurgulayarak özetlemektir. "
            "Ek yorum yapma, sadece özeti döndür."
        )
        system_message = SystemMessage(content=system_instruction)

        # 2. Kullanıcı Mesajı (Özetlenecek Metin)
        human_message = HumanMessage(content=text_to_summarize)

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
        return summary_response


