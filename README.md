# 🧠 AI Chat + Image Generator 🎨

A smart Streamlit app that takes your input prompt and generates:

- 🤖 A **natural language response** using `Flan-T5` from Hugging Face
- 🎨 A **matching AI-generated image** using `Stable Diffusion v1-4`

Optimized to run on **low-spec laptops** and fully built with open-source tools.  
This is like a lightweight version of **ChatGPT + DALL·E** built by me!

---

## 📸 Demo

> _Prompt:_ `"How far is the Sun from Earth?"`  
> 🧠 **AI says:** `"The Sun is approximately 93 million miles (150 million kilometers) from Earth."`  
> 🎨 *(Matching image appears below)*

![App Screenshot](screenshot.png)

---

## 🚀 Features

- 💬 AI-generated answers using `google/flan-t5-base`
- 🎨 Visual images via Hugging Face `Stable Diffusion`
- 🧠 Streamlit-based web app (no front-end coding required)
- ✅ Error handling + download buttons
- ⚡ Optimized for low memory usage

---

## 🛠️ Tech Stack

- `Python`
- `Streamlit`
- `Hugging Face Transformers`
- `Torch`
- `Pillow`
- `requests`

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/ai-chat-image-app.git
cd ai-chat-image-app
pip install -r requirements.txt
streamlit run app.py
