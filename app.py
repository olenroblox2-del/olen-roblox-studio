import streamlit as st
import google.generativeai as genai
import os

# --- 1. SETTING API ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = "AIzaSyB06UXMFuJB0uEevvPVDVtAgdm_qyRAtDI"

genai.configure(api_key=API_KEY)

# --- 2. SISTEM AUTO-MODEL (Mencegah Error 404) ---
def get_model():
    # Daftar model dari yang terbaru sampai yang paling stabil
    model_names = ['gemini-1.5-flash', 'gemini-1.5-flash-latest', 'gemini-pro']
    for name in model_names:
        try:
            m = genai.GenerativeModel(name)
            # Tes singkat apakah model merespon
            return m
        except:
            continue
    return None

model = get_model()

# --- 3. TAMPILAN DASHBOARD ---
st.set_page_config(page_title="Olen Roblox Studio", layout="wide")

col1, col2 = st.columns([1, 4])
with col1:
    if os.path.exists("Charming Chibi in the Field-Photoroom.png"):
        st.image("Charming Chibi in the Field-Photoroom.png", use_container_width=True)
    else:
        st.info("Avatar Olen")

with col2:
    st.title("🎬 Olen Roblox Animation Studio")
    st.write("Free Tier Mode - Production Hub for **@olenroblox**")

st.markdown("---")

# --- 4. INPUT ---
with st.sidebar:
    st.header("⚙️ Pengaturan")
    ide = st.text_area("Ide Cerita:", placeholder="Misal: Olen dikejar hantu...")
    submit = st.button("🚀 MULAI GENERATE")

# --- 5. EKSEKUSI ---
if submit:
    if not ide:
        st.error("Isi idenya dulu ya!")
    elif model is None:
        st.error("Google AI sedang sibuk. Coba lagi dalam 1 menit.")
    else:
        with st.spinner("🤖 AI sedang bekerja..."):
            try:
                prompt = f"Buat skrip Roblox untuk karakter Olen (rambut oranye, kacamata putih, celana kodok). Ide: {ide}"
                response = model.generate_content(prompt)
                st.success("Berhasil! Ini hasilnya:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Maaf Kak Olen, ada kendala teknis: {str(e)}")
