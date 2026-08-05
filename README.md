# 🛍️ AI Product Description Generator

> Upload any product image → Claude AI writes a compelling description instantly.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-FF4B4B?logo=streamlit&logoColor=white)
![Claude](https://img.shields.io/badge/Claude-claude--sonnet--4--6-8B5CF6)
![Tests](https://img.shields.io/badge/Tests-33%20passed-brightgreen)

---
## 📌 What it does?

AI Product Describer is a Streamlit web app that takes a product photo and uses Claude's vision model to generate ready-to-use marketing copy — tailored to the platform and tone you choose.

Whether you're listing on Amazon, writing luxury brand prose, or drafting an Instagram caption, the app generates polished output in under 10 seconds.

---

## ▶️ HOW TO RUN  (Step by Step)

### Step 1 — Clone this repo

```bash

git clone git@github.com:asandhu5/product-describer.git
cd ai-product-describer
```

### Step 2 — Create a virtual environment

```bash
# Mac / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3 — Install all dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Add your Anthropic API key

Open the file `.streamlit/secrets.toml` and replace the placeholder:

```toml
ANTHROPIC_API_KEY = "sk-ant-your-actual-key-here"
```

Get your key from: https://console.anthropic.com/keys

### Step 5 — Run the app

```bash
streamlit run app.py
```

Your browser opens automatically at http://localhost:8501

---

## 🧪 HOW TO RUN TESTS

```bash
pytest tests/ -v
```

Expected result: **33 passed**

---

## ✨ Features

| Feature | Detail |
|---|---|
| 🖼️ **Vision-Powered** | Claude reads and understands the actual product image |
| 🎨 **4 Description Styles** | E-commerce, Luxury Brand, Technical/Detailed, Casual/Social Media |
| 🗣️ **4 Writing Tones** | Professional, Friendly, Persuasive, Minimal |
| 📏 **Word Count Control** | Slider from 50 → 350 words |
| ⬇️ **Download Output** | Export generated description as a .txt file |
| 🧪 **Unit Tests** | Full test suite, zero API calls needed |

---
## 📋 Supported Formats
JPG · JPEG · PNG · WEBP — max 16 MB

---

## 📄 License

Licensed under the **MIT License**.

---
