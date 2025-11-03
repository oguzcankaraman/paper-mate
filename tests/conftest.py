# tests/conftest.py
import sys
from pathlib import Path
import shutil
import tempfile
import pytest

# --- src-layout: tests => src yolunu PYTHONPATH'e ekle ---
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


# ----------------- Ortak yardımcı fixture'lar -----------------

@pytest.fixture
def tmpdir_clean():
    """Her test için izole geçici klasör."""
    d = Path(tempfile.mkdtemp(prefix="pmate_"))
    try:
        yield d
    finally:
        shutil.rmtree(d, ignore_errors=True)


@pytest.fixture
def sample_texts():
    return [
        "Paper-Mate speeds up reading.",
        "Embedding search should return relevant chunks.",
        "PDF parsing must preserve text order.",
    ]


@pytest.fixture
def fake_env(monkeypatch):
    """LLM/API testlerinde gerçek anahtar gerektirmesin."""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-123")
    monkeypatch.setenv("ENV", "test")


class _FakeLLM:
    def __init__(self, static="OK"):
        self.static = static

    def complete(self, prompt: str, **kw) -> str:
        # Deterministik çıktı
        return f"[FAKE-LLM] {self.static} :: {prompt[:40]}"


@pytest.fixture
def fake_llm():
    return _FakeLLM(static="DONE")


# ----------------- PDF üretim ve yollar -----------------

@pytest.fixture
def write_pdf(tmpdir_clean):
    """
    Basit PDF oluşturucu.
    reportlab yoksa otomatik .txt dosyasına düşer; testin toleranslı karşılaştırma yapması önerilir.
    """
    try:
        from reportlab.pdfgen import canvas  # type: ignore

        def _make_pdf(text: str, name: str = "sample.pdf") -> Path:
            p = tmpdir_clean / name
            c = canvas.Canvas(str(p))
            y = 800
            for line in (text.splitlines() or [""]):
                c.drawString(40, y, line)
                y -= 14
            c.save()
            return p

        return _make_pdf
    except Exception:
        # Geri dönüş: düz metin (extract_text testin bunu da okuyabiliyorsa)
        def _make_txt(text: str, name: str = "sample.txt") -> Path:
            p = tmpdir_clean / name
            p.write_text(text, encoding="utf-8")
            return p

        return _make_txt


@pytest.fixture
def sample_pdf_path(write_pdf) -> Path:
    """Okunabilir içerikli örnek PDF yolu döndürür."""
    content = "Hello PDF\nLine 2\nTürkçe: ğüşiöç ĞÜŞİÖÇ"
    return write_pdf(content, name="ok.pdf")


@pytest.fixture
def corrupted_pdf_path(tmpdir_clean) -> Path:
    """Bozuk PDF dosyası yolu döndürür."""
    p = tmpdir_clean / "broken.pdf"
    p.write_bytes(b"%PDF-1.4\n%\x80\x81\x82\xff\nTHIS_IS_NOT_VALID_CONTENT")
    return p


# ----------------- Embedding mock -----------------

@pytest.fixture
def mock_embedder():
    """
    Deterministik 3D embedding:
      [ transformer_sayısı, attention_sayısı, kelime_sayısı ]
    """
    def _embed(texts):
        if not isinstance(texts, (list, tuple)):
            texts = [texts]
        vecs = []
        for t in texts:
            s = (t or "").lower()
            vecs.append([
                float(s.count("transformer")),
                float(s.count("self-attention") + s.count("attention")),
                float(len(s.split())),
            ])
        return vecs
    return _embed
