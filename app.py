import streamlit as st

st.set_page_config(
    page_title="🎨 AI Görsel Üretici",
    page_icon="🎨"
)

st.title("🎨 AI Görsel Üretici")
st.success("✅ Uygulama çalışıyor!")

# Basit arayüz
prompt = st.text_input("Prompt girin:", "beautiful landscape")
if st.button("Üret"):
    st.info("⚠️ AI modülleri henüz yüklenmedi")
    st.image("https://placehold.co/400x400/667eea/ffffff?text=AI+Sanat")

st.markdown("---")
st.markdown("🎯 Sonraki adımda AI entegrasyonu eklenecek!")