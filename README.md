# 🛍️ AI Product Description Generator

> Upload any product image → Claude AI writes a compelling description instantly.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-FF4B4B?logo=streamlit&logoColor=white)
![Claude](https://img.shields.io/badge/Claude-claude--sonnet--4--6-8B5CF6)
![Tests](https://img.shields.io/badge/Tests-33%20passed-brightgreen)

---

## 📁 Folder Structure

```
ai-product-describer/
├── app.py                    ← Streamlit UI
├── utils.py                  ← All business logic (testable)
├── requirements.txt          ← Python dependencies
├── secrets.toml.example      ← Template for your API key
├── .gitignore                ← Hides secrets and cache
└── .streamlit/
    ├── config.toml           ← Theme and upload size
    └── secrets.toml          ← Your actual API key (never pushed)
└── tests/
    ├── __init__.py
    ├── conftest.py
    └── test_utils.py         ← 33 unit tests
```

---

## ▶️ HOW TO RUN LOCALLY (Step by Step)

### Step 1 — Open terminal in this folder

```bash
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

You will see `(venv)` appear at the start of your terminal line.

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

## 🐙 HOW TO PUSH TO GITHUB

### Step 1 — Create a new repo on GitHub
1. Go to https://github.com/new
2. Name: `ai-product-describer`
3. Set to **Public**
4. Do NOT check "Add README"
5. Click **Create repository**

### Step 2 — Push from your terminal

```bash
git init
git add .
git commit -m "Initial commit: AI Product Describer"
git remote add origin https://github.com/YOUR_USERNAME/ai-product-describer.git
git branch -M main
git push -u origin main
```

---

## ☁️ HOW TO DEPLOY ON STREAMLIT CLOUD (Free Live Link)

1. Go to https://share.streamlit.io and sign in with GitHub
2. Click **New app**
3. Select your repo: `YOUR_USERNAME/ai-product-describer`
4. Branch: `main` | Main file: `app.py`
5. Click **Advanced settings** → paste in **Secrets**:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-your-actual-key-here"
   ```
6. Click **Deploy** — live in ~2 minutes

---

## 🔄 How to Update After Changes

```bash
git add .
git commit -m "What you changed"
git push
```

Streamlit Cloud redeploys automatically.
