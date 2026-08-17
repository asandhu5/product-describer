import base64

import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import ClientError, ServerError
from PIL import Image

from utils import STYLE_PROMPTS, image_to_base64, count_words, build_prompt, strip_markdown

# Free tier, no credit card required. Get a key at https://aistudio.google.com
GEMINI_MODEL = "gemini-3.6-flash"

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Product Describer",
    page_icon="🛍️",
    layout="wide"
)

# ── Session State ─────────────────────────────────────────────────────────────
if "description" not in st.session_state:
    st.session_state.description = None
if "word_count" not in st.session_state:
    st.session_state.word_count = 0
if "used_style" not in st.session_state:
    st.session_state.used_style = ""

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background-color: #f4f5f9; }
    [data-testid="stSidebar"]          { background-color: #171730; }
    [data-testid="stSidebar"] *        { color: #eaeaf5 !important; }

    /* Sidebar dropdowns (selectbox) — fix invisible white-on-white */
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background-color: #262646 !important;
        border: 1px solid #3d3d66 !important;
        border-radius: 8px !important;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] svg { fill: #eaeaf5 !important; }

    /* Dropdown option list renders in a portal outside the sidebar */
    [data-baseweb="popover"] ul { background-color: #1f1f3a !important; }
    [data-baseweb="popover"] li { color: #eaeaf5 !important; }
    [data-baseweb="popover"] li:hover { background-color: #2f2f5a !important; }

    /* Slider */
    [data-testid="stSidebar"] [data-baseweb="slider"] { padding-top: 6px; }

    .stButton > button {
        background-color: #171730;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        padding: 0.6em 1.2em;
    }
    .stButton > button:hover { background-color: #262650; border: none; }

    .description-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem 1.8rem;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        line-height: 1.75;
        color: #1a1a2e;
    }
    h1 { color: #171730; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🛍️ AI Product Description Generator")
st.caption("Upload any product image → Gemini generates a compelling description instantly")
st.divider()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    st.markdown("---")

    style = st.selectbox(
        "Description Style",
        list(STYLE_PROMPTS.keys()),
        help="Choose the platform or context for the description."
    )
    tone = st.selectbox(
        "Tone",
        ["Professional", "Friendly", "Persuasive", "Minimal"],
        help="Overall voice of the generated text."
    )
    max_words = st.slider(
        "Max Word Count",
        min_value=50, max_value=350, value=150, step=25,
        help="Approximate upper limit for description length."
    )
    st.markdown("---")
    st.markdown("**Supported Formats**")
    st.markdown("JPG · PNG · JPEG · WEBP")
    st.caption("Max file size: 16 MB")
    st.markdown("---")
    st.caption(f"Powered by Gemini ({GEMINI_MODEL}) Vision")

# ── Main Layout ───────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.subheader("📷 Product Image")
    uploaded = st.file_uploader(
        "label",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed"
    )
    if uploaded:
        image = Image.open(uploaded)
        st.image(image, use_column_width=True)
        size_kb = uploaded.size / 1024
        w, h = image.size
        st.caption(f"📁 {uploaded.name}  ·  {size_kb:.1f} KB  ·  {w}×{h} px")
    else:
        st.info("👆 Drag & drop a product image or click Browse")

with col_right:
    st.subheader("📝 Generated Description")

    if not uploaded:
        st.info("Upload a product image on the left to begin.")
    else:
        btn_col, _ = st.columns([2, 1])
        with btn_col:
            generate = st.button(
                "✨ Generate Description",
                type="primary",
                use_container_width=True
            )

        if generate:
            img_b64 = image_to_base64(image)
            prompt  = build_prompt(style, tone, max_words)

            with st.spinner("🤖 Analyzing image and writing description..."):
                try:
                    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
                    response = client.models.generate_content(
                        model=GEMINI_MODEL,
                        contents=[
                            types.Part.from_bytes(
                                data=base64.b64decode(img_b64),
                                mime_type="image/png",
                            ),
                            prompt,
                        ],
                    )
                    st.session_state.description = strip_markdown(response.text)
                    st.session_state.word_count  = count_words(st.session_state.description)
                    st.session_state.used_style  = style.split("(")[0].strip()

                except ClientError as e:
                    if e.code == 401 or e.code == 403:
                        st.error("❌ Invalid API key. Check `.streamlit/secrets.toml`.")
                    elif e.code == 429:
                        st.error("❌ Rate limit reached. Wait a moment and try again.")
                    else:
                        st.error(f"❌ Gemini API error: {e}")
                    st.session_state.description = None
                except ServerError as e:
                    st.error(f"❌ Gemini server error — usually transient, try again shortly. ({e})")
                    st.session_state.description = None
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.session_state.description = None

        if st.session_state.description:
            # Download + metrics sit above the description card, not below it.
            st.download_button(
                label="⬇️ Download as .txt",
                data=st.session_state.description,
                file_name="product_description.txt",
                mime="text/plain",
                use_container_width=True,
            )
            m1, m2, m3 = st.columns(3)
            st.divider()

            display_text = st.session_state.description.replace("\n", "<br>")
            st.markdown(
                f'<div class="description-card">{display_text}</div>',
                unsafe_allow_html=True,
            )