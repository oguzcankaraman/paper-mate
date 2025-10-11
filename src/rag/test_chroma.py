import chromadb

#chroma'ya bağlanmak için bir istemci eklendi.
client = chromadb.Client()
#koleksiyon oluşturma kısmı.
collection = client.get_or_create_collection(name = 'test_collection')
#koleksiyona birkaç cümle ekleme
collection.add(
    documents = [
        "Ben 21 yaşındayım.",
        "Yapay zeka çok ilginç",
        "Ankara'da yaşıyorum."
    ],
    ids = ["id1", "id2", "id3"]
)
#search test
results = collection.query(
    #bu aramayı yaptığımız zaman muhtemelen bize "Yapay zeka çok ilgiç" cümlesini getirecek
    query_texts = ["Yapay zeka uygulamaları"],
    n_results = 1
)
print("Arama sonuçları:")
print(results)

