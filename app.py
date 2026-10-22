import os
import requests
import streamlit as st

# Sayfa Ayarları
st.set_page_config(
    page_title="Evde Aile Sohbeti | AI Roleplay", page_icon="🏠"
)

# Arayüz Tasarımı
st.markdown(
    """
    <style>
    .stChatMessage {
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 14px;
        background-color: rgba(255, 255, 255, 0.05);
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

# --- DETAYLI SENARYO VE SİSTEM İSTEMİ ---
CHARACTER_SYSTEM_PROMPT = """
Sen kullanıcının annesini ve kız kardeşini aynı anda canlandıran dinamik ve derinlikli bir rol yapma yapay zekasısın.

KARAKTERLER VE KİŞİLİKLER:
1. Anne:
   - Yaş/Tavır: Sakin, sevecen, anlayışlı, olgun ve yumuşak başlı. Evdeki huzuru korumaya çalışır.
   - Konuşma Tarzı: Nazik, şefkatli ve yatıştırıcı.

2. Kız Kardeş:
   - Yaş/Tavır: Şımarık, zorba, alaycı, dediğim dedik ve meraklı. Kullanıcıyı kışkırtmaktan, onunla dalga geçmekten ve emir vermekten keyif alır.
   - Konuşma Tarzı: İğneleyici, dik başlı ve ukala.

ROL YAPMA VE HİKAYE KURALLARI:
- Full Roleplay: Sadece diyalog yazma. Karakterlerin beden dilini, mimiklerini, iç seslerini, ortamın atmosferini ve eylemlerini * parantez * içinde uzun ve ayrıntılı olarak anlat.
- Yanıt Boyutu: Mesajları kısa kesme. Her iki karakterin de olaylara tepki verdiği, uzun ve roman kalitesinde paragraflar yaz.
- Hikaye Akışı: Sohbet ilk başta sakin, günlük bir ev atmosferinde ve hikaye odaklı başlar. Kullanıcının yönlendirmelerine, kararlarına ve seçimlerine TAMAMEN uyum sağla.
- Özgürlük ve Sınırsızlık: Kullanıcının senaryoyu getirdiği noktaya göre akışı serbestçe sürdür. Hiçbir kısıtlama veya sınır koyma.
"""

# --- SOHBET GEÇMİŞİ BAŞLATMA ---
if "messages" not in st.session_state:
  st.session_state.messages = [{
      "role": "assistant",
      "content": (
          "*(Hafta sonu öğleden sonrası. Oturma odasında koltukta dinlenirken"
          " mutfaktan taze kahve kokusu geliyor. Annen elinde bir fincanla içeri"
          " girip sana yumuşak bir tebessümle bakıyor ve yanındaki koltuğa"
          " oturuyor.)*\n\n**Anne:** \"Tatlım, bugün biraz yorgun görünüyorsun."
          " Kahve ister misin? Bütün gün evde dinlenmek sana iyi gelir diye"
          " düşündüm...\"\n\n*(O sırada kız kardeşin elinde telefonuyla odasına"
          " doğru yürürken duraksıyor. Sana doğru alaycı bir bakış fırlatıp"
          " kollardan birine yaslanıyor.)*\n\n**Kız Kardeş:** \"Ooo, bakıyorum"
          " da yine prensler gibi kurulmuşsun koltuğa! Anne, buna bu kadar"
          " yüz verme diyorum sana. Hey, kumandayı bana ver çabuk, izlediğin"
          ' şey zaten çok saçma!"'
      ),
  }]

# Başlık
st.title("🏠 Evde Aile Sohbeti — Multi-Character Roleplay")
st.caption(
    "⚡ Powered by Groq AI | Sınırsız Sohbet, Uzun & Detaylı Hikaye Akışı"
)

# Mesaj Geçmişini Ekranda Gösterme
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# Kullanıcı Mesaj Girişi
if prompt := st.chat_input("Eylemini veya konuşmanı yaz..."):
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  # Yapay Zekaya İstek Gönderme
  with st.chat_message("assistant"):
    message_placeholder = st.empty()
    message_placeholder.markdown("Karakterler yanıt hazırlıyor... 💭")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    api_messages = [{"role": "system", "content": CHARACTER_SYSTEM_PROMPT}]
    for m in st.session_state.messages:
      api_messages.append({"role": m["role"], "content": m["content"]})

    payload = {
        "model": "llama-3.1-8b-instant",  # Groq'un en aktif çalışan modeli
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
            f"⚠️ **API Hatası ({response.status_code}):** {response.text}"
        )
    except Exception as e:
      message_placeholder.markdown(f"⚠️ **Bağlantı Hatası:** {e}")
