import os

# ✅ Fix PyTorch + Watchdog issues on Windows
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
os.environ["PYTORCH_JIT"] = "0"
os.environ["STREAMLIT_SERVER_FILE_WATCHER_TYPE"] = "none"

import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import uuid
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# ✅ MUST be first Streamlit command
st.set_page_config(page_title="🧠 Chat + Image Generator", layout="centered")

# --- Hugging Face API Token ---
API_TOKEN = "Bearer YOUR_KEY" # ADD YOUR KEY HERE
IMG_URL = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"
IMG_HEADERS = {"Authorization": API_TOKEN}

# --- Load FLAN-T5 Base (lightweight smart model) ---
@st.cache_resource
def load_text_model():
    tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
    model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
    return tokenizer, model

text_tokenizer, text_model = load_text_model()

# --- Image generation function ---
def generate_image(prompt):
    response = requests.post(IMG_URL, headers=IMG_HEADERS, json={"inputs": prompt})
    if response.status_code != 200 or "image" not in response.headers.get("content-type", ""):
        try:
            error_info = response.json()
            st.error("❌ Hugging Face API returned an error:")
            st.code(error_info, language="json")
        except Exception:
            st.error("⚠️ Hugging Face returned unexpected HTML or text.")
            st.markdown("🚧 The image server may be **down or overloaded**. Try again shortly.")
            st.code(response.text[:500] + "..." if len(response.text) > 500 else response.text, language="html")
        return None
    return Image.open(BytesIO(response.content))

# --- Text generation function ---
def generate_text(prompt):
    input_text = f"Answer clearly and helpfully: {prompt}"
    input_ids = text_tokenizer(input_text, return_tensors="pt").input_ids
    output = text_model.generate(input_ids, max_new_tokens=100)
    return text_tokenizer.decode(output[0], skip_special_tokens=True)

# --- Streamlit UI ---
st.title("🧠 AI Chat + Image Generator 🎨")
st.markdown("Ask anything and get a **smart AI answer** and a **matching AI image**.")

prompt = st.text_input("💬 What's your prompt?", placeholder="e.g. How far is the sun from Earth?")

if st.button("🚀 Generate") and prompt:
    with st.spinner("🧠 Generating smart reply..."):
        text_reply = generate_text(prompt)
        st.markdown(f"**🤖 AI says:** {text_reply}")
        st.caption("⚠️ AI-generated text may not be 100% factually accurate. Use for creative or educational purposes.")

    with st.spinner("🎨 Creating image..."):
        image = generate_image(prompt)
        if image:
            st.image(image, caption="🎨 AI-Generated Image", use_container_width=True)
            file_id = str(uuid.uuid4())
            image_path = f"image_{file_id}.png"
            image.save(image_path)
            with open(image_path, "rb") as f:
                st.download_button("⬇️ Download Image", f, file_name=image_path, mime="image/png")
