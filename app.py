import streamlit as st
from geoclip import GeoCLIP
from PIL import Image
import tempfile
import os
import pandas as pd

st.set_page_config(page_title="Foto Konum Bulucu", page_icon="📍", layout="centered")

st.title("📍 Fotoğraftan Konum Tahmini")
st.write("Bir fotoğraf yükle veya kamerayla çek, yapay zeka nerede çekildiğini tahmin etsin!")

# Modeli sadece bir kez yükle (hızlı olsun diye)
@st.cache_resource
def load_model():
    return GeoCLIP()

model = load_model()

# Fotoğraf giriş yöntemi seç
secim = st.radio("Fotoğraf nasıl gelsin?", ["Dosya Yükle", "Kamerayla Çek"])

image_file = None
if secim == "Dosya Yükle":
    image_file = st.file_uploader("Fotoğraf seç", type=["jpg", "jpeg", "png"])
else:
    image_file = st.camera_input("Fotoğraf çek")

if image_file is not None:
    # Fotoğrafı göster
    img = Image.open(image_file)
    st.image(img, caption="Yüklenen fotoğraf", use_container_width=True)

    # Geçici dosyaya kaydet (model dosya yolu istiyor)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        img.convert("RGB").save(tmp.name)
        tmp_path = tmp.name

    with st.spinner("Konum tahmin ediliyor... 🌍"):
        top_pred_gps, top_pred_prob = model.predict(tmp_path, top_k=5)

    os.remove(tmp_path)

    st.subheader("🎯 En Olası 5 Konum")

    # En iyi tahmini haritada göster
    en_iyi_lat = float(top_pred_gps[0][0])
    en_iyi_lon = float(top_pred_gps[0][1])

    harita_df = pd.DataFrame({"lat": [en_iyi_lat], "lon": [en_iyi_lon]})
    st.map(harita_df, zoom=6)

    # Listeyi yazdır
    for i in range(len(top_pred_gps)):
        lat = float(top_pred_gps[i][0])
        lon = float(top_pred_gps[i][1])
        prob = float(top_pred_prob[i])
        link = f"https://www.google.com/maps?q={lat},{lon}"
        st.markdown(
            f"**{i+1}.** Enlem: `{lat:.4f}`, Boylam: `{lon:.4f}` "
            f"— güven: `{prob:.3f}` — [Google Maps'te aç]({link})"
        )