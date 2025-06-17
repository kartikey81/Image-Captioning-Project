import streamlit as st
from PIL import Image
from utils import generate_caption, text_to_speech, get_audio_html
import os

st.set_page_config(page_title="Multilingual Image Captioning", layout="centered")

st.title("🖼️ Multilingual Image Captioning with TTS")
st.markdown("Generate captions in both **English and Hindi**, and listen to them via Text-to-Speech.")

# --- Image input method
input_method = st.selectbox("Choose how to provide the image", ["Upload from device", "Capture using camera"])

image = None

if input_method == "Upload from device":
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)

elif input_method == "Capture using camera":
    captured_image = st.camera_input("Take a picture")
    if captured_image:
        image = Image.open(captured_image)

# --- Toggle sections
show_en = st.checkbox("Show English Caption + Audio", value=True)
show_hi = st.checkbox("Show Hindi Caption + Audio", value=True)

# --- Process if image is available
if image:
    st.image(image, caption="Selected Image", use_column_width=True)

    with st.spinner("Generating captions..."):
        caption_en = generate_caption(image)

        from deep_translator import GoogleTranslator
        caption_hi = GoogleTranslator(source='en', target='hi').translate(caption_en)

        st.success("Captions Generated!")

        if show_en:
            st.subheader("📄 English Caption")
            st.write(caption_en)

            with st.spinner("🔊 Generating English speech..."):
                audio_en = text_to_speech(caption_en, lang='en')
                st.markdown(get_audio_html(audio_en), unsafe_allow_html=True)

        if show_hi:
            st.subheader("📄 Hindi Caption")
            st.write(caption_hi)

            with st.spinner("🔊 Generating Hindi speech..."):
                audio_hi = text_to_speech(caption_hi, lang='hi')
                st.markdown(get_audio_html(audio_hi), unsafe_allow_html=True)

    # Cleanup temp files
    if os.path.exists("temp_audio.mp3"):
        os.remove("temp_audio.mp3")
