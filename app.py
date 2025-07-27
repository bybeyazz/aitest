import streamlit as st
import torch
from diffusers import StableDiffusionPipeline
from PIL import Image
import time

st.set_page_config(
    page_title="🎨 AI Görsel Üretici",
    page_icon="🎨"
)

st.title("🎨 AI Görsel Üretici")
st.success("✅ Uygulama çalışıyor!")

# Sidebar
with st.sidebar:
    st.header("⚙️ Ayarlar")
    
    if torch.cuda.is_available():
        st.success(f"✅ CUDA Aktif\n\n**GPU:** {torch.cuda.get_device_name(0)}")
    else:
        st.warning("⚠️ CPU ile çalışacak")
    
    steps = st.slider("Adım Sayısı", 10, 100, 30)
    guidance = st.slider("Yaratıcılık", 1.0, 20.0, 7.5)

# Ana içerik
col1, col2 = st.columns(2)

with col1:
    st.header("✍️ Prompt")
    prompt = st.text_input("Prompt girin:", "beautiful landscape")
    
    negative_prompt = st.text_area("İstemediğiniz şeyler:",
                                  "blurry, low quality, bad anatomy, ugly",
                                  height=100)
    
    if st.button("🚀 Görsel Üret", use_container_width=True):
        if prompt.strip():
            try:
                with st.spinner("🎨 AI görsel üretiyor..."):
                    # Modeli yükle
                    pipe = StableDiffusionPipeline.from_pretrained(
                        "runwayml/stable-diffusion-v1-5",
                        torch_dtype=torch.float16,
                        safety_checker=None,
                    )
                    pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")
                    
                    # Görsel üret
                    image = pipe(
                        prompt,
                        negative_prompt=negative_prompt,
                        num_inference_steps=steps,
                        guidance_scale=guidance
                    ).images[0]
                    
                    # Session state'e kaydet
                    st.session_state.generated_image = image
                    st.session_state.last_prompt = prompt
                    
                    st.success("✅ Görsel üretildi!")
                    
            except Exception as e:
                st.error(f"❌ Hata: {str(e)}")
        else:
            st.warning("Lütfen bir prompt girin!")

with col2:
    st.header("🖼️ Üretilen Görsel")
    
    if 'generated_image' in st.session_state:
        st.image(st.session_state.generated_image, 
                caption=st.session_state.last_prompt,
                use_column_width=True)
        
        # İndirme butonu
        import io
        buf = io.BytesIO()
        st.session_state.generated_image.save(buf, format="PNG")
        st.download_button(
            label="💾 Görseli İndir",
            data=buf.getvalue(),
            file_name="ai_art.png",
            mime="image/png",
            use_container_width=True
        )
    else:
        st.info("🎨 Henüz görsel üretilmedi")

# Footer
st.markdown("---")
st.markdown("🎯 AI Görsel Üretici - Streamlit ile")
