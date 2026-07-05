import streamlit as st
from PIL import Image
import io

st.set_page_config(page_title="Konum Bul", page_icon="🌍", layout="centered")

st.title("🌍 KonumBul")
st.caption("Fotoğrafı yükle, konumu bulalım")

# 📁 DOSYA YÜKLEME - EN ÜSTTE
st.subheader("📁 Fotoğraf Seç")
uploaded = st.file_uploader(
    "Bilgisayardan / galeriden fotoğraf seç",
    type=["jpg", "jpeg", "png", "webp"]
)

st.markdown("---")

# 📋 YAPIŞTIRMA - ayrı bölümde
st.subheader("📋 Veya Yapıştır")
try:
    from streamlit_paste_button import paste_image_button as pbutton
    paste_result = pbutton("📋 Görseli Yapıştır (Ctrl+V)")
except Exception as e:
    st.warning(f"Yapıştırma butonu yüklenemedi: {e}")
    paste_result = None

st.markdown("---")

# Görsel geldiyse göster
img = None
if uploaded is not None:
    img = Image.open(uploaded)
elif paste_result is not None and paste_result.image_data is not None:
    img = paste_result.image_data

if img is not None:
    st.image(img, use_container_width=True)
    st.success("✅ Görsel alındı! (Analiz kodu buraya eklenecek)")
