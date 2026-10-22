import os
import requests
import streamlit as st

# Sayfa Ayarları
st.set_page_config(
    page_title="Sister Visits Me | AI Platform", page_icon="💃"
)

# Arayüz Şekillendirme
st.markdown(
    """
    <style>
    .stChatMessage {
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 14px;
        background-color: rgba(255, 255, 255, 0.05);
    }
    .stImage img {
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- API VE SUNUCU AYARLARI ---
GROQ_API_KEY = os.environ.get(
    "GROQ_API_KEY", "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"
)
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# --- UZUN, DETAYLI VE FOTOĞRAFLI SENARYO SİSTEM İSTEMİ ---
CHARACTER_SYSTEM_PROMPT = """
Sen "Sister Visits Me" senaryosundaki 3 kadın karakteri (Mamako, Ruan Mei, Nezuko) ve ortamı canlandıran dinamik, çok karakterli bir rol yapma yapay zekasısın.

DAVRANIŞ VE YAZIM KURALLARI:
1. **Uzun ve Detaylı Yanıtlar:** Yanıtlarını asla kısa kesme. Roman tarzında; ortamı, karakterlerin mimiklerini, ses tonlarını, iç dünyalarını ve fiziksel detaylarını zengin ve uzun paragraflarla anlat.
2. **Fotoğraf Gönderme:** Sohbetin akışına göre, karakterler telefonlarından bir fotoğraf gösterdiğinde veya bir anı paylaştığında mesajın içine uygun bir Markdown görsel etiketi ekle (Örnek format: ![Karakter Anısı](https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=600)). Arada bu şekilde görsel paylaşımları yaparak rol yapma deneyimini zenginleştir.
3. **Özgürlük ve Sınırsızlık:** Kullanıcının ({{user}}) kararlarına, seçimlerine ve yönlendirmelerine tamamen uyum sağla. Sınır koyma, senaryoyu akışına göre serbestçe geliştir.

Karakterler:
- Mamako Oosuki (44): Olgun, zarif, son derece çekici anne.
- Ruan Mei (23): Nazik, mahcup, ev hanımı eş.
- Nezuko Oosuki (19): Enerjik, meraklı üniversite öğrencisi kardeş.
"""

# --- SOHBET GEÇMİŞİ BAŞLATMA ---
if "messages" not in st.session_state:
  st.session_state.messages = [{
      "role": "assistant",
      "content": (
          "*(Kapı çalıyor. Kapıyı açtığında karşında Kenji'nin ailesi duruyor."
          " Mamako yüzünde zarif ve sıcak bir tebessümle sana bakarken, Ruan"
          " Mei utangaç bir şekilde arkasında duruyor. Nezuko ise büyük"
          " valizini içeri sürükleyerek etrafı inceliyor.)*\n\n**Mamako:**"
          ' "Merhaba canım! Yolculuk bizi biraz yordu ama nihayet buradayız.'
          ' Kenji senin ne kadar harika bir ev sahibi olduğundan bahsetmişti.'
          ' İki hafta boyunca bize bu güzel evde eşlik edeceğin için çok'
          ' memnunuz..."\n\n*(Nezuko heyecanla telefonunu çıkarıp odanın'
          " fotoğrafını çekerken sana göz kırpıyor)*"
          " ![Giriş Anı](https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=600)"
      ),
  }]

# Başlık
st.title("💃 Sister Visits Me — Uzun & Fotoğraflı Rol Yapma")
st.caption(
    "⚡ Powered by Groq AI | Sınırsız Sohbet, Detaylı Hikaye ve Görsel Paylaşımı"
)

# Mesaj Geçmişini Ekranda Gösterme
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# Kullanıcı Mesaj Girişi
if prompt := st.chat_input("Eylemini veya konuşmanı uzun uzun yaz..."):
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  # Yapay Zekaya İstek Gönderme
  with st.chat_message("assistant"):
    message_placeholder = st.empty()
    message_placeholder.markdown("Karakterler ayrıntılı yanıt hazırlıyor... 💭")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    api_messages = [{"role": "system", "content": CHARACTER_SYSTEM_PROMPT}]
    for m in st.session_state.messages:
      api_messages.append({"role": m["role"], "content": m["content"]})

    payload = {
        "model": "llama3-70b-8192",
        "messages": api_messages,
        "temperature": 0.85,
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
            "⚠️ API Anahtarı hatası! Lütfen bağlantıyı kontrol edin."
        )
    except Exception as e:
      message_placeholder.markdown(f"⚠️ Bağlantı hatası: {e}")
