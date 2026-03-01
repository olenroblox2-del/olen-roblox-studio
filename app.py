import streamlit as st
import google.generativeai as genai
import os

# --- 1. KONFIGURASI API ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = "AIzaSyB06UXMFuJB0uEevvPVDVtAgdm_qyRAtDI"

genai.configure(api_key=API_KEY)

# Gunakan model paling stabil untuk Free Tier
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# --- 2. SETTING HALAMAN ---
st.set_page_config(page_title="Olen Roblox Studio", layout="wide")

# --- 3. TAMPILAN DASHBOARD (GAMBAR & JUDUL) ---
col_img, col_tit = st.columns([1, 5])
with col_img:
    # Mencoba mencari file gambar dengan nama yang tepat
    if os.path.exists("Charming Chibi in the Field-Photoroom.png"):
        st.image("Charming Chibi in the Field-Photoroom.png", use_container_width=True)
    else:
        # Jika file tidak ditemukan, kita tampilkan teks pengganti agar tidak blank
        st.warning("🖼️ Foto Avatar Belum Terbaca")

with col_tit:
    st.title("🎬 Olen Roblox Animation Studio")
    st.write("Production Center for **@olenroblox**")

st.markdown("---")

# --- 4. SIDEBAR (SEMUA MENU KEMBALI DI SINI) ---
with st.sidebar:
    st.header("⚙️ Pengaturan Produksi")
    
    # Menampilkan kembali menu yang sempat hilang
    tema = st.selectbox("Pilih Tema:", ["Horror Survival", "Comedy Skit", "Action Adventure", "Drama Roleplay"])
    
    pendamping = st.multiselect("Karakter Teman:", 
                                ["Bacon Junior", "Spyder Sammy", "Rumi"], 
                                default=["Bacon Junior"])
    
    jml_adegan = st.slider("Jumlah Adegan:", 3, 15, 5)
    
    st.markdown("---")
    ide = st.text_area("Tulis Ide Cerita:", placeholder="Misal: Olen terjebak di basement sekolah...")
    
    submit = st.button("🚀 MULAI GENERATE", type="primary")

# --- 5. LOGIKA GENERASI ---
if submit:
    if not ide:
        st.error("Silakan tulis ide ceritanya dulu ya, Kak!")
    else:
        with st.spinner("🤖 AI sedang merancang naskah..."):
            try:
                # Instruksi detail visual Olen
                prompt = f"""
                Buat storyboard Roblox detail. 
                Karakter Utama: Olen (rambut oranye, kacamata putih, baju belang, celana kodok).
                Teman: {', '.join(pendamping)}. Tema: {tema}. Adegan: {jml_adegan}.
                Ide: {ide}.
                Output: Pisahkan dengan '---' untuk: 1. Script, 2. Image Prompt, 3. Motion Prompt.
                """
                
                response = model.generate_content(prompt)
                hasil = response.text
                bagian = hasil.split('---')

                # Menampilkan hasil dalam Tab agar rapi
                t1, t2, t3 = st.tabs(["📝 Script", "🎨 Image Prompt", "🎥 Motion Prompt"])
                with t1: st.write(bagian[0] if len(bagian) > 0 else hasil)
                with t2: st.code(bagian[1] if len(bagian) > 1 else "N/A")
                with t3: st.code(bagian[2] if len(bagian) > 2 else "N/A")
                
            except Exception as e:
                st.error(f"Terjadi kendala: {str(e)}")
