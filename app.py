import streamlit as st
import google.generativeai as genai
import os

# --- 1. SETTING API KEY ---
# Mengambil dari Secrets Streamlit Cloud (Pastikan sudah diisi di Manage App > Settings > Secrets)
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    # Jika di laptop sendiri, pakai ini
    API_KEY = "AIzaSyB06UXMFuJB0uEevvPVDVtAgdm_qyRAtDI"

genai.configure(api_key=API_KEY)

# --- 2. PILIH MODEL STABIL ---
model = genai.GenerativeModel('gemini-pro')

# --- 3. TAMPILAN DASHBOARD ---
st.set_page_config(page_title="Olen Roblox Studio", layout="wide", page_icon="🦊")

col1, col2 = st.columns([1, 4])
with col1:
    # Menggunakan nama file gambar yang Kak Olen upload sebelumnya
    if os.path.exists("Charming Chibi in the Field-Photoroom.png"):
        st.image("Charming Chibi in the Field-Photoroom.png", use_container_width=True)
    else:
        st.info("Avatar Olen")

with col2:
    st.title("🎬 Olen Roblox Animation Studio")
    st.write("Ubah ide ceritamu jadi konten viral untuk **@olenroblox**")

st.markdown("---")

# --- 4. SIDEBAR INPUT ---
with st.sidebar:
    st.header("⚙️ Pengaturan Produksi")
    tema = st.selectbox("Pilih Tema:", ["Horror Survival", "Comedy Skit", "Action", "Drama"])
    pendamping = st.multiselect("Karakter Teman:", ["Bacon Junior", "Spyder Sammy", "Rumi"], default=["Bacon Junior"])
    ide = st.text_area("Tulis Ide Cerita:", placeholder="Contoh: Olen dikejar monster di Doors...")
    jml_adegan = st.slider("Jumlah Adegan:", 3, 10, 5)
    submit = st.button("🚀 MULAI GENERATE")

# --- 5. LOGIKA GENERASI ---
if submit:
    if not ide:
        st.error("Waduh, idenya diisi dulu dong Kak Olen!")
    else:
        with st.spinner("🤖 AI sedang memproses..."):
            try:
                # Instruksi detail visual Olen (Rambut oranye, kacamata putih, celana kodok)
                prompt_final = f"""
                Buat storyboard animasi Roblox detail.
                Karakter Utama: Olen (Anak kecil, rambut oranye, kacamata putih, baju belang oranye, celana kodok).
                Teman: {pendamping}.
                Tema: {tema}.
                Jumlah Adegan: {jml_adegan}.
                Ide Cerita: {ide}.
                
                Berikan output dalam 3 bagian (pisahkan dengan '---'):
                BAGIAN 1: Skrip & Dialog Seru.
                ---
                BAGIAN 2: Image Prompt untuk Midjourney/Leonardo.
                ---
                BAGIAN 3: Motion Prompt untuk Luma AI/Runway.
                """
                
                response = model.generate_content(prompt_final)
                
                # Memecah hasil menjadi 3 bagian
                hasil = response.text
                bagian = hasil.split('---')

                t1, t2, t3 = st.tabs(["📝 Script", "🎨 Image Prompt", "🎥 Motion Prompt"])
                
                with t1:
                    st.subheader("📜 Naskah Produksi")
                    st.write(bagian[0] if len(bagian) > 0 else hasil)
                
                with t2:
                    st.subheader("🖼️ Prompt Gambar")
                    st.code(bagian[1] if len(bagian) > 1 else "Gagal memuat prompt gambar.")
                
                with t3:
                    st.subheader("🎬 Prompt Animasi")
                    st.code(bagian[2] if len(bagian) > 2 else "Gagal memuat prompt video.")
                    
            except Exception as e:
                st.error(f"Terjadi kesalahan: {str(e)}")
                st.info("Coba cek apakah API Key di 'Secrets' sudah benar.")

