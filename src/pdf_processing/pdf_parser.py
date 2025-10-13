import os
import pprint
from langchain_community.document_loaders import PyPDFLoader

# Kullanıcıdan dosya yolu al
pdf_path = input("PDF yolu: ").strip().strip('"')
print("Yol:", pdf_path)
print("Var mı?", os.path.exists(pdf_path))

# Dosya var mı kontrol et
if not os.path.exists(pdf_path):
    print(f"❌ HATA: Dosya bulunamadı → {pdf_path}")
else:
    try:
        # PDF'i yükle
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()

        # Sayfa sayfa içeriği ve metadata'yı yazdır
        for i, doc in enumerate(docs):
            print(f"\n--- Sayfa {i + 1} ---")
            print(doc.page_content)
            pprint.pprint(doc.metadata)

    except ValueError as ve:
        print(f"❌ HATA: PDF dosyası geçersiz veya bozuk. Detay: {ve}")

    except Exception as e:
        print(f"⚠️ Beklenmeyen bir hata oluştu: {e}")
