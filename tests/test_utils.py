"""
tests/test_utils.py
Unit tests for utils.py — runs without Streamlit or the Anthropic API.
Run with:  pytest tests/ -v
"""

import base64
import io
import pytest
from PIL import Image

from utils import STYLE_PROMPTS, image_to_base64, count_words, build_prompt


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def rgb_image():
    """100×100 solid red RGB image."""
    return Image.new("RGB", (100, 100), color=(255, 0, 0))

@pytest.fixture
def rgba_image():
    """50×50 semi-transparent green RGBA image."""
    return Image.new("RGBA", (50, 50), color=(0, 255, 0, 128))

@pytest.fixture
def valid_style():
    return list(STYLE_PROMPTS.keys())[0]


# ── image_to_base64 ───────────────────────────────────────────────────────────

class TestImageToBase64:
    def test_returns_string(self, rgb_image):
        assert isinstance(image_to_base64(rgb_image), str)

    def test_non_empty(self, rgb_image):
        assert len(image_to_base64(rgb_image)) > 0

    def test_valid_base64(self, rgb_image):
        decoded = base64.b64decode(image_to_base64(rgb_image))
        assert len(decoded) > 0

    def test_decoded_is_valid_png(self, rgb_image):
        decoded  = base64.b64decode(image_to_base64(rgb_image))
        restored = Image.open(io.BytesIO(decoded))
        assert restored.format == "PNG"

    def test_image_dimensions_preserved(self, rgb_image):
        decoded  = base64.b64decode(image_to_base64(rgb_image))
        restored = Image.open(io.BytesIO(decoded))
        assert restored.size == rgb_image.size

    def test_rgba_converted_to_rgb(self, rgba_image):
        decoded  = base64.b64decode(image_to_base64(rgba_image))
        restored = Image.open(io.BytesIO(decoded))
        assert restored.mode == "RGB"

    def test_different_images_produce_different_output(self, rgb_image, rgba_image):
        assert image_to_base64(rgb_image) != image_to_base64(rgba_image)

    def test_large_image(self):
        large = Image.new("RGB", (1920, 1080), color=(100, 149, 237))
        assert len(image_to_base64(large)) > 0

    def test_single_pixel_image(self):
        tiny = Image.new("RGB", (1, 1), color=(0, 0, 0))
        assert isinstance(image_to_base64(tiny), str)


# ── count_words ───────────────────────────────────────────────────────────────

class TestCountWords:
    def test_simple_sentence(self):
        assert count_words("hello world") == 2

    def test_single_word(self):
        assert count_words("hello") == 1

    def test_empty_string(self):
        assert count_words("") == 0

    def test_whitespace_only(self):
        assert count_words("   ") == 0

    def test_none_returns_zero(self):
        assert count_words(None) == 0

    def test_multiline_text(self):
        assert count_words("Line one\nLine two\nLine three") == 6

    def test_extra_spaces_between_words(self):
        assert count_words("word1   word2   word3") == 3

    def test_returns_int(self):
        assert isinstance(count_words("a b c"), int)


# ── build_prompt ──────────────────────────────────────────────────────────────

class TestBuildPrompt:
    def test_returns_string(self, valid_style):
        assert isinstance(build_prompt(valid_style, "Professional", 150), str)

    def test_tone_injected(self, valid_style):
        assert "Friendly" in build_prompt(valid_style, "Friendly", 100)

    def test_max_words_injected(self, valid_style):
        assert "200" in build_prompt(valid_style, "Professional", 200)

    def test_no_leftover_placeholders(self, valid_style):
        result = build_prompt(valid_style, "Professional", 150)
        assert "{tone}"      not in result
        assert "{max_words}" not in result

    def test_all_styles_build_without_error(self):
        for style in STYLE_PROMPTS:
            assert isinstance(build_prompt(style, "Professional", 150), str)

    def test_all_styles_inject_tone(self):
        for style in STYLE_PROMPTS:
            assert "Persuasive" in build_prompt(style, "Persuasive", 150)

    def test_all_styles_inject_max_words(self):
        for style in STYLE_PROMPTS:
            assert "75" in build_prompt(style, "Minimal", 75)

    def test_invalid_style_raises_keyerror(self):
        with pytest.raises(KeyError):
            build_prompt("NonExistentStyle", "Professional", 150)

    def test_zero_max_words_raises_valueerror(self):
        with pytest.raises(ValueError):
            build_prompt(list(STYLE_PROMPTS.keys())[0], "Friendly", 0)

    def test_negative_max_words_raises_valueerror(self):
        with pytest.raises(ValueError):
            build_prompt(list(STYLE_PROMPTS.keys())[0], "Friendly", -10)


# ── STYLE_PROMPTS sanity checks ───────────────────────────────────────────────

class TestStylePrompts:
    def test_at_least_one_style(self):
        assert len(STYLE_PROMPTS) >= 1

    def test_all_styles_have_tone_placeholder(self):
        for style, template in STYLE_PROMPTS.items():
            assert "{tone}" in template, f"Missing {{tone}} in: {style}"

    def test_all_styles_have_max_words_placeholder(self):
        for style, template in STYLE_PROMPTS.items():
            assert "{max_words}" in template, f"Missing {{max_words}} in: {style}"

    def test_all_style_keys_are_strings(self):
        for key in STYLE_PROMPTS:
            assert isinstance(key, str)

    def test_all_templates_are_non_empty_strings(self):
        for style, template in STYLE_PROMPTS.items():
            assert isinstance(template, str)
            assert len(template.strip()) > 0
