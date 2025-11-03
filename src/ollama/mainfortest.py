
# run_summary.py
import asyncio


from langchain_core.documents import Document
from typing import List
from src.api.services.prompt_service import PromptService

# ollama_client.py dosyasından OllamaClient sınıfını içe aktar
from ollamaClass import OllamaClient



# 'summarizer' metodu için main fonksiyonu
async def main():

    service = PromptService(file_path="ollama/promptOllama.json")
    await service.load_prompts()

    try:
        client = OllamaClient(model_name="llama3:8b")
    except Exception as e:
        print(
            f"\n!! HATA: OllamaClient başlatılamadı. Ollama sunucunuzun ve 'llama3:8b' modelinin çalıştığından emin olun. Hata: {e}")
        return

        # 1. Örnek Metni Parçalara Ayırıp List[Document] Haline Getirme
    parca_1 = """Yapay zeka, bilgisayarların insan zekasını taklit etmesini sağlayan bir bilim dalıdır.
    Bu teknoloji, öğrenme, problem çözme, karar verme ve dil anlama gibi yeteneklere
    sahip sistemler geliştirmeyi amaçlar."""

    parca_2 = """Yapay zeka, makine öğrenimi, derin öğrenme, doğal dil işleme (NLP) ve bilgisayarla görme
    gibi alt alanlara ayrılır. Günümüzde, sağlık, finans, otomotiv ve e-ticaret gibi pek çok
    sektörde yaygın olarak kullanılmaktadır."""

    # List[Document] yapısını oluşturma
    ornek_document_listesi: List[Document] = [
        Document(page_content=parca_1, metadata={"source": "giris_paragrafi"}),
        Document(page_content=parca_2, metadata={"source": "alt_alanlar_paragrafi"})
    ]

    print("\n=============================================")
    print("Özetlenecek Metin (List[Document] İçeriği):\n---")
    # Kullanıcıya göstermek için içeriği birleştiriyoruz
    print(ornek_document_listesi[0].page_content.strip())
    print("...")
    print(ornek_document_listesi[1].page_content.strip())
    print("---")
    print(f"Gönderilen Tip: {type(ornek_document_listesi)} (List[Document])")
    print("=============================================")

    # 2. Özetleme Metodunu Çağırma (List[Document] kullanılarak)
    print("\n>>> Senaryo 1: 'kısa ve öz' özetleme <<<")
    # text_to_summarize'a List[Document] nesnesini doğrudan iletiyoruz.
    summary_1 = await client.summarizer(text_to_summarize=ornek_document_listesi, length="kısa ve öz")

    print("\n--- SONUÇ 1 (Kısa ve Öz) ---")
    print(f"Yanıt Tipi: {type(summary_1)}")
    print("Özet İçeriği:")
    print(summary_1.content)
    print("---------------------------------\n")


# Ana fonksiyonu çalıştır
if __name__ == "__main__":
    asyncio.run(main())

