import streamlit as st
from streamlit_option_menu import option_menu
import google.generativeai as genai
import urllib.parse
import PyPDF2

# --- 1. AYARLAR VE ANAHTAR ---
GOOGLE_API_KEY = "AIzaSyDLamkBZzN4xHaKTdBos3iyDEpENU9ZXFg"

# --- 2. SİSTEM VE HAFIZA BAŞLATMA ---
if "messages" not in st.session_state:
    st.session_state.messages = [] # Sohbet geçmişi burada saklanır
if "file_text" not in st.session_state:
    st.session_state.file_text = ""

try:
    genai.configure(api_key = "AIzaSyDLamkBZzN4xHaKTdBos3iyDEpENU9ZXFg")
    # Gemini 2.5 Flash ve Türkçe Sistem Talimatı
    model = genai.GenerativeModel(
        model_name='gemini-2.5-flash',
        system_instruction="Sen Okirit 3.0'sın. Uzman asistan ve yazılımcısın. Her zaman samimi, Türkçe konuş ve kanka diye hitap et."
    )
except Exception as e:
    st.error(f"Bağlantı Hatası kanka: {e}")

# Görsel Motoru (Bedava & Sınırsız)
def get_image_url(prompt):
    return f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=1024&height=1024&nologo=true"

# --- 3. ARAYÜZ TASARIMI ---
st.set_page_config(page_title="Okirit 3.0 Live", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: white; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #333; }
    .stTextInput>div>div>input { background-color: #1f2328; color: #00ffcc; border-radius: 10px; }
    .live-card { background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%); padding: 20px; border-radius: 15px; text-align: center; color: black; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. YAN PANEL ---
with st.sidebar:
    st.title("⚡ OKİRİT 3.0 PRO")
    st.write(f"🟢 **Model:** Gemini 2.5 Flash")
    st.divider()
    if st.button("🗑️ Sohbeti Sıfırla", use_container_width=True):
        st.session_state.messages = []
        st.session_state.file_text = ""
        st.rerun()
    st.divider()
    st.caption("2026 Kararlı Sürüm")

# --- 5. ANA MENÜ ---
secilen = option_menu(None, ["Sohbet", "Live (Sesli)", "Görsel Üret", "Dosya Analizi"], 
    icons=["chat-dots", "mic", "brush", "file-pdf"], orientation="horizontal")

# --- 6. MODLAR ---

# --- SOHBET MODU (KAYIT ÖZELLİKLİ) ---
if secilen == "Sohbet":
    st.subheader("💬 Okirit Sohbet (Hafıza Aktif)")
    # Mesaj geçmişini bas
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Yaz kanka, her şeyi hatırlıyorum..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                # Geçmişi de modele gönderiyoruz ki hatırlasın
                res = model.generate_content(prompt)
                st.markdown(res.text)
                st.session_state.messages.append({"role": "assistant", "content": res.text})
            except Exception as e:
                st.error(f"Hata kanka: {e}")

# --- LIVE MODU (SİMÜLASYON) ---
elif secilen == "Live (Sesli)":
    st.markdown('<div class="live-card">🎙️ OKİRİT LIVE MODU AKTİF</div>', unsafe_allow_html=True)
    st.info("Kanka, Gemini Live özelliğini tarayıcıda simüle ediyorum. Konuşmak için metin kutusunu kullan, ben sana sesli cevap verecekmişim gibi düşün!")
    
    live_input = st.text_input("Şu an seni dinliyorum kanka, ne diyeceksin?")
    if live_input:
        with st.spinner("Okirit düşünüyor..."):
            res = model.generate_content(f"Kısa ve canlı bir cevap ver: {live_input}")
            st.success(f"Okirit Diyor ki: {res.text}")
            # Tarayıcının konuşma özelliğini tetikleyen basit bir HTML
            st.components.v1.html(f"""
                <script>
                var msg = new SpeechSynthesisUtterance('{res.text.replace("'", "")}');
                msg.lang = 'tr-TR';
                window.speechSynthesis.speak(msg);
                </script>
            """, height=0)

# --- GÖRSEL ÜRET MODU ---
elif secilen == "Görsel Üret":
    st.subheader("🎨 Görsel Stüdyosu")
    g_input = st.text_input("Ne hayal ediyorsun?")
    if st.button("Çiz"):
        if g_input:
            url = get_image_url(g_input)
            st.image(url, use_container_width=True)
            st.markdown(f"[📥 İndir]({url})")

# --- DOSYA ANALİZİ ---
elif secilen == "Dosya Analizi":
    st.subheader("📂 PDF Analizi")
    f = st.file_uploader("Dosya at", type=["pdf"])
    if f:
        reader = PyPDF2.PdfReader(f)
        st.session_state.file_text = "".join([p.extract_text() for p in reader.pages])
        st.success("Okudum kanka!")
        soru = st.text_input("Dosya hakkında sor:")
        if st.button("Analiz Et"):
            res = model.generate_content(f"Dosya: {st.session_state.file_text[:8000]}\nSoru: {soru}")
            st.write(res.text)