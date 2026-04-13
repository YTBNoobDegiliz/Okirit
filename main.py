import streamlit as st
import requests
import base64

# --- API AYARI (Değiştirme) ---
# Kendi Base64 anahtarını buraya yapıştır knk
HIDDEN_KEY = "QUl6YVN5QWFSdC15TnE5T2I2Ty1pU01YNnlWQ1JYaFhjVXloTGhJ" 

def get_key():
    return base64.b64decode(HIDDEN_KEY).decode("utf-8")

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Okirit AI", page_icon="🤖", layout="centered")

# --- TAMAMEN ÖZEL CSS (Arayüz Burası) ---
st.markdown("""
    <style>
    /* Arka Plan ve Genel Font */
    .stApp {
        background-color: #121212;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Üst Başlık */
    .okirit-header {
        text-align: center;
        color: #00E676;
        text-shadow: 0 0 15px #00E676;
        font-size: 2.5rem;
        font-weight: bold;
        letter-spacing: 2px;
        margin-bottom: 20px;
    }

    /* Mesaj Konteyneri */
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 15px;
        padding: 10px;
        margin-bottom: 80px; /* Giriş alanı için boşluk */
    }

    /* Kullanıcı Mesaj Baloncuğu */
    .user-bubble {
        align-self: flex-end;
        background: linear-gradient(135deg, #007AFF, #00C6FF);
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 0px 18px;
        max-width: 80%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        font-size: 0.95rem;
    }

    /* Okirit Mesaj Baloncuğu */
    .ai-bubble {
        align-self: flex-start;
        background-color: #1D2733;
        color: #E0E0E0;
        padding: 15px 20px;
        border-radius: 18px 18px 18px 0px;
        max-width: 85%;
        border: 1px solid #2B394A;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        font-size: 0.95rem;
    }
    
    .ai-name {
        color: #00E676;
        font-weight: bold;
        font-size: 0.8rem;
        margin-bottom: 5px;
        letter-spacing: 1px;
    }

    /* Markdown Kod Blokları İyileştirmesi */
    .stMarkdown pre {
        background-color: #0F111A !important;
        border: 1px solid #2B394A !important;
        border-radius: 8px !important;
    }
    .stMarkdown code {
        color: #FF80AB !important; /* Kod rengi */
    }

    /* Giriş Alanı Sabitleme ve Tasarımı */
    .stChatInputContainer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #121212;
        padding: 15px;
        border-top: 1px solid #2B394A;
        z-index: 100;
    }
    .stChatInputContainer input {
        border-radius: 25px !important;
        background-color: #1D2733 !important;
        border: 1px solid #2B394A !important;
        color: white !important;
        padding: 12px 20px !important;
    }
    .stChatInputContainer input:focus {
        border-color: #00E676 !important;
        box-shadow: 0 0 5px #00E676 !important;
    }
    
    /* Streamlit varsayılan elemanlarını gizle */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    </style>
    """, unsafe_allow_html=True)

# Başlığı Bas
st.markdown("<div class='okirit-header'>OKİRİT AI</div>", unsafe_allow_html=True)

# Mesaj Geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları Özel HTML ile Görüntüle
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"<div class='user-bubble'>{message['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class='ai-bubble'>
                <div class='ai-name'>OKİRİT</div>
                <div>{message['content']}</div>
            </div>
        """, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Giriş Alanı
if prompt := st.chat_input("Okirit'e bir şeyler yaz..."):
    # Kullanıcı mesajını ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Sayfayı yenile (mesajı hemen göstermek için)
    st.rerun()

# Eğer son mesaj kullanıcıdaysa, API'den cevap al
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    user_prompt = st.session_state.messages[-1]["content"]
    
    with st.spinner("Okirit cevaplıyor..."):
        API_KEY = get_key()
        API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        
        payload = {
            "contents": [{"parts": [{"text": f"Senin adın Okirit. Uzman bir yazılımcısın. Yanıtlarını profesyonelce hazırla. Kodları markdown blokları içinde ver: {user_prompt}"}]}]
        }
        
        try:
            res = requests.post(API_URL, json=payload)
            response_text = res.json()['candidates'][0]['content']['parts'][0]['text']
            # Cevabı ekle
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            # Sayfayı yenile (cevabı göstermek için)
            st.rerun()
        except:
            st.error("API Hatası! Base64 anahtarını doğru girdiğinden emin ol knk.")