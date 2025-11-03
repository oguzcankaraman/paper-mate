import sys
import os
import asyncio
from typing import List
from pathlib import Path

import streamlit as st
import requests
import fitz  # ✅ PDF metin çıkarımı için eklendi (PyMuPDF)

# === Ortam hazırlığı ===
ROOT = Path(__file__).resolve().parent
SRC = ROOT / "paper-mate-main" / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

# === Backend endpoint adresleri ===
API_BASE = "http://localhost:8000"
REGISTER_URL = f"{API_BASE}/auth/register"
LOGIN_URL = f"{API_BASE}/auth/login"
UPLOAD_URL = f"{API_BASE}/files/upload"
CHAT_URL = f"{API_BASE}/chat"

# === Backend bağımlılıklarını kontrol et ===
use_backend_methods = False
try:
    from src.pdf_processing.pdf_parser import PdfProcessor
    from src.ollama.ollamaClass import OllamaClient
    use_backend_methods = True
except Exception as e:
    st.warning(
        f"⚠️ Backend modülleri yüklenemedi: {e}\n"
        "OllamaClient veya PdfProcessor sınıfı bulunamazsa özetleme özelliği sınırlı çalışır."
    )

# === Session state ===
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "token" not in st.session_state:
    st.session_state["token"] = None
if "email" not in st.session_state:
    st.session_state["email"] = None

# Geliştirme aşaması için login'i atla
st.session_state["logged_in"] = True
st.session_state["token"] = "dummy_token"
st.session_state["email"] = "test@user.com"

# === Başlık ===
st.title("📘 Akademik Makale Analiz Aracı")
st.caption("Yapay zeka destekli makale özetleme aracı")

menu = st.sidebar.selectbox("Menü", ["🔑 Giriş / Kayıt", "📄 PDF Özetleme", "🥚 Easter Egg"])

# ===================================================================
# 🔑 GİRİŞ / KAYIT SAYFASI
# ===================================================================
if menu == "🔑 Giriş / Kayıt":
    st.header("Kullanıcı Girişi veya Kayıt Ol")

    tab1, tab2 = st.tabs(["Giriş", "Kayıt Ol"])

    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Şifre", type="password", key="login_password")

        if st.button("Giriş Yap"):
            try:
                res = requests.post(LOGIN_URL, json={"email": email, "password": password})
                if res.status_code == 200:
                    st.session_state["logged_in"] = True
                    st.session_state["token"] = res.json().get("token", None)
                    st.session_state["email"] = email
                    st.success("✅ Giriş başarılı!")
                elif res.status_code == 404:
                    st.error("⚠️ /auth/login endpointi bulunamadı. Backend henüz tamamlanmamış olabilir.")
                else:
                    st.error(f"Giriş başarısız: {res.text}")
            except requests.exceptions.ConnectionError:
                st.warning("⚠️ Backend bağlantısı başarısız (localhost:8000 erişilemiyor).")
            except Exception as e:
                st.error(f"Hata: {e}")

    with tab2:
        reg_email = st.text_input("Yeni Email", key="reg_email")
        reg_password = st.text_input("Yeni Şifre", type="password", key="reg_password")

        if st.button("Kayıt Ol"):
            try:
                res = requests.post(REGISTER_URL, json={"email": reg_email, "password": reg_password})
                if res.status_code in [200, 201]:
                    st.success("✅ Kayıt başarılı! Giriş yapabilirsiniz.")
                elif res.status_code == 404:
                    st.warning("⚠️ /auth/register endpointi backend'de yok. Henüz eklenmemiş olabilir.")
                else:
                    st.error(f"Kayıt başarısız: {res.text}")
            except requests.exceptions.ConnectionError:
                st.warning("⚠️ Backend bağlantısı başarısız (localhost:8000 erişilemiyor).")
            except Exception as e:
                st.error(f"Hata: {e}")

# ===================================================================
# 📄 PDF ÖZETLEME SAYFASI
# ===================================================================
elif menu == "📄 PDF Özetleme":
    st.header("PDF Dosyasını Yükle ve Özetle")

    if not st.session_state["logged_in"]:
        st.warning("🚫 Lütfen önce giriş yapın.")
        st.stop()

    uploaded_file = st.file_uploader("Bir makale (PDF veya DOCX) yükleyin:", type=["pdf", "docx"])

    summary = None
    if uploaded_file:
        st.info(f"Yüklendi: {uploaded_file.name}")

        tmp_dir = ROOT / "tmp_uploads"
        tmp_dir.mkdir(exist_ok=True)
        tmp_path = tmp_dir / uploaded_file.name
        with open(tmp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        if st.button("Özetle"):
            headers = {"Authorization": f"Bearer {st.session_state['token']}"} if st.session_state["token"] else {}
            try:
                with open(tmp_path, "rb") as f:
                    res = requests.post(UPLOAD_URL, files={"file": f}, headers=headers)
                if res.status_code == 200:
                    data = res.json()
                    summary = data.get("summary") or data.get("summary_text")
                    if not summary:
                        st.warning("⚠️ Backend yanıtında 'summary' alanı bulunamadı.")
                elif res.status_code == 404:
                    st.warning("⚠️ /files/upload endpointi backend’de tanımlı değil.")
                else:
                    st.error(f"Backend yanıtı: {res.status_code} - {res.text}")
            except requests.exceptions.ConnectionError:
                st.warning("⚠️ Backend çalışmıyor. Yerel özetleme ile devam edilecek.")
            except Exception as e:
                st.error(f"Hata: {e}")

        # === Fallback Özetleme ===
        def extract_text_from_pdf(pdf_path):
            """PDF'den okunabilir metin çıkarır"""
            text = ""
            try:
                with fitz.open(pdf_path) as doc:
                    for page in doc:
                        text += page.get_text()
            except Exception:
                pass
            return text.strip()

        if not summary:
            if use_backend_methods:
                try:
                    st.info("Backend özetleme kullanılmaya çalışılıyor (OllamaClient)...")
                    pdf_proc = PdfProcessor()
                    docs = pdf_proc.load_pdf(str(tmp_path))
                    client = OllamaClient()
                    result_msg = asyncio.run(client.summarizer(docs, "kısa ve öz"))
                    summary = getattr(result_msg, "content", str(result_msg))
                except Exception as e:
                    st.warning(f"OllamaClient çalışmadı ({e}). Basit özetleme devreye girdi.")
                    text = extract_text_from_pdf(tmp_path)
                    summary = " ".join(text.split()[:200]) + "..."
            else:
                st.warning("⚠️ Ne backend, ne OllamaClient kullanılabiliyor. Basit fallback aktif.")
                if uploaded_file.name.lower().endswith(".pdf"):
                    text = extract_text_from_pdf(tmp_path)
                else:
                    try:
                        text = Path(tmp_path).read_text(errors="ignore")
                    except Exception:
                        text = ""
                summary = " ".join(text.split()[:150]) + "..."

        st.subheader("📘 Makale Özeti")
        st.write(summary)

        st.markdown("---")
        st.subheader("Makale Hakkında Soru Sor")
        user_question = st.text_input("Sorunuzu yazın:")

        if st.button("Soruyu Gönder"):
            if not user_question.strip():
                st.warning("Lütfen bir soru girin.")
            else:
                try:

                    payload = {"summary": summary, "question": user_question}
                    res = requests.post(CHAT_URL, json=payload)
                    if res.status_code == 200:
                        answer = res.json().get("answer", "Yanıt alınamadı.")
                        if answer.strip().startswith("%PDF"):
                            st.warning("⚠️ PDF içeriği metne dönüştürülmeden döndü. Backend içeriği PDF olarak gönderiyor.")
                            answer = "PDF içeriği okunamadı, lütfen backend'in metin dönüşümünü kontrol edin."
                        st.success(answer)
                    elif res.status_code == 404:
                        st.warning("⚠️ /chat endpointi backend'de tanımlı değil.")
                    else:
                        st.error(f"Backend yanıtı: {res.status_code}")
                except requests.exceptions.ConnectionError:
                    st.warning("⚠️ Backend çalışmıyor, yerel yanıt üretiliyor.")
                    st.write(f"🧠 Tahmini yanıt: Makale özetine göre — {summary[:100]}...")

# ===================================================================
# Easter Egg SAYFASI
# ===================================================================
else:
    st.header("Sistem Bilgisi ve Durum")
    st.markdown(
        """
        **Bu arayüz ne yapar:**
        - Kullanıcı girişi ve kayıt işlemleri (/auth/register, /auth/login)
        - PDF yükleme ve backend üzerinden özet alma (/files/upload)
        - Makale özeti üzerinden sohbet (/chat)

        **Eksik Olanlar (Backend'de tamamlanmalı):**
        - `/auth/register` — kullanıcıyı DB'ye kaydeder  
        - `/auth/login` — kullanıcıyı doğrular ve token döner  
        - `/files/upload` — PDF alır, özet üretir  
        - `/chat` — özet üzerinden soru-cevap sağlar  
        """
    )
    st.divider()
    st.write("Kullanıcı:", st.session_state.get("email", "—"))
    st.write("Backend modülleri yüklü mü:", "✅" if use_backend_methods else "❌")
