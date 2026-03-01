import streamlit as st
import google.generativeai as genai
import os

# --- 1. KONFIGURASI API ---
# Mengambil API Key dari st.secrets (untuk online) atau manual (untuk lokal)
# Pastikan API Key Kak Olen 'AIzaSyB06UXMFuJB0uEevvPVDVtAgdm_qyRAtDI' sudah benar
api_key = st.secrets.get("GEMINI_API_KEY", "AIzaSyB06UXMFuJB0uEevvPVDVtAgdm_qyRAtDI")

# PERBAIKAN: Logika diubah agar hanya error jika api_key benar-benar kosong
if not api_key:
    st.error("🔑 API Key tidak ditemukan! Masukkan API Key di Secrets atau di dalam kode.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. SETTING HALAMAN ---
st.set_page_config(page_title="Olen Roblox Studio", layout="wide")

# --- 3. UI DASHBOARD ---
col_img, col_tit = st.columns([1, 5])
with col_img:
    # Menggunakan nama file gambar yang Kak Olen miliki
    if os.path.exists("image_0.png"):
        st.image("image_0.png", use_container_width=True)
    elif os.path.exists("Charming Chibi in the Field-Photoroom.png"):
        st.image("Charming Chibi in the Field-Photoroom.png", use_container_width=True)
    else:
        st.info("🖼️ Olen Avatar")

with col_tit:
    st.title("🎬 Olen Roblox Animation Studio")
    st.write("Production Center for **@olenroblox**")

st.markdown("---")

# --- 4. SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Pengaturan Produksi")
    tema = st.selectbox("Pilih Tema:", ["Horror Survival", "Comedy Skit", "Action Adventure", "Drama Roleplay"])
    pendamping = st.multiselect("Karakter Teman:", ["Bacon Junior", "Spyder Sammy", "Rumi"], default=["Bacon Junior"])
    jml_adegan = st.slider("Jumlah Adegan:", 3, 15, 5)
    st.markdown("---")
    ide = st.text_area("Tulis Ide Cerita:", placeholder="Misal: Olen terjebak di basement sekolah...")
    submit = st.button("🚀 MULAI GENERATE", type="primary")

# --- 5. LOGIKA GENERASI & STATE ---
if "hasil_ai" not in st.session_state:
    st.session_state.hasil_ai = None

if submit:
    if not ide:
        st.error("Silakan tulis ide ceritanya dulu ya, Kak!")
    else:
        with st.spinner("🤖 AI sedang merancang naskah..."):
            try:
                # Instruksi khusus untuk karakter Olen
                prompt = f"""
                Buat storyboard Roblox detail. 
                Karakter Utama: Olen (rambut oranye, kacamata putih, baju belang, celana kodok).
                Teman: {', '.join(pendamping)}. Tema: {tema}. Adegan: {jml_adegan}.
                Ide: {ide}.
                Output: Pisahkan dengan tanda '---' untuk: 
                1. Script Cerita, 
                2. Image Prompt (AI Image Gen), 
                3. Motion Prompt (Video AI).
                """
                
                response = model.generate_content(prompt)
                st.session_state.hasil_ai = response.text
            except Exception as e:
                st.error(f"Terjadi kendala API: {str(e)}")

# --- 6. MENAMPILKAN HASIL ---
if st.session_state.hasil_ai:
    # Memastikan bagian dipisahkan dengan benar
    bagian = st.session_state.hasil_ai.split('---')
    
    t1, t2, t3 = st.tabs(["📝 Script", "🎨 Image Prompt", "🎥 Motion Prompt"])
    
    with t1:
        st.markdown(bagian[0] if len(bagian) > 0 else st.session_state.hasil_ai)
    with t2:
        st.code(bagian[1].strip() if len(bagian) > 1 else "Prompt gambar tidak tersedia")
    with t3:
        st.code(bagian[2].strip() if len(bagian) > 2 else "Prompt gerakan tidak tersedia")
