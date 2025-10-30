import chromadb
from typing import  Optional
from langchain_core.documents import Document

class VectorStore:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.client = chromadb.PersistentClient(path="./chroma_db")
        # Her kullanıcı için ayrı collection
        self.collection = self.client.get_or_create_collection(
            name=f'user{user_id}_collection'
        )

    def add_user_documents(self, documents: list[Document]):
        # Kullanıcının yüklediği dökümanları ekle
        contents = [doc.page_content for doc in documents]
        metadatas = [{"user_id": self.user_id, **doc.metadata} for doc in documents]
        ids = [f"user{self.user_id}doc{i}" for i in range(len(documents))]
        self.collection.add(documents=contents, metadatas=metadatas, ids=ids)

    def find_document(self, query: str) -> Optional[Document]:
        # Sadece bu kullanıcının collection'ında arama yapar
        results = self.collection.query(
            query_texts=[query],
            n_results=1,
            include=["metadatas", "documents"]
        )
        if results and results['documents'][0]:
            page_content = results['documents'][0][0]
            metadata = results['metadatas'][0][0]
            return Document(page_content=page_content, metadata=metadata)
        return None

    def delete_collection(self):
        # Mevcut kullanıcının koleksiyonunu veritabanından tamamen siler.
        print(f"'{self.collection.name}' koleksiyonu siliniyor...")
        try:
            self.client.delete_collection(name=self.collection.name)
            print("Koleksiyon başarıyla silindi.")
        except Exception as e:
            print(f"Koleksiyon silinirken bir hata oluştu: {e}")



#--------------------Main Test Blogu----------------------
if __name__ == "__main__":
    # Test için bir kullanıcı ID'si belirleme
    test_user_id = "12345"

    # VectorStore'u bu kullanıcı için başlat
    user_vector_store = VectorStore(user_id=test_user_id)

    # Kullanıcının ekleyeceği sahte dokümanları oluştur
    sample_docs = [
        Document(page_content="Yapay zeka etiği, algoritmaların adil ve şeffaf olmasını amaçlar.",
                 metadata={"source": "makale_1.pdf"}),
        Document(page_content="Ankara, Türkiye'nin başkenti ve en kalabalık ikinci şehridir.",
                 metadata={"source": "cografya_kitabi.pdf"}),
        Document(page_content="Oğuz ve Yağız projeyi bitirdikleri için çok mutlu ve heyecanlılar.")
    ]

    # Bu dokümanları kullanıcının koleksiyonuna ekle
    user_vector_store.add_user_documents(documents=sample_docs)

    # Koleksiyonun güncel durumunu kontrol etme
    print(f"Koleksiyondaki doküman sayısı: {user_vector_store.collection.count()}")

    # Bir arama yaparak `find_document` metodunu test etme kısmı
    search_query = "Başkent neresidir?"
    found_doc = user_vector_store.find_document(search_query)

    print(f"\n'{search_query}' araması için bulunan sonuç:")
    if found_doc:
        print(f"  İçerik: {found_doc.page_content}")
        print(f"  Metadata: {found_doc.metadata}")
    else:
        print("  İlgili doküman bulunamadı.")

    # Test bittikten sonra temizlik için `delete_collection` metodunu çağırma
    user_vector_store.delete_collection()

    # Silme sonrası koleksiyonun durumunu kontrol etme (hata vermesi beklenir)
    try:
        count = user_vector_store.collection.count()
        print(f"Silme sonrası doküman sayısı: {count}")
    except Exception as e:
        print(f"Silme sonrası koleksiyona erişmeye çalışırken beklenen hata: {e}")