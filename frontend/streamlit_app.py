import sys
import os
import asyncio
import streamlit as st
import requests  # Giriş ve kayıt istekleri için gerekli


#  Çalıştırmak için :
# streamlit run frontend/streamlit_app.py

# Proje kökünü (paper-mate klasörünü) sys.path'e ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.api.services import (
    OllamaClientService,
    PdfParserService,
    RagService,
    VectorDatabaseService,
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

menu = st.sidebar.selectbox("Menü", ["🔑 Giriş / Kayıt", "📄 PDF Özetleme", "ℹ️ Bilgi Sayfası"])

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
                LOGIN_URL = "http://localhost:8000/auth/login"
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
                REGISTER_URL = "http://localhost:8000/auth/register"
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
if menu == "📄 PDF Özetleme":
    st.header("PDF Dosyasını Yükle ve Özetle")

    if not st.session_state["logged_in"]:
        st.warning("🚫 Lütfen önce giriş yapın.")
        st.stop()

    uploaded_file = st.file_uploader("Bir makale (PDF veya DOCX) yükleyin:", type=["pdf", "docx"])

    summary = None
    if uploaded_file:
        st.info(f"Yüklendi: {uploaded_file.name}")

        from pathlib import Path

        tmp_dir = Path("frontend/tmp_uploads")
        tmp_dir.mkdir(parents=True, exist_ok=True)
        tmp_path = tmp_dir / uploaded_file.name

        with open(tmp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        if st.button("Özetle"):
            headers = {"Authorization": f"Bearer {st.session_state['token']}"} if st.session_state["token"] else {}
            pdf_parser = PdfParserService()
            try:
                result = asyncio.run(pdf_parser.api_process_and_chunk_pdf(tmp_path))
                chunks = result.get("chunks", [])
            except Exception as e:
                st.error(f"PDF işlenirken hata: {e}")
                st.stop()
            vector_database = VectorDatabaseService()
            _ = asyncio.run(vector_database.add_documents_for_user("1", chunks))
            ollama_client = OllamaClientService()
            summary = asyncio.run(ollama_client.api_summarizer(chunks))

        st.subheader("📘 Makale Özeti")
        st.write(summary)

        st.markdown("---")
        st.subheader("Makale Hakkında Soru Sor")
        user_question = st.text_input("Sorunuzu yazın:")

        if st.button("Soruyu Gönder"):
            if not user_question.strip():
                st.warning("Lütfen bir soru girin.")
            else:
                from src.api.database.crud import create_user, get_user_by_email
                from src.rag import RAG
                rag = RAG()
                test_email = "test@example.com"
                user = get_user_by_email(rag.db, test_email)
                if not user:
                    user = create_user(rag.db, "Test User", test_email, "test123")
                rag = RagService()
                result = asyncio.run(rag.make_conversation(user_question.strip(), 1))
                print(result)
                st.write(result)

# ===================================================================
# Bilgi SAYFASI
# ===================================================================
else:
    st.header("Sistem Bilgisi ve Durum")
    st.markdown(
        """
        **Bu arayüz neler yapar:**
        - Kullanıcı girişi ve kayıt işlemleri (AI, kullanıcıların soru ve isteklerini hatırlayacaktır.)
        - PDF yükleyerek AI destekli kolay ve hızlı özet alma
        - Makale özeti sonrası açılan sohbet penceresi ile soru-cevap ve konuyla alakalı diğer kaynaklara erişim imkanı
        """
    )
    st.divider()
    st.write("Kullanıcı:", st.session_state.get("email", "—"))
