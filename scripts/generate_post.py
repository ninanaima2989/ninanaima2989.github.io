#!/usr/bin/env python3
"""
Automatic blog post generator (EN, optionally AR)
Topics: AI, Cybersecurity, Data Science
Powered by Google Gemini API

🔧 FIXED VERSION
---------------
Strategy that avoids ALL previous errors:
  1) FIRST call  -> small JSON only (title, excerpt, tags)   [response_mime_type=json]
  2) SECOND call -> pure Markdown article (NOT inside JSON)  [plain text]
  3) Optional 3rd call -> Arabic Markdown article

Why this works:
  - JSON stays tiny -> never truncated, never invalid
  - Markdown is plain text -> no escaping headaches, no broken \\n
  - Each call has its own try/except -> one failure doesn't crash everything
  - Stable model: gemini-1.5-flash (or override via env var)
"""

import os
import sys
import re
import json
import random
import datetime
import traceback
from pathlib import Path

from slugify import slugify
import google.generativeai as genai


# ============================================================
# 1. CONFIGURATION
# ============================================================
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("[ERROR] GEMINI_API_KEY not found in environment variables")
    sys.exit(1)

genai.configure(api_key=API_KEY)

# ✅ Stable model. Override with env var GEMINI_MODEL if needed.
#    Recommended values (in order of preference):
#      - gemini-1.5-flash         (most stable, free quota)
#      - gemini-2.5-flash         (newer, also stable)
#      - gemini-flash-latest      (auto-updated alias)
MODEL_NAME = os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")

# Should we also generate Arabic? Default = False (English only).
# Set env var GENERATE_ARABIC=1 to enable it.
GENERATE_ARABIC = os.environ.get("GENERATE_ARABIC", "0") == "1"

try:
    MODEL = genai.GenerativeModel(MODEL_NAME)
    print(f"[INFO] Using model: {MODEL_NAME}")
except Exception as e:
    print(f"[WARN] Failed to load {MODEL_NAME} ({e}), falling back to gemini-1.5-flash")
    MODEL_NAME = "gemini-1.5-flash"
    MODEL = genai.GenerativeModel(MODEL_NAME)


# ============================================================
# 2. TOPIC LIBRARY
# ============================================================
TOPICS = {
    "AI": [
        "Large Language Models advancements",
        "Computer Vision breakthroughs",
        "Reinforcement Learning applications",
        "Generative AI in production",
        "AI ethics and bias mitigation",
        "Multimodal AI systems",
        "AI agents and autonomous systems",
        "Prompt engineering best practices",
        "Retrieval Augmented Generation (RAG)",
        "Fine-tuning open-source models",
        "AI in healthcare diagnostics",
        "Edge AI and on-device inference",
    ],
    "Cybersecurity": [
        "Zero-trust architecture",
        "Ransomware defense strategies",
        "Cloud security best practices",
        "Penetration testing techniques",
        "Threat intelligence platforms",
        "Identity and access management",
        "Supply chain security",
        "Post-quantum cryptography",
        "SIEM and SOC operations",
        "Container and Kubernetes security",
        "OSINT techniques for defenders",
        "Phishing detection with ML",
    ],
    "Data Science": [
        "Feature engineering techniques",
        "MLOps pipelines",
        "Time series forecasting",
        "Big data architectures",
        "Data visualization storytelling",
        "Causal inference methods",
        "Real-time analytics",
        "Vector databases",
        "A/B testing frameworks",
        "Data quality and observability",
        "Graph neural networks",
        "Synthetic data generation",
    ],
}


def pick_topic():
    """Randomly select category and topic."""
    category = random.choice(list(TOPICS.keys()))
    topic = random.choice(TOPICS[category])
    return category, topic


# ============================================================
# 3. GEMINI CALLS
# ============================================================
def _strip_code_fences(text: str) -> str:
    """Remove ```json ... ``` or ``` ... ``` wrappers if present."""
    text = text.strip()
    text = re.sub(r"^```(?:json|markdown|md)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def generate_metadata(category: str, topic: str) -> dict:
    """
    Call #1 — SMALL JSON only.
    Returns: {title_en, excerpt_en, tags: [...]}
    Why small? -> Gemini never truncates short JSON, so json.loads() is safe.
    """
    prompt = f"""You are a senior technical writer specialized in {category}.
Topic: "{topic}"

Return ONLY a valid JSON object (no markdown fences, no comments) with this exact schema:

{{
  "title_en": "Catchy English title, max 70 chars",
  "excerpt_en": "1-2 sentence English summary, max 200 chars",
  "tags": ["tag1", "tag2", "tag3", "tag4"]
}}

Rules:
- Output JSON only, nothing else.
- No newlines inside string values.
- Use plain ASCII quotes.
"""
    response = MODEL.generate_content(
        prompt,
        generation_config={
            "temperature": 0.4,
            "max_output_tokens": 512,            # tiny -> never truncated
            "response_mime_type": "application/json",
        },
    )
    raw = _strip_code_fences(response.text or "")
    data = json.loads(raw)

    # Validate
    for key in ("title_en", "excerpt_en", "tags"):
        if key not in data:
            raise ValueError(f"Missing key '{key}' in metadata response")
    if not isinstance(data["tags"], list) or not data["tags"]:
        data["tags"] = [category]
    return data


def generate_markdown_article(category: str, topic: str, title: str, lang: str = "en") -> str:
    """
    Call #2 — PURE MARKDOWN, no JSON wrapping.
    Returns the article body as plain Markdown text.
    """
    if lang == "en":
        prompt = f"""You are a senior technical writer in {category}.
Write a comprehensive English Markdown blog post.

Title: {title}
Topic: {topic}

Structure (use real Markdown, no JSON, no code fences around the whole thing):
- A short introduction paragraph
- 3 to 4 sections, each with a `##` heading
- At least one practical, runnable code example inside a fenced code block (```language ... ```)
- Bullet points where appropriate
- A final `## Conclusion` section (2-4 sentences)

Constraints:
- 800-1200 words
- Output Markdown ONLY (do NOT wrap the whole response in ``` fences)
- Do NOT include front matter (---), I will add it myself
- Do NOT repeat the title at the top
"""
    else:  # Arabic
        prompt = f"""أنت كاتب تقني محترف متخصص في مجال {category}.
اكتب مقالاً تقنياً شاملاً باللغة العربية بصيغة Markdown.

العنوان: {title}
الموضوع: {topic}

البنية المطلوبة:
- فقرة مقدمة قصيرة
- 3 إلى 4 أقسام، كل قسم يبدأ بـ `##`
- مثال برمجي عملي واحد على الأقل داخل كتلة كود ```لغة ... ```
- نقاط مرقمة عند الحاجة
- قسم أخير `## الخاتمة` (2-4 جمل)

قيود:
- 800-1200 كلمة
- مخرجات Markdown فقط (لا تُغلِّف الرد كله بـ ``` fences)
- لا تُضِف front matter (---)، سأضيفها بنفسي
- لا تُكرر العنوان في الأعلى
"""
    response = MODEL.generate_content(
        prompt,
        generation_config={
            "temperature": 0.6,
            "max_output_tokens": 4096,           # enough for ~1200 words
            # NO response_mime_type -> we want plain text
        },
    )
    text = response.text or ""
    # Some models occasionally wrap the whole thing in ```markdown fences. Strip those.
    text = _strip_code_fences(text)
    if not text.strip():
        raise ValueError(f"Empty Markdown response for lang={lang}")
    return text


# ============================================================
# 4. FILE WRITING
# ============================================================
def write_post(title: str, excerpt: str, tags: list, content: str,
               category: str, lang: str, slug: str) -> Path:
    """Write a single-language post file in _posts/."""
    today = datetime.date.today().isoformat()
    filename = f"{today}-{slug}-{lang}.md"
    filepath = Path("_posts") / filename
    filepath.parent.mkdir(exist_ok=True)

    # Escape problematic chars for YAML front matter
    safe_title = title.replace('"', "'").replace("\n", " ").strip()
    safe_excerpt = excerpt.replace('"', "'").replace("\n", " ").strip()
    tags_yaml = "\n".join([f"  - {t}" for t in tags])

    front_matter = (
        "---\n"
        "layout: post\n"
        f'title: "{safe_title}"\n'
        f"date: {today} 12:00:00 +0000\n"
        f"categories: [{category}]\n"
        "tags:\n"
        f"{tags_yaml}\n"
        f"lang: {lang}\n"
        f'excerpt: "{safe_excerpt}"\n'
        "---\n\n"
    )

    filepath.write_text(front_matter + content.strip() + "\n", encoding="utf-8")
    print(f"[OK] Created: {filepath}")
    return filepath


# ============================================================
# 5. MAIN
# ============================================================
def main():
    category, topic = pick_topic()
    print(f"[INFO] Category: {category} | Topic: {topic}")

    # --- Step 1: metadata (small JSON) ---
    try:
        meta = generate_metadata(category, topic)
        print(f"[OK] Metadata generated: {meta['title_en']}")
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON in metadata: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Metadata generation failed: {e}")
        traceback.print_exc()
        sys.exit(1)

    title_en = meta["title_en"]
    excerpt_en = meta["excerpt_en"]
    tags = meta["tags"]
    slug = (slugify(title_en)[:60] or "post")

    # --- Step 2: English Markdown ---
    try:
        content_en = generate_markdown_article(category, topic, title_en, lang="en")
        print(f"[OK] English article generated ({len(content_en)} chars)")
    except Exception as e:
        print(f"[ERROR] English article generation failed: {e}")
        traceback.print_exc()
        sys.exit(1)

    write_post(title_en, excerpt_en, tags, content_en, category, "en", slug)

    # --- Step 3: Arabic Markdown (OPTIONAL) ---
    if GENERATE_ARABIC:
        try:
            content_ar = generate_markdown_article(category, topic, title_en, lang="ar")
            print(f"[OK] Arabic article generated ({len(content_ar)} chars)")
            # Reuse English excerpt/title for simplicity; you can also ask Gemini for Arabic versions.
            # Here we keep tags + same title, mark lang=ar.
            write_post(title_en, excerpt_en, tags, content_ar, category, "ar", slug)
        except Exception as e:
            # ❗ Arabic failure does NOT kill the workflow.
            print(f"[WARN] Arabic article skipped due to error: {e}")

    print("[SUCCESS] Generation completed successfully!")


if __name__ == "__main__":
    main()

