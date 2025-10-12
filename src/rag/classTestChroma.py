import chromadb
from typing import Optional
from langchain_core.documents import Document


class classTestChroma:

    def __init__(self):

        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(name='test_collection')
        self._initialize_data()

    def _initialize_data(self):

        if self.collection.count() == 0:
            print("Koleksiyon boş, başlangıç verileri ekleniyor...")
            documents_to_add = [
                Document(page_content="Ben 21 yaşındayım.", metadata={"source": "mammal-pets-doc"}),
                Document(page_content="Yapay zeka çok ilginç.", metadata={"source": "mammal-pets-doc"}),
                Document(page_content="Ankara'da yaşıyorum.", metadata={"source": "mammal-pets-doc"}),
            ]
            contents = [doc.page_content for doc in documents_to_add]
            metadatas = [doc.metadata for doc in documents_to_add]
            ids = [f"id{i + 1}" for i in range(len(documents_to_add))]
            self.collection.add(documents=contents, metadatas=metadatas, ids=ids)

        print(f"Koleksiyonda toplam {self.collection.count()} adet doküman var.")

    def find_document(self, query: str) -> Optional[Document]:

        results = self.collection.query(
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



if __name__ == "__main__":
    #chroma instance
    classTestChroma_instance = classTestChroma()
    #test ifadesi
    search_query = "Yapay zeka uygulamaları"
    found_doc = classTestChroma_instance.find_document(search_query)

    print(f"\n'{search_query}' araması için bulunan sonuç:")
    if found_doc:
        print("Bulunan Döküman Tipi:", type(found_doc))
        print("Döküman İçeriği:", found_doc.page_content)
        print("Döküman Metadatası:", found_doc.metadata)
    else:
        print("İlgili doküman bulunamadı.")