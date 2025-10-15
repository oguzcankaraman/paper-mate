import asyncio
from typing import List
from langchain_core.documents import Document

# VectorStore sınıfını import
from src.rag import VectorStore


class VectorDatabaseService:
    def __init__(self):
        print("VectorDatabaseService başlatıldı.")

    async def add_documents_for_user(self, user_id: str, documents: List[Document]) -> dict:

        try:
            # VectorStore'u başlat.
            user_vector_store = VectorStore(user_id=user_id)

            # kullanıcının koleksiyonuna dokümanları ekle.
            user_vector_store.add_user_documents(documents=documents)

            return {
                "success": True,
                "message": f"'{user_id}' kullanıcısı için {len(documents)} doküman başarıyla eklendi."
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"'{user_id}' kullanıcısı için doküman eklenemedi: {str(e)}"
            }

    async def search_for_user(self, user_id: str, query: str) -> dict:
        """
        Belirtilen kullanıcının dokümanları içinde arama yapar.
        """
        try:
            # VectorStore'u başlat.
            user_vector_store = VectorStore(user_id=user_id)

            # kullanıcının koleksiyonunda arama yap.
            found_doc = user_vector_store.find_document(query)

            return {
                "success": True,
                "document": found_doc
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"'{user_id}' kullanıcısı için arama yapılamadı: {str(e)}"
            }

    async def delete_user_data(self, user_id: str) -> dict:
        """
        Belirtilen kullanıcının tüm veritabanı koleksiyonunu siler.
        """
        try:
            # VectorStore'u başlat.
            user_vector_store = VectorStore(user_id=user_id)

            # kullanıcının koleksiyonunu sil.
            user_vector_store.delete_collection()

            return {
                "success": True,
                "message": f"'{user_id}' kullanıcısının verileri başarıyla silindi."
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"'{user_id}' kullanıcısının verileri silinemedi: {str(e)}"
            }


#------------------------------Main Test blogu------------------------------
if __name__ == "__main__":
    async def main():
        # servisi başlat
        service = VectorDatabaseService()

        # test için bir kullanıcı ID'si ve dokümanlar hazırla
        test_user_id = "user_9876"
        test_docs = [
            Document(page_content="Yapay zeka etiği, algoritmaların adil ve şeffaf olmasını amaçlar.",
                     metadata={"source": "makale_1.pdf"}),
            Document(page_content="Ankara, Türkiye'nin başkenti ve en kalabalık ikinci şehridir.",
                     metadata={"source": "cografya_kitabi.pdf"})
        ]

        # kullanıcı için doküman ekle
        add_result = await service.add_documents_for_user(user_id=test_user_id, documents=test_docs)
        print("Ekleme Sonucu:", add_result)

        # aynı kullanıcı için arama yap
        search_result = await service.search_for_user(user_id=test_user_id, query="Türkiye'nin başkenti neresi?")
        print("\nArama Sonucu:", search_result)

        # kullanıcının verilerini temizle
        delete_result = await service.delete_user_data(user_id=test_user_id)
        print("\nSilme Sonucu:", delete_result)


    asyncio.run(main())