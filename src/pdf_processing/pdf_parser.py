import os
import asyncio
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pprint import pprint


class PdfProcessor:
    """
    Asenkron olarak PDF dosyalarını yüklemek ve işlemek için tasarlanmış sınıf.
    """

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Başlatıcı. Text Splitterı yapılandırır.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            # Genellikle bu ayar ile metinler sırayla newline, çift newline, boşluk vs. ile bölünür.
            separators=["\n\n", "\n", " ", ""],
            length_function=len
        )
        print(f"PdfProcessor başlatıldı. Parça boyutu: {chunk_size}, Örtüşme: {chunk_overlap}")

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

    async def process_and_chunk_pdf(self, pdf_path: str) -> List[Document]:
            """
            PDF'i yükler, LangChain Document formatına çevirir ve ardından küçük parçalara (chunk) ayırır.

            :param pdf_path: İşlenecek PDF dosyasının yolu.
            :return: Parçalara ayrılmış metinleri (Document nesneleri) içeren bir liste.
            """
            print(f"\n--- 1. Yükleme ve Formatlama Başlıyor: {pdf_path} ---")

            # AŞAMA 1: Mevcut metodu kullanarak yükleme (parse_pdf)
            # Bu aşama, PDF'i okur ve her sayfayı bir Document yapar.
            page_documents = await self.parse_pdf(pdf_path)

            if not page_documents:
                print("❗ Yüklenecek sayfa bulunamadı. İşlem sonlanıyor.")
                return []

            # AŞAMA 2: Parçalara Ayırma (Chunking)
            print("\n--- 2. Parçalara Ayırma (Chunking) Başlıyor ---")
            # Text splitter'ın asenkron versiyonu yoktur, senkron çalıştırıyoruz.

            # from_documents metodu, yüklenen tüm Document'ları alır ve parçalara ayırır.
            chunk_documents = await asyncio.to_thread(
                self.text_splitter.split_documents,
                page_documents
            )

            print(f"✅ Parçalama tamamlandı. Toplam {len(chunk_documents)} parça üretildi.")
            return chunk_documents




# ----------------------------------------------------------------------
# Kullanım ve Test Bloğu (Asyncio ile)
# ----------------------------------------------------------------------

async def main_process():
    """
    PdfProcessor sınıfını test etmek için asenkron ana işlev.
    """
    # 1. Sınıf örneğini oluştur ve chunking parametrelerini belirle
    processor = PdfProcessor(chunk_size=1500, chunk_overlap=150)

    # 2. Kullanıcıdan senkron bir şekilde girdi al
    pdf_path = input("📄 PDF dosya yolunu girin: ").strip().strip('"')

    # 3. **İstenen Tek Metodu Çağır** (hem yükleme hem parçalama yapar)
    chunks = await processor.process_and_chunk_pdf(pdf_path)

    if chunks:
        print(f"\n--- Toplam Parça Sayısı: {len(chunks)} ---")
        for i, chunk in enumerate(chunks):
            print(f"\n--- 📄 Parça {i + 1} ---")
            # İçeriğin ilk 300 karakterini basıyoruz
            print(chunk.page_content[:300] + "...")
            print("!! Metadata (Chunking sonrası sayfa numarası, kaynak vb. korunur):")
            pprint(chunk.metadata)
    else:
        print("❗Hiçbir içerik yüklenemedi veya parça üretilemedi.")


if __name__ == "__main__":
    # Asenkron ana fonksiyonu çalıştırmak için asyncio.run() kullanılır
    try:
        asyncio.run(main_process())
    except Exception as e:
        print(f"Uygulama çalıştırma hatası: {e}")