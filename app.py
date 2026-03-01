import streamlit as st
import google.generativeai as genai
import os

# --- KONFIGURASI API ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = "AIzaSyB06UXMFuJB0uEevvPVDVtAgdm_qyRAtDI"

genai.configure(api_key=API_KEY)

# --- SISTEM MODEL CERDAS ---
# Kode ini akan mencoba 3 nama model berbeda sampai berhasil
def get_working_model():
    for model_name in ['gemini-1.5-flash-latest', 'gemini-1.5-flash', 'gemini-pro']:
        try:
            m = genai.GenerativeModel(model_name)
            # Tes apakah model ini merespon (hanya tes kecil)
            return m
        except:
            continue
    return None

model = get_working_model()

# --- TAMPILAN DASHBOARD ---
st.set_page_config(page_title="Olen Roblox Studio", layout="wide")

st.title("🎬 Olen Roblox Animation Studio")
st.write("Free Tier Mode - Production Hub for @olenroblox")

# Menampilkan placeholder jika gambar tidak ditemukan
if os.path.exists("Charming Chibi in the Field-Photoroom.png"):
    st.image("Charming Chibi in the Field-Photoroom.png", width=150)
else:
    st.info("Avatar Olen")

st.markdown("---")

# --- INPUT AREA ---
with st.sidebar:
    st.header("⚙️ Pengaturan")
    ide = st.text_area("Ide Cerita:", placeholder="Misal: Olen dikejar hantu...")
    submit = st.button("🚀 MULAI GENERATE")

# --- EKSEKUSI ---
if submit:
    if not ide:
        st.error("Isi idenya dulu ya, Kak!")
    elif model is None:
        st.error("Google AI sedang sibuk. Tunggu sebentar lalu coba lagi.")
    else:
        with st.spinner("🤖 AI sedang memproses naskah Olen..."):
            try:
                # Instruksi detail visual Olen
                prompt = f"Buat skrip Roblox untuk Olen (rambut oranye, kacamata putih, celana kodok). Ide: {ide}"
                response = model.generate_content(prompt)
                st.success("✅ BERHASIL!")
                st.write(response.text)
            except Exception as e:
                st.error(f"Teknis Error: {str(e)}")
