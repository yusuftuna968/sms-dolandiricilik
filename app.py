import streamlit as st
import joblib
import os

# =========================
# SAYFA AYARLARI
# =========================
st.set_page_config(
    page_title="SMS Dolandırıcılık Tespiti",
    page_icon="📱",
    layout="centered"
)

# =========================
# ARKA PLAN + TASARIM (CSS)
# =========================
st.markdown("""
<style>
/* Arka plan */
.stApp {
    background: linear-gradient(to bottom right, #f7f9fc, #eef2f7);
}

/* Ana kart görünümü */
section.main > div {
    background-color: white;
    padding: 25px;
    border-radius: 14px;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.06);
}

/* Buton stili */
div.stButton > button {
    border-radius: 10px;
    height: 3em;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# ZİYARET SAYACI (GİZLİ)
# =========================
COUNTER_FILE = "counter.txt"

if not os.path.exists(COUNTER_FILE):
    with open(COUNTER_FILE, "w") as f:
        f.write("0")

with open(COUNTER_FILE, "r") as f:
    count = int(f.read())

count += 1

with open(COUNTER_FILE, "w") as f:
    f.write(str(count))

# =========================
# BAŞLIK / AÇIKLAMA
# =========================
st.markdown("""
<h1 style='text-align:center;'>📱 SMS Dolandırıcılık Tespiti</h1>
<p style='text-align:center; font-size:16px;'>
Gelen SMS'in güvenli olup olmadığını saniyeler içinde kontrol edin.
</p>
""", unsafe_allow_html=True)

# =========================
# MODEL YÜKLEME
# =========================
model = joblib.load("sms_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# =========================
# SMS GİRİŞİ
# =========================
st.markdown("### 📩 SMS Metni")
sms = st.text_area(
    "",
    height=150,
    placeholder="Örnek: Tebrikler! 10.000 TL kazandınız..."
)

# =========================
# ANALİZ BUTONU
# =========================
analyze = st.button("🔍 Analiz Et", use_container_width=True)

if analyze:
    if sms.strip() == "":
        st.warning("Lütfen bir mesaj giriniz.")
    else:
        sms_vec = vectorizer.transform([sms])
        result = model.predict(sms_vec)[0]

        st.markdown("---")

        if result == 1:
            st.error("🚨 DOLANDIRICI SMS")

            st.markdown("""
            ### ❓ Bu mesaj neden dolandırıcı olabilir?
            Bu tür mesajlar genellikle:
            - **Acil durum hissi** yaratır,
            - **Ödül veya para vaadi** içerir,
            - Resmî kurum adı kullanıp **şüpheli linkler** barındırır,
            - Kişisel bilgi talep edebilir.

            ⚠️ Bu tür mesajlarda linklere tıklamanız önerilmez.
            """)
        else:
            st.success("✅ GÜVENLİ SMS")

            st.markdown("""
            ### ℹ️ Bilgi
            Bu mesajda yaygın dolandırıcılık kalıpları tespit edilmedi.  
            Yine de şüpheliyseniz resmî kurumlarla doğrulama yapmanız önerilir.
            """)

# =========================
# BİLGİLENDİRİCİ İÇERİKLER
# =========================
with st.expander("🧨 Sık Kullanılan Dolandırıcılık Cümleleri"):
    st.markdown("""
    - Hesabınız askıya alındı  
    - Kazandığınız ödülü almak için tıklayın  
    - Kimlik doğrulama gerekli  
    - 24 saat içinde işlem yapmazsanız hesabınız kapanacaktır  
    - Paketiniz teslim edilemedi  
    - Şüpheli işlem tespit edildi
    """)

with st.expander("🛡️ Dolandırıcılıktan Nasıl Korunursun?"):
    st.markdown("""
    - Bilinmeyen linklere tıklama  
    - Banka ve resmî kurumları **kendin arayarak** doğrula  
    - SMS ile **TC, şifre, kart bilgisi paylaşma**  
    - Şüpheli mesajları sil ve bildir  

    📌 Resmî kurumlar SMS ile kişisel bilgi istemez.
    """)

# =========================
# ADMİN PANELİ (SADECE SEN)
# =========================
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

# =========================
# UYARI + FOOTER
# =========================
st.markdown("""
---
⚠️ **Uyarı:**  
Bu uygulama eğitim ve bilgilendirme amaçlıdır.  
Sonuçlar %100 doğruluk garantisi vermez.

<p style='text-align:center; font-size:12px;'>
Geliştirici: Yusuf Tuna • Streamlit
</p>
""", unsafe_allow_html=True)




