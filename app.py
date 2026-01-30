import streamlit as st
import joblib

st.set_page_config(page_title="SMS Kontrol", page_icon="📱")

model = joblib.load("sms_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

st.title("📱 SMS Dolandırıcılık Tespiti")

sms = st.text_area("SMS mesajını yaz")

if st.button("Analiz Et"):
    if sms.strip() == "":
        st.warning("Mesaj gir")
    else:
        sms_vec = vectorizer.transform([sms])
        sonuc = model.predict(sms_vec)[0]

        if sonuc == 1:
            st.error("🚨 DOLANDIRICI SMS")
        else:
            st.success("✅ GÜVENLİ SMS")
