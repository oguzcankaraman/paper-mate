import chromadb
from typing import Optional, List
from langchain_core.documents import Document


class VectorStore:

    def __init__(self):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.client.get_or_create_collection(
            name='main_user_collection'
        )
        print(f"VectorStore başlatıldı. Koleksiyon: '{self.collection.name}'")

    def add_user_documents(self, user_id: str, documents: List[Document]):
        """Belirtilen kullanıcının dökümanlarını ana koleksiyona ekler."""
        contents = [doc.page_content for doc in documents]
        metadatas = [{"user_id": user_id, **doc.metadata} for doc in documents]
        ids = [f"user_{user_id}_doc_{i}" for i in range(len(documents))]

        self.collection.add(documents=contents, metadatas=metadatas, ids=ids)

    def find_document(self, user_id: str, query: str) -> Optional[Document]:
        results = self.collection.query(
            query_texts=[query],
            n_results=1,
            # aramanın sadece user_id'si eşleşen dokümanlarda yapılmasını sağlar.
            where={"user_id": user_id},
            include=["metadatas", "documents"]
        )
        if results and results['documents'][0]:
            page_content = results['documents'][0][0]
            metadata = results['metadatas'][0][0]
            return Document(page_content=page_content, metadata=metadata)
        return None

    def delete_user_documents(self, user_id: str):
        """Ana koleksiyondan belirtilen kullanıcıya ait tüm dökümanları siler."""
        print(f"'{self.collection.name}' koleksiyonundan '{user_id}' kullanıcısının verileri siliniyor...")
        try:
            # sadece o kullanıcıya ait verileri sil
            self.collection.delete(where={"user_id": user_id})
            print(f"'{user_id}' kullanıcısının verileri silindi.")
        except Exception as e:
            print(f"Veriler silinirken bir hata oluştu: {e}")


#---------------------------Main Test BLogu---------------------------
if __name__ == "__main__":
    test_user_id = "12345"
    # VectorStore nesnesi oluşturma
    vector_store_instance = VectorStore()

    sample_docs = [
        Document(page_content="Yapay zeka etiği, algoritmaların adil ve şeffaf olmasını amaçlar.", metadata={"source": "makale_1.pdf"}),
        Document(page_content="Ankara, Türkiye'nin başkenti ve en kalabalık ikinci şehridir.", metadata={"source": "cografya_kitabi.pdf"})
    ]

    # metotları user_id ile çağırma
    vector_store_instance.add_user_documents(user_id=test_user_id, documents=sample_docs)
    found_doc = vector_store_instance.find_document(user_id=test_user_id, query="Başkent neresidir?")

    print(f"\nBulunan sonuç: {found_doc.page_content if found_doc else 'Bulunamadı.'}")

    vector_store_instance.delete_user_documents(user_id=test_user_id)