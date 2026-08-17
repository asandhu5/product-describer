import base64
import io
import re
from PIL import Image


STYLE_PROMPTS: dict[str, str] = {
    "E-commerce (Amazon / Shopify)": (
        "You are an expert e-commerce copywriter. Analyze this product image carefully "
        "and write a compelling product listing in PLAIN TEXT ONLY — do not use markdown "
        "symbols such as **, ##, backticks, or any other formatting characters anywhere "
        "in your response.\n\n"
        "Structure it as:\n"
        "Line 1: a catchy, keyword-rich product title\n\n"
        "A powerful 1-2 sentence hook.\n\n"
        "Key Features:\n"
        "- Feature 1\n- Feature 2\n- Feature 3\n- Feature 4\n\n"
        "End with a short call-to-action sentence.\n\n"
        "Tone: {tone}. Keep it under {max_words} words. "
        "Only describe what you can actually see or reasonably infer from the image."
    ),
    "Luxury Brand": (
        "You are a luxury brand copywriter for a high-end retailer. "
        "Examine this product and write a sophisticated, premium description "
        "that conveys exclusivity, refined craftsmanship, and aspirational value. "
        "Use elegant, evocative language. Do not use generic filler words. "
        "Write in PLAIN TEXT ONLY — no markdown symbols such as **, ##, or backticks.\n\n"
        "Tone: {tone}. Maximum {max_words} words."
    ),
    "Technical / Detailed": (
        "You are a technical product writer. Analyze this product image carefully and produce "
        "a detailed description in PLAIN TEXT ONLY — no markdown symbols such as **, ##, or "
        "backticks — that covers:\n"
        "- Visible materials and build quality\n"
        "- Likely use cases and target audience\n"
        "- Key differentiating features\n"
        "- Any visible specifications\n\n"
        "Be precise and factual. Only describe what you can actually see or reasonably infer.\n\n"
        "Tone: {tone}. Maximum {max_words} words."
    ),
    "Casual / Social Media": (
        "You are a social media content creator. Write a fun, energetic Instagram caption "
        "for this product in PLAIN TEXT ONLY — no markdown symbols such as **, ##, or backticks. "
        "Be conversational, enthusiastic, and relatable. "
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


def strip_markdown(text: str) -> str:
    """Remove common markdown formatting symbols, in case the model
    emits them despite the plain-text instruction in the prompt."""
    if not text or not text.strip():
        return text or ""

    cleaned = text
    cleaned = re.sub(r"(?m)^#{1,6}\s*", "", cleaned)           # headers
    cleaned = re.sub(r"\*\*(.+?)\*\*", r"\1", cleaned)          # **bold**
    cleaned = re.sub(r"__(.+?)__", r"\1", cleaned)              # __bold__
    cleaned = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"\1", cleaned)  # *italic*
    cleaned = re.sub(r"`{1,3}(.+?)`{1,3}", r"\1", cleaned)      # `code`
    cleaned = re.sub(r"(?m)^[\*\-]\s+", "• ", cleaned)          # bullets -> •
    return cleaned.strip()


def build_prompt(style: str, tone: str, max_words: int) -> str:

    if style not in STYLE_PROMPTS:
        raise KeyError(
            f"Unknown style: '{style}'. "
            f"Valid options: {list(STYLE_PROMPTS.keys())}"
        )
    if max_words < 1:
        raise ValueError(f"max_words must be >= 1, got {max_words}")

    return STYLE_PROMPTS[style].format(tone=tone, max_words=max_words)