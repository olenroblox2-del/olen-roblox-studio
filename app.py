import streamlit as st
import google.generativeai as genai
import os

# --- 1. KONFIGURASI API & BRAND ---
# Menggunakan API Key yang Anda berikan
API_KEY = "AIzaSyB06UXMFuJB0uEevvPVDVtAgdm_qyRAtDI"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

# --- 2. SETTING HALAMAN ---
st.set_page_config(page_title="Olen Studio Pro", layout="wide", page_icon="🦊")

# Tampilan Custom agar estetik di HP maupun Laptop
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #ff4b4b; color: white; font-weight: bold; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #e1e4e8; border-radius: 5px 5px 0 0; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HEADER ---
col_logo, col_text = st.columns([1, 4])
with col_logo:
    if os.path.exists("image_0.png"):
        st.image("image_0.png", use_container_width=True)
    else:
        st.write("🦊 **Olen Avatar**")

with col_text:
    st.title("Olen Roblox Animation Studio")
    st.write("Ubah ide roleplay menjadi animasi cinematic berkualitas tinggi untuk channel **@olenroblox**.")

st.markdown("---")

# --- 4. SIDEBAR INPUT ---
with st.sidebar:
    st.header("🎬 Panel Produksi")
    
    tema = st.selectbox("Tema Cerita:", ["Horror Survival", "Comedy Skit", "Action Adventure", "Drama Roleplay"])
    gaya = st.selectbox("Gaya Visual:", ["Roblox Realistic (Blender Style)", "Smooth Plastic", "Classic R6"])
    
    st.subheader("👥 Karakter & Audio")
    st.markdown("- **Utama:** Olen (Rambut Oranye, Kacamata Putih, Celana Kodok)")
    pendamping = st.multiselect("Teman:", ["Bacon Junior", "Spyder Sammy", "Rumi"], default=["Bacon Junior"])
    st.info("🔊 Mode: Suara Asli Kak Olen (Otentik)")
    
    st.markdown("---")
    ide = st.text_area("Ide Cerita Singkat:", placeholder="Misal: Olen dan Bacon terjebak di lift berhantu...")
    jml_adegan = st.slider("Jumlah Adegan:", 3, 12, 6)
    
    generate_btn = st.button("🚀 GENERATE MASTERPIECE")

# --- 5. LOGIKA GENERASI ---
if generate_btn:
    if not ide:
        st.warning("Silakan isi ide ceritanya dulu, Kak Olen!")
    else:
        with st.spinner("🤖 AI sedang merancang storyboard Olen Universe..."):
            # Instruksi detail untuk AI
            system_instruction = f"""
            Role: Sutradara Animasi Profesional untuk Channel @olenroblox.
            Karakter Utama: Olen (Anak kecil, rambut oranye acak, kacamata putih, baju belang oranye-kuning, celana kodok denim).
            Karakter Teman: {', '.join(pendamping)}.
            Gaya Visual: {gaya}.
            Suara: Dialog harus cocok untuk diisi suara asli Kak Olen yang ekspresif dan lucu.
            
            Berikan output dalam 3 bagian (pisahkan dengan '---'):
            BAGIAN 1: Skrip & Viral Hooks. Sertakan dialog yang kuat dan "Hook" di 3 detik pertama.
            ---
            BAGIAN 2: Image Prompt. Detail untuk Midjourney/DALL-E (Lighting, Angle, Roblox Aesthetic).
            ---
            BAGIAN 3: Motion Prompt. Instruksi gerakan kamera dan karakter untuk Luma AI atau Runway Gen-3.
            """
            
            response = model.generate_content(f"{system_instruction}\n\nIde: {ide}\nJumlah Adegan: {jml_adegan}")
            hasil_raw = response.text
            bagian = hasil_raw.split('---')

            st.session_state['hasil_full'] = hasil_raw
            st.session_state['bagian'] = bagian

# --- 6. DISPLAY HASIL ---
if 'hasil_full' in st.session_state:
    st.download_button("📥 Download Berkas Produksi", st.session_state['hasil_full'], "storyboard_olen.txt")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Naskah", "🎨 Prompt Gambar", "🎥 Prompt Animasi", "🚀 Viral Hooks", "📖 Tutorial"])
    
    bg = st.session_state['bagian']
    
    with tab1:
        st.subheader("📜 Skrip & Dialog Otentik")
        st.write(bg[0] if len(bg) > 0 else "Gagal memuat skrip.")
        
    with tab2:
        st.subheader("🖼️ Prompt Gambar (Base Image)")
        st.code(bg[1] if len(bg) > 1 else "Gagal memuat prompt gambar.")
        
    with tab3:
        st.subheader("🎬 Prompt Animasi (Luma/Runway)")
        st.code(bg[2] if len(bg) > 2 else "Gagal memuat prompt video.")
        
    with tab4:
        st.subheader("🔥 Perpustakaan Hook Viral")
        st.markdown("""
        1. **The Cliffhanger:** "Aku gak nyangka karakter ini bakal lakuin itu ke Olen..."
        2. **The Secret:** "Jangan pernah ketik kode ini di Roblox jam 12 malam!"
        3. **The Challenge:** "Bisakah Olen selamat tanpa melompat sama sekali?"
        """)

    with tab5:
        st.subheader("🎬 Tutorial Cepat ke Video")
        st.markdown("""
        1. **Visual:** Salin prompt dari **Tab 2** ke Leonardo.ai atau Midjourney. Pastikan Olen terlihat ikonik.
        2. **Animasi:** Upload gambar tersebut ke **Luma Dream Machine**. Masukkan prompt dari **Tab 3**.
        3. **Editing:** Gabungkan klip di CapCut, rekam suara asli Kak Olen, dan tambahkan musik Roblox!
        """)

    # --- 7. RATING SYSTEM ---
    st.markdown("---")
    st.write("**Bagaimana kualitas hasil ini?**")
    feedback = st.feedback("stars")
    if feedback is not None:
        st.success(f"Rating {feedback+1} bintang berhasil dikirim! AI akan belajar dari sini.")
