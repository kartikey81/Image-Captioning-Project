import streamlit as st
from PIL import Image
from utils import generate_caption, text_to_speech, get_audio_html
import os

st.set_page_config(page_title="Multilingual Image Captioning", layout="centered")

st.title("Multilingual Image Captioning with TTS")
st.markdown("Generate captions for uploaded or captured images in **English or Hindi**, and hear them via text-to-speech.")

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

# --- Options
language = st.selectbox("Select output language", ["English", "Hindi"])
output_mode = st.radio("Select output format", ["Text", "Text + Speech"])

# --- Process image if available
if image:
    st.image(image, caption="Selected Image", use_column_width=True)

    with st.spinner("Generating caption..."):
        caption_en = generate_caption(image)
        caption = caption_en

        if language == "Hindi":
            from deep_translator import GoogleTranslator
            caption = GoogleTranslator(source='en', target='hi').translate(caption_en)

        st.success("Caption Generated!")

        if output_mode in ["Text", "Text + Speech"]:
            st.subheader("📄 Caption")
            st.write(caption)

        if output_mode == "Text + Speech":
            with st.spinner("Converting to speech..."):
                audio_file = text_to_speech(caption, lang='hi' if language == 'Hindi' else 'en')
                st.markdown(get_audio_html(audio_file), unsafe_allow_html=True)

    # Clean up
    if os.path.exists("temp_audio.mp3"):
        os.remove("temp_audio.mp3")
