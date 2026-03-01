import streamlit as st
import google.generativeai as genai

# Ganti baris API_KEY lama dengan ini:
API_KEY = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=MY_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="AI Story Maker", layout="wide")
st.title("🎬 My AI Story App")

# Input di samping
with st.sidebar:
    st.header("Input Cerita")
    ide = st.text_area("Tulis ide ceritamu:")
    tombol = st.button("Buat Storyboard")

# Area Tab
if tombol:
    with st.spinner("AI sedang berpikir..."):
        # Kita minta AI memberikan jawaban terstruktur
        prompt_lengkap = f"Buat storyboard singkat dari ide ini: {ide}. Pisahkan jadi: 1. Skrip, 2. Prompt Gambar, 3. Prompt Video."
        response = model.generate_content(prompt_lengkap)
        
        tab1, tab2, tab3 = st.tabs(["📝 Skrip", "🎨 Prompt Gambar", "🎥 Prompt Video"])
        
        # Penjelasan sederhana: Hasil AI kita bagi ke tab
        with tab1:
            st.write(response.text)
        with tab2:
            st.info("Gunakan ini di Midjourney/DALL-E")
            st.write(response.text)
        with tab3:
            st.info("Gunakan ini di Luma/Runway")

            st.write(response.text)
