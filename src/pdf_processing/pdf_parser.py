import os

from pprint import pprint
from langchain_community.document_loaders import PyPDFLoader
from typing import List
from langchain_core.documents import Document


def pdf_parser(pdf_path: str) -> List[Document]:

    if not os.path.exists(pdf_path):
        print(f"❌ HATA: Dosya bulunamadı → {pdf_path}")
        return []

    try:
        # PDF'i yükle
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()

        print(f"✅ Başarıyla yüklendi: {len(docs)} sayfa bulundu.")
        return docs

    except ValueError as ve:
        print(f"❌ HATA: PDF dosyası geçersiz veya bozuk. Detay: {ve}")
        return []

    except Exception as e:
        print(f"⚠️ Beklenmeyen bir hata oluştu: {e}")
        return []


# Main bloğu
if __name__ == "__main__":
    pdf_path = input("📄 PDF dosya yolunu girin: ").strip().strip('"')

    docs = pdf_parser(pdf_path)

    if docs:
        for i, doc in enumerate(docs):
            print(f"\n--- 📄 Sayfa {i + 1} ---")
            print(doc.page_content)  # İçeriğin ilk 300 karakteri
            print("!! Metadata:")
            pprint(doc.metadata)
    else:
        print("❗Hiçbir içerik yüklenemedi.")









