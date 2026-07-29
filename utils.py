
import base64
import io
from PIL import Image



STYLE_PROMPTS: dict[str, str] = {
    "E-commerce (Amazon / Shopify)": (
        "You are an expert e-commerce copywriter. Analyze this product image carefully "
        "and write a compelling product listing structured as:\n"
        "**[Product Title]** — a catchy, keyword-rich title\n\n"
        "A powerful 1-2 sentence hook.\n\n"
        "**Key Features:**\n"
        "- Feature 1\n- Feature 2\n- Feature 3\n- Feature 4\n\n"
        "End with a short call-to-action sentence.\n\n"
        "Tone: {tone}. Keep it under {max_words} words. "
        "Only describe what you can actually see or reasonably infer from the image."
    ),
    "Luxury Brand": (
        "You are a luxury brand copywriter for a high-end retailer. "
        "Examine this product and write a sophisticated, premium description "
        "that conveys exclusivity, refined craftsmanship, and aspirational value. "
        "Use elegant, evocative language. Do not use generic filler words.\n\n"
        "Tone: {tone}. Maximum {max_words} words."
    ),
    "Technical / Detailed": (
        "You are a technical product writer. Analyze this product image carefully and produce "
        "a detailed description that covers:\n"
        "- Visible materials and build quality\n"
        "- Likely use cases and target audience\n"
        "- Key differentiating features\n"
        "- Any visible specifications\n\n"
        "Be precise and factual. Only describe what you can actually see or reasonably infer.\n\n"
        "Tone: {tone}. Maximum {max_words} words."
    ),
    "Casual / Social Media": (
        "You are a social media content creator. Write a fun, energetic Instagram caption "
        "for this product. Be conversational, enthusiastic, and relatable. "
        "Use 2-3 emojis naturally within the text — not all clumped together. "
        "End with 6-8 relevant hashtags on a new line.\n\n"
        "Tone: {tone}. Maximum {max_words} words."
    ),
}


def image_to_base64(image: Image.Image) -> str:

    buf = io.BytesIO()
    image.convert("RGB").save(buf, format="PNG")
    return base64.standard_b64encode(buf.getvalue()).decode("utf-8")


def count_words(text: str) -> int:

    if not text or not text.strip():
        return 0
    return len(text.split())


def build_prompt(style: str, tone: str, max_words: int) -> str:

    if style not in STYLE_PROMPTS:
        raise KeyError(
            f"Unknown style: '{style}'. "
            f"Valid options: {list(STYLE_PROMPTS.keys())}"
        )
    if max_words < 1:
        raise ValueError(f"max_words must be >= 1, got {max_words}")

    return STYLE_PROMPTS[style].format(tone=tone, max_words=max_words)
