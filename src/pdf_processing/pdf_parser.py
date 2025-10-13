import os
import pprint
from langchain_community.document_loaders import PyPDFLoader
import os

pdf_path = input("PDF yolu: ").strip().strip('"')


print(f"📄 Girilen yol: {pdf_path}")
print("✅ Dosya gerçekten var mı?", os.path.exists(pdf_path))

if not os.path.exists(pdf_path):
    print(f"❌ HATA: Dosya bulunamadı → {pdf_path}")
else:
    try:
        loader = PyPDFLoader(pdf_path)

        docs = loader.load()

        for i ,doc in enumerate(docs):
           print(f"--- Sayfa {i + 1} ---")
           print(doc.page_content)
           pprint.pprint(doc.metadata)
           print()

    except ValueError as e:
     print(f"❌ HATA: PDF dosyası geçersiz veya bozuk. Detay: {e}")

    except Exception as e:
     print(f"⚠️ Beklenmeyen bir hata oluştu: {e}")






