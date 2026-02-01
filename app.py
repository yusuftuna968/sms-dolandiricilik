import streamlit as st
import joblib
import os

# --------------------
# ZİYARET SAYACI
# --------------------
COUNTER_FILE = "counter.txt"

if not os.path.exists(COUNTER_FILE):
    with open(COUNTER_FILE, "w") as f:
        f.write("0")

with open(COUNTER_FILE, "r") as f:
    count = int(f.read())

count += 1

with open(COUNTER_FILE, "w") as f:
    f.write(str(count))

# --------------------
# SAYFA AYARLARI
# --------------------
st.set_page_config(page_title="SMS Kontrol", page_icon="📱")
st.title("📱 SMS Dolandırıcılık Tespiti")


# --------------------
# MODEL YÜKLEME
# --------------------
model = joblib.load("sms_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# --------------------
# KULLANICI GİRDİSİ
# --------------------
sms = st.text_area("📩 SMS mesajını yaz")

if st.button("🔍 Analiz Et"):
    if sms.strip() == "":
        st.warning("Lütfen bir mesaj giriniz.")
    else:
        sms_vec = vectorizer.transform([sms])
        result = model.predict(sms_vec)[0]

        if result == 1:
            st.error("🚨 DOLANDIRICI SMS")

            st.markdown("""
            ### ❓ Bu mesaj neden dolandırıcı olabilir?
            Bu tür mesajlar genellikle:
            - **Acil durum hissi** yaratır,
            - **Ödül veya para vaadi** içerir,
            - Resmî kurum adı kullanıp **şüpheli linkler** barındırır,
            - Kişisel bilgi talep edebilir.

            ⚠️ Bu tür mesajlarda linklere tıklamamanız önerilir.
            """)
        else:
            st.success("✅ GÜVENLİ SMS")

# --------------------
# BİLGİLENDİRİCİ İÇERİKLER
# --------------------
st.markdown("""
---
### 🧨 Sık Kullanılan Dolandırıcılık Cümleleri
- “Hesabınız askıya alındı”
- “Kazandığınız ödülü almak için tıklayın”
- “Kimlik doğrulama gerekli”
- “24 saat içinde işlem yapmazsanız hesabınız kapanacaktır”
- “Paketiniz teslim edilemedi”
- “Şüpheli işlem tespit edildi”
""")

st.markdown("""
---
### 🛡️ Dolandırıcılıktan Nasıl Korunursun?
- Bilinmeyen linklere tıklama
- Resmî kurumları **kendin arayarak** doğrula
- SMS ile **kişisel bilgi paylaşma**
- Şüpheli mesajları sil ve bildir

📌 Resmî kurumlar SMS ile şifre istemez.
""")

# --------------------
# UYARI (HUKUKİ KORUMA)
# --------------------
st.markdown("""
---
⚠️ **Uyarı:**  
Bu uygulama bilgilendirme ve eğitim amaçlıdır.  
Sonuçlar %100 doğruluk garantisi vermez.
""")
st.markdown("---")
st.subheader("🔐 Admin Paneli")

admin_password = st.text_input(
    "Admin şifresi",
    type="password",
    placeholder="Sadece site sahibi"
)

if admin_password == "546500":
    st.success("Giriş başarılı")
    st.metric("👥 Toplam ziyaret", count)
elif admin_password != "":
    st.error("Yetkisiz erişim")




