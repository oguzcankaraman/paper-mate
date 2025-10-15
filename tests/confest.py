"""
Paper-Mate test altyapısı için ortak ayarlar e fixture'lar
pytest otamatik ayarlar import edilmeye gerek kalmaz

"""

import os
import random
import numpy as np
import pytest

# DETERMİNİSTİk ------> Sonuçlar sabitlenir.
  
@pytest.fixture(autouse=True, scope="session")
def make_deterministic():
    os.environ["PYTHONHASHSEED"] = "0"
    random.seed(0)
    np.random.seed(0)


# Örnek PDF dosyası ---------> Örnek pdf dosya yolu döner.

@pytest.fixture
def sample_pdf_path():
    return os.path.join("tests", "data", "sample_short.pdf")


# Bozuk PDF Testi -------> Bozuk PDF dosya yolu döner.

@pytest.fixture
def corrupted_pdf_path():
    return os.path.join("tests", "data", "corrupted.pdf")


# Mock embedding ---------> Embedding fonksiyonunu sahte hale getirir.

@pytest.fixture
def mock_embedder(monkeypatch):
    def fake_embed(texts):
        return [[len(t) % 5, len(t) % 7, 1.0] for t in texts]
    monkeypatch.setattr("src.rag.embeddings.embed_texts", fake_embed)
    return fake_embed