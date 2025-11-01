"""
Embedding ve Arama Unit Testleri

Embedding sisteminin ve arama sisteminin doğru çalisip çalişmadiğini test eder.

"""
from src.rag.retriever import TopKRetriever

#Mock embedding fonksiyonu doğru sonuç üretiyor mu?

def test_embedding_boyutu_dogrulama(mock_embedder):
    metinler = ["merhaba", "dünya", "yapay zeka"]
    vektorler = mock_embedder(metinler)
    assert len(vektorler) == len(metinler)
    assert all(len(v) == 3 for v in vektorler), "Vektör uzunluğu 3 olmali"
 

#Retriever alakalı sonuçları döndürüyor mu?

def test_retriever_sonuc(mock_embedder):
    belger[
        ("d1", "Stokastik gradyan inişi kayip fonksiyonlarini optimize eder."),
        ("d2", "Transformer mimarisi self-attention mekanizmasini kullanir."),
        ("d3", "Atif sayilari görünürlükle ilişkilidir."),
    ] 

    retriever = TopKRetriever(k=2)
    retriever.index(
        texts=[d[1] for d in belgeler],
        ids=[d[0] for d in belgeler],
        embed_fn=mock_embedder,
    )

    sonuc = retriever.search("self-attention nedir?")
    assert isinstance(sonuc, list)
    assert len(sonuc) > 0
    en_iyi_idler = [r.get("id") for r in sonuc]
    assert "d2" in en_iyi_idler, "En alakali belge bulunamadi."