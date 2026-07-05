import streamlit as st
from PIL import Image
from google import genai

st.set_page_config(page_title="KonumBul", page_icon="🌍", layout="centered")

# ---------- API ANAHTARI ----------
try:
    GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("⚠️ GEMINI_API_KEY bulunamadı. Streamlit Secrets içine ekleyin.")
    st.stop()

client = genai.Client(api_key=GOOGLE_API_KEY)

# ---------- ANALİZ FONKSİYONU ----------
def konumu_analiz_et(img):
    with st.spinner("🔍 Konum analiz ediliyor..."):
        try:
            prompt = """
Bu fotoğrafın nerede çekildiğini tahmin et.

Lütfen Türkçe cevap ver ve şunları belirt:
1. En olası ülke
2. En olası şehir
3. Varsa mahalle/semt
4. Belirgin yapılar veya landmarklar
5. En olası 3 konumu yüzde olasılıklarıyla sırala
6. Hangi ipuçlarına baktığını açıkla:
   - tabelalar
   - mimari
   - yol çizgileri
   - araç plakaları
   - yazı dili
   - bitki örtüsü
   - dağ, deniz, iklim
   - diğer görsel detaylar

Kesin emin değilsen bunu açıkça söyle.
"""

            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=[prompt, img]
            )

            st.success("✅ Analiz tamamlandı!")
            st.markdown(response.text)

        except Exception as e:
            st.error(f"Hata oluştu: {e}")

# ---------- BAŞLIK ----------
st.title("🌍 KonumBul")
st.caption("Fotoğrafı yükle veya yapıştır, konumu tahmin edelim")

# ---------- DOSYA YÜKLEME ----------
st.subheader("📁 Fotoğraf Seç")

uploaded = st.file_uploader(
    "Bilgisayardan / galeriden fotoğraf seç",
    type=["jpg", "jpeg", "png", "webp"]
)

st.markdown("---")

# ---------- YAPIŞTIRMA ----------
st.subheader("📋 Veya Yapıştır")

paste_result = None

try:
    from streamlit_paste_button import paste_image_button as pbutton
    paste_result = pbutton("📋 Görseli Yapıştır")
except Exception:
    st.info("Yapıştırma özelliği için requirements.txt içine şunu ekle: streamlit-paste-button")

st.markdown("---")

# ---------- GÖRSELİ AL ----------
img = None

if uploaded is not None:
    img = Image.open(uploaded)

elif paste_result is not None and hasattr(paste_result, "image_data"):
    if paste_result.image_data is not None:
        img = paste_result.image_data

# ---------- ANALİZ ----------
if img is not None:
    st.image(img, use_container_width=True)

    if st.button("🔍 Konumu Bul", type="primary"):
        konumu_analiz_et(img)

else:
    st.info("👆 Yukarıdan bir fotoğraf yükle veya yapıştır.")
