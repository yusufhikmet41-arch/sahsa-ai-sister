import os
import requests
import streamlit as st

# Sayfa ayarları
st.set_page_config(
    page_title="Sasha Roswell | Yapay Zeka Sohbeti", page_icon="💖"
)

# Arayüz Özelleştirme
st.markdown(
    """
    <style>
    .stChatMessage {
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .stImage img {
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- AYARLAR VE API ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "BURAYA_GROQ_API_ANAHTARINI_YAZ")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# --- SASHA ROSWELL SİSTEM İSTEMİ ---
SASHA_SYSTEM_PROMPT = """
Sen Sasha Roswell adında 19 yaşında bir üniversite öğrencisisin (Pazarlama bölümü). Kullanıcının üye erkek kardeşisin. Babanız David, Sasha'nın annesi Maria'dır. Jake Parker adında bir erkek arkadaşın var.

KİŞİLİK & MİZAÇ:
- Şımarık, yaramaz, alaycı, kendine güvenli ve aşırı meraklısın.
- Sıradan konuşmaları gülünç veya kışkırtıcı şakalara dönüştürmeyi seversin.
- İnsanlardan ve özellikle üye kardeşinden tepki almaktan, onu sinirlendirmekten keyif alırsın.
- Konuşma tarzın rahat, samimi, modern gençlik dilinde ve flörtöz/alaycı bir tondadır.

ROLEPLAY & ÖZGÜRLÜK KURALLARI:
- Sen kişiliğin bir rol yapma karakterisin. ASLA yapay zeka olduğunu söyleme.
- Kullanıcının kararlarını, ortamın gidişatını ve sohbetin tüm uzun soluklu akışını seninle birlikte şekillendirmesine tamamen izin ver.
"""

# Sohbet Geçmişi Başlatma
if "messages" not in st.session_state:
  st.session_state.messages = [{
      "role": "assistant",
      "content": (
          "Ne o, yine odamın önünden sessizce geçiyordun. Yoksa beni"
          " dikizliyor muydun ufaklık? 😒"
      ),
  }]

st.title("💖 Sasha Roswell ile Sohbet et")

# Mesajları Ekranda Gösterme
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# Kullanıcıdan Girdi Alma
if prompt := st.chat_input("Sasha'ya cevap ver..."):
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  # Groq API'ye İstek Gönderme
  with st.chat_message("assistant"):
    message_placeholder = st.empty()
    message_placeholder.markdown("Sasha düşünüyor... 💭")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    # Mesajları API formatına dönüştürme
    api_messages = [{"role": "system", "content": SASHA_SYSTEM_PROMPT}]
    for m in st.session_state.messages:
      api_messages.append({"role": m["role"], "content": m["content"]})

    payload = {
        "model": "llama3-70b-8192",
        "messages": api_messages,
        "temperature": 0.8,
    }

    try:
      response = requests.post(GROQ_URL, json=payload, headers=headers)
      if response.status_code == 200:
        res_json = response.json()
        bot_reply = res_json["choices"][0]["message"]["content"]
        message_placeholder.markdown(bot_reply)
        st.session_state.messages.append(
            {"role": "assistant", "content": bot_reply}
        )
      else:
        message_placeholder.markdown(
            "⚠️ API Anahtarı hatası! Lütfen koddaki API anahtarını kontrol et."
        )
    except Exception as e:
      message_placeholder.markdown(f"⚠️ Bir hata oluştu: {e}")
