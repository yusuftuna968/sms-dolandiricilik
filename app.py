import streamlit as st
import joblib
import os
from datetime import datetime

# ======================
# ENV / ADMIN
# ======================
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# ======================
# SAYFA AYARI
# ======================
st.set_page_config(
    page_title="SMS Guard",
    page_icon="🛡️",
    layout="centered"
)

# ======================
# SESSION STATE
# ======================
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

if "history" not in st.session_state:
    st.session_state.history = []

# ======================
# DARK MODE TOGGLE
# ======================
st.sidebar.title("⚙️ Ayarlar")
st.session_state.dark_mode = st.sidebar.toggle(
    "🌙 Koyu Mod", value=st.session_state.dark_mode
)

# ======================
# CSS
# ======================
if st.session_state.dark_mode:
    bg = "#0f172a"
    card = "#020617"
    text = "#e5e7eb"
else:
    bg = "#f7f9fc"
    card = "#ffffff"
    text = "#0f172a"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {bg};
        color: {text};
    }}
    section.main > div {{
        background-color: {card};
        padding: 25px;
        border-radius: 14px;
        box-shadow: 0px 4px 14px rgba(0,0,0,0.08);
    }}
    div.stButton > button {{
        border-radius: 10px;
        height: 3em;
        font-size: 16px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ======================
# MODEL YÜKLE
# ======================
model = joblib.load("sms_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# ======================
# BAŞLIK
# ======================
st.markdown(
    "<h1 style='text-align:center;'>🛡️ SMS Guard</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center;'>SMS mesajlarını yapay zekâ ile analiz eder</p>",
    unsafe_allow_html=True
)

# ======================
# ANA UYGULAMA
# ======================
sms = st.text_area(
    "📩 SMS Metni",
    height=150,
    placeholder="Örnek: Tebrikler! Ödül kazandınız..."
)

analyze = st.button("🔍 Analiz Et", use_container_width=True)

if analyze:
    if sms.strip() == "":
        st.warning("Lütfen bir mesaj giriniz.")
    else:
        sms_vec = vectorizer.transform([sms])
        result = model.predict(sms_vec)[0]

        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M")
        label = "DOLANDIRICI" if result == 1 else "GÜVENLİ"

        # Admin için geçmişe ekle
        st.session_state.history.append({
            "time": timestamp,
            "sms": sms[:120],
            "result": label
        })

        if result == 1:
            st.error("🚨 DOLANDIRICI MESAJ!")
            st.markdown("""
            ### ❗ Neden şüpheli olabilir?
            - Aciliyet hissi oluşturur  
            - Para / ödül vaadi içerir  
            - Link veya bilgi ister  

            ⚠️ Linklere tıklamayın, bilgi paylaşmayın.
            """)
        else:
            st.success("✅ GÜVENLİ MESAJ")

# ======================
# BİLGİLENDİRME
# ======================
st.markdown("""
---
### 🛡️ Dolandırıcılıktan Nasıl Korunursun?
- Bilinmeyen linklere tıklama  
- SMS ile kimlik / kart bilgisi verme  
- Resmî kurumları kendin arayarak doğrula  

📌 Bu uygulama **bilgilendirme amaçlıdır**, %100 doğruluk garantisi vermez.
""")
# ======================
# 🔐 ADMIN PANEL
# ======================

ADMIN_PASSWORD = "546500"

st.sidebar.markdown("---")
st.sidebar.subheader("🔐 Admin Panel")

admin_pass = st.sidebar.text_input(
    "Admin Şifre",
    type="password"
)

# session_state yoksa oluştur
if "history" not in st.session_state:
    st.session_state.history = []

if admin_pass:
    if admin_pass == ADMIN_PASSWORD:
        st.sidebar.success("Giriş başarılı")

        st.sidebar.markdown("### 📊 Analiz Geçmişi")

        if len(st.session_state.history) == 0:
            st.sidebar.info("Henüz analiz yok.")
        else:
            for item in reversed(st.session_state.history[-10:]):
                st.sidebar.write(
                    f"🕒 {item['time']} | {item['result']}\n\n"
                    f"📩 {item['sms']}"
                )

    else:
        st.sidebar.error("Şifre yanlış")








