import streamlit as st
import joblib
import os
import time
from datetime import datetime

# ----------------------
# SAYFA AYAR
# ----------------------
st.set_page_config(
    page_title="SMS Guard",
    page_icon="🛡️",
    layout="centered"
)

# ----------------------
# ZİYARETÇİ SAYACI
# ----------------------
COUNTER_FILE = "counter.txt"

if not os.path.exists(COUNTER_FILE):
    with open(COUNTER_FILE, "w") as f:
        f.write("0")

with open(COUNTER_FILE, "r") as f:
    count = int(f.read())

count += 1

with open(COUNTER_FILE, "w") as f:
    f.write(str(count))

# ----------------------
# OTURUM BAŞLANGIÇ SÜRESİ
# ----------------------
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# ----------------------
# MODEL YÜKLEME
# ----------------------
model = joblib.load("sms_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# ----------------------
# ANALİZ GEÇMİŞİ
# ----------------------
if "history" not in st.session_state:
    st.session_state.history = []

# ----------------------
# BAŞLIK
# ----------------------
st.title("🛡️ SMS Guard")
st.write("SMS Dolandırıcılık Tespit Sistemi")

# ----------------------
# SMS ANALİZ
# ----------------------
sms = st.text_area("📩 SMS Mesajını Yaz")

analyze = st.button("🔍 Analiz Et", use_container_width=True)

if analyze:
    if sms.strip() == "":
        st.warning("Mesaj gir.")
    else:
        sms_vec = vectorizer.transform([sms])
        sonuc = model.predict(sms_vec)[0]

        if sonuc == 1:
            st.error("🚨 DOLANDIRICI SMS")
            sonuc_text = "Dolandırıcı"
        else:
            st.success("✅ Güvenli SMS")
            sonuc_text = "Güvenli"

        gecen_sure = int((time.time() - st.session_state.start_time) / 60)

        st.session_state.history.append({
            "time": datetime.now().strftime("%H:%M"),
            "result": sonuc_text,
            "sure": gecen_sure
        })

# ----------------------
# BİLGİ YAZILARI
# ----------------------
st.markdown("""
---
### 🧨 Dolandırıcılık Mesajlarında Sık Görülenler
- “Ödül kazandınız”
- “Hesabınız askıya alındı”
- “Hemen linke tıklayın”
- “Şüpheli işlem var”

⚠️ Linklere tıklamadan önce kontrol edin.
""")

# ======================
# ADMIN PANEL
# ======================
ADMIN_PASSWORD = "546500"

st.sidebar.markdown("---")
st.sidebar.subheader("🔐 Admin Panel")

admin_pass = st.sidebar.text_input(
    "Şifre",
    type="password"
)

if admin_pass:
    if admin_pass == ADMIN_PASSWORD:
        st.sidebar.success("Giriş başarılı")

        # 👉 Ziyaretçi sayısı
        st.sidebar.write(f"👥 Toplam ziyaret: {count}")

        # 👉 Ortalama süre hesaplama
        if len(st.session_state.history) > 0:
            ortalama = sum([x["sure"] for x in st.session_state.history]) // len(st.session_state.history)
            st.sidebar.write(f"⏱ Ortalama süre: {ortalama} dk")

        st.sidebar.markdown("### 📊 Son Analizler")

        for item in reversed(st.session_state.history[-10:]):
            st.sidebar.write(
                f"{item['time']} | {item['result']} | {item['sure']} dk"
            )

    else:
        st.sidebar.error("Şifre yanlış")




