"""
PDF dosyalarından metin çıkarma işlemlerini kontrol eder.
"""

import pytest
from src.pdf_processing.extract import extract_text

#PDF dosyasında metin okunabiliyor mu?

def test_pdf_metni_basariyla_okunuyor(sample_pdf_patch):
    metin = extract_text(sample_pdf_patch)
    assert isinstance(metin, str)
    assert len(metin) > 20, "PDF'ten alınan metin ya boş ya da çok kısa"


#Bozuk PDF testi

def test_bozuk_pdf_hata_veriyor(corrupted_pdf_patch):
    with pytest.raises(Exception):
        _ = extract_text(corrupted_pdf_patch)

