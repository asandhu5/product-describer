import streamlit as st
import anthropic
from PIL import Image

from utils import STYLE_PROMPTS, image_to_base64, count_words, build_prompt

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
    [data-testid="stAppViewContainer"] { background-color: #f8f9fa; }
    [data-testid="stSidebar"]          { background-color: #1a1a2e; }
    [data-testid="stSidebar"] *        { color: white !important; }
    .stButton > button {
        background-color: #1a1a2e;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        padding: 0.6em 1.2em;
    }
    .stButton > button:hover { background-color: #16213e; border: none; }
    .description-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem 1.8rem;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        line-height: 1.7;
    }
    h1 { color: #1a1a2e; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🛍️ AI Product Description Generator")
st.caption("Upload any product image → Claude AI generates a compelling description instantly")
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
    st.caption("Powered by Claude claude-sonnet-4-6 Vision")

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
                    client = anthropic.Anthropic(
                        api_key=st.secrets["ANTHROPIC_API_KEY"]
                    )
                    response = client.messages.create(
                        model="claude-sonnet-4-6",
                        max_tokens=1024,
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "image",
                                        "source": {
                                            "type": "base64",
                                            "media_type": "image/png",
                                            "data": img_b64,
                                        },
                                    },
                                    {"type": "text", "text": prompt},
                                ],
                            }
                        ],
                    )
                    st.session_state.description = response.content[0].text
                    st.session_state.word_count  = count_words(st.session_state.description)
                    st.session_state.used_style  = style.split("(")[0].strip()

                except anthropic.AuthenticationError:
                    st.error("❌ Invalid API key. Check `.streamlit/secrets.toml`.")
                    st.session_state.description = None
                except anthropic.RateLimitError:
                    st.error("❌ Rate limit reached. Wait a moment and try again.")
                    st.session_state.description = None
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.session_state.description = None

        if st.session_state.description:
            st.markdown(
                f'<div class="description-card">{st.session_state.description}</div>',
                unsafe_allow_html=True,
            )
            st.markdown("&nbsp;", unsafe_allow_html=True)
            m1, m2, m3 = st.columns(3)
            m1.metric("Words",  st.session_state.word_count)
            m2.metric("Style",  st.session_state.used_style)
            m3.metric("Model",  "Sonnet 4.6")
            st.divider()
            st.download_button(
                label="⬇️ Download as .txt",
                data=st.session_state.description,
                file_name="product_description.txt",
                mime="text/plain",
                use_container_width=True,
            )
