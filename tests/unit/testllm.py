'''
LLM Özetleme Unit Testleri
---------------------------

Bu testler LLM özetleme fonksiyonunun mock_llm ile sabit ve deterministik çıktı ürettiğini kontrol eder.


'''

from src.llm.summarize import summarize 

#Özetleme fonksiyonu çalışıyor mu?
def test_ozetleme(mock_llm):
    uzun_metin = "Transformer mimarisi üzerine kısa bir açıklama"
    sonuc = summarize(uzun_metin)
    assert isinstance(sonuc, str)
    assert "Özet:" in sonuc, "Mock LLM beklenen formatta yanıt üretemedi."

