import streamlit as st
import requests

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Okirit AI", page_icon="🤖")

# --- BURAYA GERÇEK API ANAHTARINI YAPIŞTIR ---
API_KEY = "AIzaSyCjcWd8Eebs34JyC7gg_yqHRAHetjz2DDw" 

# --- ŞIK TASARIM (Bok Gibi Durmayan Versiyon) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0F111A; }}
    .okirit-header {{ text-align: center; color: #00E676; text-shadow: 0 0 10px #00E676; font-size: 2.2rem; font-weight: bold; margin-top: -50px; margin-bottom: 20px; }}
    .user-msg {{ background: #007AFF; color: white; padding: 12px; border-radius: 15px 15px 0 15px; margin: 10px 0; width: fit-content; max-width: 80%; float: right; clear: both; box-shadow: 2px 2px 5px rgba(0,0,0,0.3); }}
    .ai-msg {{ background: #1D2733; color: #E0E0E0; padding: 15px; border-radius: 15px 15px 15px 0; margin: 10px 0; width: fit-content; max-width: 85%; float: left; clear: both; border: 1px solid #2B394A; }}
    .ai-name {{ color: #00E676; font-size: 0.8rem; font-weight: bold; margin-bottom: 5px; }}
    #MainMenu, footer, header {{visibility: hidden;}}
    .stChatInputContainer {{ border-radius: 30px !important; }}
    </style>
    <div class="okirit-header">OKİRİT AI</div>
    """, unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Mesajları Ekrana Bas
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f'<div class="user-msg">{chat["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-msg"><div class="ai-name">OKİRİT</div>{chat["content"]}</div>', unsafe_allow_html=True)

# Giriş Alanı
if prompt := st.chat_input("Okirit'e bir şeyler yaz..."):
    # Senin mesajını ekle
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    # API İsteği
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    payload = {{"contents": [{"parts": [{"text": f"Senin adın Okirit. Uzman bir yazılımcısın: {{prompt}}"}]}]}}
    
    try:
        response = requests.post(url, json=payload)
        bot_response = response.json()['candidates'][0]['content']['parts'][0]['text']
        st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
    except:
        st.session_state.chat_history.append({"role": "assistant", "content": "Hata oluştu knk, anahtarın doğru mu?"})
    
    st.rerun()