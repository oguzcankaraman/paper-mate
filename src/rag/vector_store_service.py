import asyncio
from typing import List
from langchain_core.documents import Document
from src.rag import VectorStore

class VectorDatabaseService:
    def __init__(self):
        self.vector_store = VectorStore()
        print("VectorDatabaseService başlatıldı.")

    async def add_documents_for_user(self, user_id: str, documents: List[Document]) -> dict:
        try:
            # add_user_documents metodunu çağırma
            self.vector_store.add_user_documents(user_id=user_id, documents=documents)
            return {
                "success": True,
                "message": f"'{user_id}' kullanıcısı için {len(documents)} doküman eklendi."
            }
        except Exception as e:
            return {"success": False, "error": f"'{user_id}' kullanıcısı için doküman eklenemedi: {str(e)}"}

    async def search_for_user(self, user_id: str, query: str) -> dict:
        try:
            # arama metodunu user_id ile çağırma
            found_doc = self.vector_store.find_document(user_id=user_id, query=query)
            return {"success": True, "document": found_doc}
        except Exception as e:
            return {"success": False, "error": f"'{user_id}' kullanıcısı için arama yapılamadı: {str(e)}"}

    async def delete_user_data(self, user_id: str) -> dict:
        try:
            # silme metodunu user_id ile çağırma
            self.vector_store.delete_user_documents(user_id=user_id)
            return {"success": True, "message": f"'{user_id}' kullanıcısının verileri silindi."}
        except Exception as e:
            return {"success": False, "error": f"'{user_id}' kullanıcısının verileri silinemedi: {str(e)}"}

#---------------------------Main Test Blogu----------------------------
if __name__ == "__main__":
    async def main():
        service = VectorDatabaseService()
        test_user_id = "user_9876"
        test_docs = [
            Document(page_content="Yapay zeka etiği, algoritmaların adil ve şeffaf olmasını amaçlar.", metadata={"source": "makale_1.pdf"}),
            Document(page_content="Ankara, Türkiye'nin başkenti ve en kalabalık ikinci şehridir.", metadata={"source": "cografya_kitabi.pdf"})
        ]
        add_result = await service.add_documents_for_user(user_id=test_user_id, documents=test_docs)
        print("Ekleme Sonucu:", add_result)
        search_result = await service.search_for_user(user_id=test_user_id, query="Türkiye'nin başkenti neresi?")
        print("\nArama Sonucu:", search_result)
        delete_result = await service.delete_user_data(user_id=test_user_id)
        print("\nSilme Sonucu:", delete_result)

    asyncio.run(main())