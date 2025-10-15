import chromadb
from typing import Optional

from langchain_core.documents import Document

# Chroma'ya bağlanmak için bir istemci eklendi.
client = chromadb.Client()
# Koleksiyon oluşturma kısmı.
collection = client.get_or_create_collection(name='test_collection')


# LangChain Document nesnelerini bir listede tanımlama.
documents_to_add = [
    Document(
        page_content="Ben 21 yaşındayım.",
        metadata={"source": "mammal-pets-doc"},
    ),
    Document(
        page_content="Yapay zeka çok ilginç.",
        metadata={"source": "mammal-pets-doc"},
    ),
    Document(
        page_content="Ankara'da yaşıyorum.",
        metadata={"source": "mammal-pets-doc"},
    )
]


contents = [doc.page_content for doc in documents_to_add]
metadatas = [doc.metadata for doc in documents_to_add]
ids = [f"id{i+1}" for i in range(len(documents_to_add))]



if collection.count() == 0:
    print("Koleksiyon boş, dokümanlar ekleniyor...")
    collection.add(
        documents=contents,
        metadatas=metadatas,
        ids=ids
    )

# kaç doküman olduğunu kontrol et.
print(f"Koleksiyonda toplam {collection.count()} adet doküman var.")


# --- find_document fonksiyonu
#bu fonksiyon rag.py'da 'search_context' içinde kullanılacak.
def find_document(query: str) -> Optional[Document]:
    results = collection.query(
        query_texts=[query],
        n_results=1,
        include=["metadatas", "documents"]
    )

    if results and results['documents'][0]:
        page_content = results['documents'][0][0]
        metadata = results['metadatas'][0][0]
        return Document(page_content=page_content, metadata=metadata)
    else:
        return None

# fonksiyon kullanımı için bir örnek
search_query = "Yapay zeka uygulamaları"
found_doc = find_document(search_query)

print(f"\n'{search_query}' araması için bulunan sonuç:")

if found_doc:
    print("Bulunan Döküman Tipi:", type(found_doc))
    print("Döküman İçeriği:", found_doc.page_content)
    print("Döküman Metadatası:", found_doc.metadata)
else:
    print("İlgili doküman bulunamadı.")