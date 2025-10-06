# 📚 PaperMate - AI-Powered Academic Paper Analyzer

> Öğrenciler ve araştırmacılar için akademik makaleleri analiz eden, özetleyen ve soru-cevap yapılabilen yapay zeka asistanı.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-in%20development-yellow.svg)

## ✨ Özellikler

- 📄 PDF yükleme ve otomatik metin çıkarma
- 🤖 LLM ile akıllı özet oluşturma
- 💬 Makaleye soru sorma (RAG tabanlı)
- 🔑 Anahtar kelime ve kavram çıkarma
- 📊 Citation analizi
- 🔍 Benzer makale önerisi

## 🚀 Hızlı Başlangıç

### Gereksinimler
- Python 3.10+
- Ollama (LLM için)
- Git

### Kurulum
```bash
# Repository'i klonla
git clone https://github.com/oguzcankaraman/paper-mate.git
cd paper-mate

# Virtual environment oluştur
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# Ollama'yı kur ve modeli indir
curl https://ollama.ai/install.sh | sh
ollama pull llama3.1:8b

# .env dosyası oluştur
cp .env.example .env
```

### Çalıştırma
```bash
# Frontend'i başlat
streamlit run frontend/app.py
```

### Proje Yapısı
```
papermate/
├── src/
│   ├── pdf_processing/    # PDF okuma ve işleme
│   ├── llm/              # LLM entegrasyonu
│   ├── rag/              # RAG sistemi
│   └── utils/            # Yardımcı fonksiyonlar
├── frontend/             # Streamlit UI
├── tests/                # Test dosyaları
├── docs/                 # Dokümantasyon
└── scripts/              # Yardımcı scriptler
```
### Ekip
- **Team 1:** PDF Processing
- **Team 2:** LLM Integration
- **Team 3:** RAG System
- **Team 4:** Frontend
- **Team 5:** Testing & QA

### Katkıda Bulunma
`CONTRIBUTING.md` dosyasına bakın

### 📝 Lisans
- MIT License - detaylar için LICENSE dosyasına bakın.
### 📮 İletişim
- Sorularınız için issue açabilir veya Discord sunucumuza katılabilirsiniz
# 
⭐ Projeyi beğendiyseniz yıldız vermeyi unutmayın!
