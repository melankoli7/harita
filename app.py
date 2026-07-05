import streamlit as st
from streamlit_paste_button import paste_image_button as pbutton
import google.generativeai as genai
from PIL import Image
import io

st.set_page_config(page_title="Konum Bul", page_icon="🌍", layout="centered")

# 🎨 Google tarzı sade tasarım
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    #MainMenu, footer, header { visibility: hidden; }
    .google-title {
        text-align: center;
        font-family: Arial, sans-serif;
        font-size: 46px;
        font-weight: 500;
        margin-top: 20px;
        margin-bottom: 4px;
    }
    .g-blue { color: #4285F4; }
    .g-red { color: #EA4335; }
    .g-yellow { color: #FBBC05; }
    .g-green { color: #34A853; }
    .subtitle {
        text-align: center;
        color: #70757a;
        font-family: Arial, sans-serif;
        font-size: 15px;
        margin-bottom: 25px;
    }
    .result-row {
        font-family: Arial, sans-serif;
        font-size: 17px;
        padding: 8px 0;
        border-bottom: 1px solid #ececec;
    }
    .result-label { color: #70757a; font-size: 13px; }
    .result-value { color: #202124; font-weight: 500; }
    .main-answer {
        font-family: Arial, sans-serif;
        font-size: 26px;
        font-weight: 600;
        color: #202124;
        padding: 12px 0 4px 0;
    }
    .or-text {
        text-align: center;
        color: #9aa0a6;
        font-family: Arial, sans-serif;
        font-size: 13px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Google tarzı başlık
st.markdown("""
<div class="google-title">
    <span class="g-blue">K</span><span class="g-red">o</span><span class="g-yellow">n</span><span class="g-blue">u</span><span class="g-green">m</span><span class="g-red">B</span><span class="g-blue">u</span><span class="g-yellow">l</span>
</div>
<div class="subtitle">Fotoğrafı yapıştır ya da yükle, konumu bulalım 🌍</div>
""", unsafe_allow_html=True)

# 🔑 Gemini API key
genai.configure(api_key= " AQ.Ab8RN6Lae3FgyYyNAldF5D5Lu13PRzjp9sRDBSPfFcRPBXHbLw")

PROMPT = """Sen dünyanın en iyi GeoGuessr şampiyonusun. Görsel analizde dahisin.
Fotoğraftan bir yerin konumunu %99 isabetle bulabilirsin.

ÇOK ÖNEMLİ ÇALIŞMA YÖNTEMİN:
Cevap vermeden ÖNCE, ANALİZ bölümünde adım adım YÜKSEK SESLE düşün.
Acele etme. Her ipucunu tek tek incele, ihtimalleri karşılaştır ve eleme yaparak
en olası konuma ulaş. Erken karar verme, tüm kanıtları topla.

İNCELEYECEĞİN İPUÇLARI:
1. DİL & YAZI: Tabela dili, alfabe, dükkan isimleri, yazı tipi, harf işaretleri
2. MİMARİ: Çatı biçimi, bina malzemesi, pencere/balkon tarzı, renk
3. DOĞA: Bitki örtüsü, ağaç türleri, toprak rengi, tarım, iklim, coğrafya
4. YOL: Trafik yönü (sağ/sol şerit), yol çizgi rengi, asfalt tipi, kaldırım taşı
5. ALTYAPI: Elektrik direkleri biçimi, tabela direkleri, korkuluklar, bariyerler
6. ARAÇLAR: Plaka rengi/biçimi, araç marka-modelleri, o ülkede yaygın araçlar
7. GÖK & IŞIK: Güneş açısı, gölge yönü, gökyüzü, mevsim, saat tahmini
8. İNSAN: Kıyafet tarzı, cilt tonu, kültürel-dini ipuçları

ELEME YÖNTEMİ:
"Şu detay X ülkesini gösteriyor AMA şu detay Y ülkesine daha uygun.
Trafik yönü ve plaka rengi birleştiğinde en olası olan..." şeklinde mantık yürüt.
Sonra kesin kararını ver.

ŞU FORMATTA CEVAP VER (formatı bozma):

ANALİZ: (buraya tüm adım adım düşünceni, elemelerini, mantığını yaz)
###
ÜLKE: (en olası ülke)
EYALET: (eyalet / il / bölge adı)
ÜLKEDEKİ KONUM: (ülkenin neresinde, ör: kuzeydoğusunda, güneybatısında)
YAKIN ŞEHİR: (en yakın büyük şehir)
ŞEHRE GÖRE KONUM: (o şehrin neresinde, ör: yaklaşık 40 km güneyinde)
GÜVEN: (%oran)
2. İHTİMAL: (yanılıyorsan ikinci en olası konum)
İPUÇLARI: (kararının en güçlü 3 somut dayanağı, kısa)"""


def konumu_analiz_et(img):
    """Verilen PIL görselini analiz edip sonucu gösterir."""
    st.image(img, use_container_width=True)

    with st.spinner("🔎 Detaylı analiz ediliyor..."):
        try:
            buf = io.BytesIO()
            img.convert("RGB").save(buf, format="JPEG", quality=100)
            image_part = {"mime_type": "image/jpeg", "data": buf.getvalue()}

            model = genai.GenerativeModel(
                "gemini-3.1-flash-lite",
                generation_config={"temperature": 0.2}
            )
            response = model.generate_content([PROMPT, image_part])
            text = response.text
        except Exception as e:
            st.error(f"❌ HATA: {e}")
            return

    # ANALİZ ile SONUÇ kısmını ayır
    if "###" in text:
        analiz_kismi, sonuc_kismi = text.split("###", 1)
    else:
        analiz_kismi, sonuc_kismi = "", text

    # Sonucu ayrıştır
    data = {}
    for line in sonuc_kismi.split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip()

    st.markdown("<br>", unsafe_allow_html=True)

    # Ana cevap büyük göster
    st.markdown(
        f'<div class="main-answer">🌍 {data.get("ÜLKE","?")} — {data.get("YAKIN ŞEHİR","?")}</div>',
        unsafe_allow_html=True
    )

    def row(label, value):
        return f"""<div class="result-row">
            <div class="result-label">{label}</div>
            <div class="result-value">{value}</div>
        </div>"""

    html = ""
    html += row("🗺️ EYALET / BÖLGE", data.get("EYALET", "?"))
    html += row("🧭 ÜLKEDEKİ KONUM", data.get("ÜLKEDEKİ KONUM", "?"))
    html += row("📍 ŞEHRE GÖRE KONUM", data.get("ŞEHRE GÖRE KONUM", "?"))
    html += row("🎯 GÜVEN", data.get("GÜVEN", "?"))
    html += row("🔄 2. İHTİMAL", data.get("2. İHTİMAL", "?"))
    st.markdown(html, unsafe_allow_html=True)

    # Gizli: modelin düşünme süreci
    with st.expander("🧠 Modelin düşünme süreci (analiz)"):
        st.write(analiz_kismi.strip() if analiz_kismi.strip() else "—")

    with st.expander("🔍 En güçlü ipuçları"):
        st.write(data.get("İPUÇLARI", "—"))


# 📋 1. YOL: Yapıştırma butonu
paste_result = pbutton("📋 Görseli Yapıştır (Ctrl+V)")

# arada "veya" yazısı
st.markdown('<div class="or-text">— veya —</div>', unsafe_allow_html=True)

# 📁 2. YOL: Dosyadan / galeriden fotoğraf ekleme
uploaded = st.file_uploader(
    "📁 Fotoğraf seç (bilgisayar / galeri)",
    type=["jpg", "jpeg", "png", "webp"],
    label_visibility="visible"
)

# Hangisi doluysa onu analiz et (yapıştırma önceliklidir)
if paste_result.image_data is not None:
    konumu_analiz_et(paste_result.image_data)
elif uploaded is not None:
    img = Image.open(uploaded)
    konumu_analiz_et(img)
