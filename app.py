import os

COUNTER_FILE = "counter.txt"

if not os.path.exists(COUNTER_FILE):
    with open(COUNTER_FILE, "w") as f:
        f.write("0")

with open(COUNTER_FILE, "r") as f:
    count = int(f.read())

count += 1

with open(COUNTER_FILE, "w") as f:
    f.write(str(count))
import streamlit as st
import joblib

st.set_page_config(page_title="SMS Kontrol", page_icon="📱")
st.info(f"👥 Bu site şu ana kadar {count} kez ziyaret edildi")
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

