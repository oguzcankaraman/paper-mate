import os
import asyncio
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from pprint import pprint


class PdfProcessor:
    """
    Asenkron olarak PDF dosyalarını yüklemek ve işlemek için tasarlanmış sınıf.
    """

    def __init__(self):
        print("PdfProcessor başlatıldı. Kullanıma hazır.")

    # pdf_parser fonksiyonunu sınıf metodu (async def) olarak tanımlıyoruz
    async def parse_pdf(self, pdf_path: str) -> List[Document]:
        """
        Asenkron olarak belirtilen PDF dosyasını yükler ve Document listesi döndürür.
        """
        # 1. Dosya Var mı Kontrolü (Asenkron bağlamda senkron işlemi çalıştırma)
        # asyncio.to_thread kullanarak ana döngüyü bloklamaktan kaçınıyoruz.
        file_exist = await asyncio.to_thread(os.path.exists, pdf_path)

        if not file_exist:
            print(f"❌ HATA: Dosya bulunamadı → {pdf_path}")
            return []

        try:
            # 2. PDF'i yükle
            loader = PyPDFLoader(pdf_path)

            # LangChain'in asenkron yükleme metodu: aload()
            docs = await loader.aload()

            print(f"✅ Başarıyla yüklendi: {len(docs)} sayfa bulundu.")
            return docs

        except ValueError as ve:
            print(f"❌ HATA: PDF dosyası geçersiz veya bozuk. Detay: {ve}")
            return []

        except Exception as e:
            print(f"⚠️ Beklenmeyen bir hata oluştu: {e}")
            return []




# ----------------------------------------------------------------------
# Kullanım ve Test Bloğu (Asyncio ile)
# ----------------------------------------------------------------------

async def main_process():
    """
    PdfProcessor sınıfını test etmek için asenkron ana işlev.
    """
    # 1. Sınıf örneğini oluştur
    processor = PdfProcessor()

    # 2. Kullanıcıdan senkron bir şekilde girdi al
    pdf_path = input("📄 PDF dosya yolunu girin: ").strip().strip('"')

    # 3. Asenkron metodu çağırırken 'await' kullan
    docs = await processor.parse_pdf(pdf_path)

    if docs:
        print(f"\nToplam yüklü sayfa sayısı: {len(docs)}")
        for i, doc in enumerate(docs):
            print(f"\n--- 📄 Sayfa {i + 1} ---")
            # İçeriğin ilk 300 karakterini basıyoruz
            print(doc.page_content[:300] + "...")
            print("!! Metadata:")
            pprint(doc.metadata)
    else:
        print("❗Hiçbir içerik yüklenemedi.")


if __name__ == "__main__":
    # Asenkron ana fonksiyonu çalıştırmak için asyncio.run() kullanılır
    try:
        asyncio.run(main_process())
    except Exception as e:
        print(f"Uygulama çalıştırma hatası: {e}")