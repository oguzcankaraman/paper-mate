import chromadb
from typing import List
from langchain_core.documents import Document
import asyncio


class VectorStore:

    def __init__(self):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.client.get_or_create_collection(
            name='main_user_collection'
        )
        print(f"VectorStore başlatıldı. Koleksiyon: '{self.collection.name}'")

    async def add_user_documents(self, user_id: str, documents: List[Document]):
        """Belirtilen kullanıcının dökümanlarını ana koleksiyona ekler."""
        contents = [doc.page_content for doc in documents]
        metadatas = [{"user_id": user_id, **doc.metadata} for doc in documents]
        ids = [f"user_{user_id}_doc_{i}" for i in range(len(documents))]

        await asyncio.to_thread(self.collection.add, documents=contents, metadatas=metadatas, ids=ids)

    async def find_document(self, user_id: str, query: str) -> List[Document]:
        results =  await asyncio.to_thread(self.collection.query,
            query_texts=[query],
            n_results=5,
            # aramanın sadece user_id'si eşleşen dokümanlarda yapılmasını sağlar.
            where={"user_id": user_id},
            include=["metadatas", "documents"]
        )
        found_documents = []
        if results and results['documents'][0]:
            # gelen tüm sonucları isleyen bir döngü
            for content, metadata in zip(results['documents'][0], results['metadatas'][0]):
                found_documents.append(
                    Document(page_content=content, metadata=metadata)
                )

        return found_documents

    async def delete_user_documents(self, user_id: str):
        """Ana koleksiyondan belirtilen kullanıcıya ait tüm dökümanları siler."""
        print(f"'{self.collection.name}' koleksiyonundan '{user_id}' kullanıcısının verileri siliniyor...")
        try:
            # sadece o kullanıcıya ait verileri sil
            await asyncio.to_thread(self.collection.delete, where={"user_id": user_id})
            print(f"'{user_id}' kullanıcısının verileri silindi.")
        except Exception as e:
            print(f"Veriler silinirken bir hata oluştu: {e}")


#---------------------------Main Test BLogu---------------------------
if __name__ == "__main__":
    async def main():
        test_user_id = "12345"
        # VectorStore nesnesi oluşturma
        vector_store_instance = VectorStore()

        sample_docs = [
            Document(page_content="Yapay zeka etiği, algoritmaların adil ve şeffaf olmasını amaçlar.", metadata={"source": "makale_1.pdf"}),
            Document(page_content="Ankara, Türkiye'nin başkenti ve en kalabalık ikinci şehridir.", metadata={"source": "cografya_kitabi.pdf"}),
            Document(page_content="Türkiye'nin en yüksek dağı Ağrı Dağı'dır.",metadata={"source": "cografya_kitabi.pdf"})
        ]

        query_search = "Türkiye'nin coğrafi özellikleri nelerdir?"
        # metotları çağırma kısmı
        await vector_store_instance.add_user_documents(user_id=test_user_id, documents=sample_docs)
        found_docs_list = await vector_store_instance.find_document(
            user_id=test_user_id,
            query=query_search,
            top_k=2
        )
        print(f"Sorulan soru : {query_search}")
        print(f"\nBulunan sonuçlar ({len(found_docs_list)} adet):")
        if found_docs_list:
            # listenin içindeki her bir dokümanı ayrı ayrı yazdırma kısmı.
            for i, doc in enumerate(found_docs_list):
                print(f"--- Sonuç {i + 1} ---")
                print(f"  İçerik: {doc.page_content}")
                print(f"  Metadata: {doc.metadata}")
        else:
            print("  İlgili doküman bulunamadı.")

        await vector_store_instance.delete_user_documents(user_id=test_user_id)

    asyncio.run(main())