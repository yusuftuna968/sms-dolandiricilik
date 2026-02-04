import streamlit as st
import joblib
from datetime import datetime

# -----------------------
# GOOGLE ANALYTICS
# -----------------------
import streamlit.components.v1 as components

components.html(
    """
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-63LPCQH8GH"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-63LPCQH8GH');
    </script>
    """,
    height=0
)

# -----------------------
# SAYFA AYARLARI
# -----------------------
st.set_page_config(
    page_title="SMS Guard",
    page_icon="🛡️",
    layout="centered"
)

# -----------------------
# SESSION STATE
# -----------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------
# MODEL YÜKLEME
# -----------------------
model = joblib.load("sms_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# -----------------------
# BAŞLIK
# -----------------------
st.markdown(
    "<h1 style='text-align:center;'>🛡️ SMS Guard</h1>"
    "<p style='text-align:center;'>SMS Dolandırıcılık Tespit Sistemi</p>",
    unsafe_allow_html=True
)

# -----------------------
# SMS GİRİŞ
# -----------------------
sms = st.text_area(
    "📩 SMS Metni",
    height=150,
    placeholder="Örnek: Tebrikler! 10.000 TL kazandınız..."
)

analyze = st.button("🔍 Analiz Et", use_container_width=True)

if analyze:
    if sms.strip() == "":
        st.warning("Lütfen bir SMS girin.")
    else:
        sms_vec = vectorizer.transform([sms])
        sonuc = model.predict(sms_vec)[0]

        if sonuc == 1:
            st.error("🚨 DOLANDIRICI SMS")
            aciklama = "DOLANDIRICI"
        else:
            st.success("✅ GÜVENLİ SMS")
            aciklama = "GÜVENLİ"

        st.session_state.history.append({
            "time": datetime.now().strftime("%H:%M"),
            "sms": sms[:80],
            "result": aciklama
        })

# -----------------------
# BİLGİLENDİRME
# -----------------------
st.markdown("""
---
### 🧨 Sık Kullanılan Dolandırıcılık Cümleleri
- “Hesabınız askıya alındı”
- “Kazandığınız ödülü almak için tıklayın”
- “24 saat içinde işlem yapmazsanız hesabınız kapanacaktır”
- “Paketiniz teslim edilemedi”
- “Şüpheli işlem tespit edildi”
""")

st.markdown("""
---
### 🛡️ Dolandırıcılıktan Nasıl Korunursun?
- Bilinmeyen linklere tıklama
- SMS ile TC, şifre, kart bilgisi paylaşma
- Resmî kurumları kendin arayarak doğrula

⚠️ Bu uygulama **bilgilendirme amaçlıdır**, %100 doğruluk garanti etmez.
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

