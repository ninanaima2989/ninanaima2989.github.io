#!/usr/bin/env python3
"""
Automatic bilingual (EN/AR) blog post generator
Topics: AI, Cybersecurity, Data Science
Powered by Google Gemini API
"""
import os
import sys
import random
import datetime
import json
import re
from pathlib import Path
from slugify import slugify
import google.generativeai as genai

# ===== Configuration =====
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("[ERROR] GEMINI_API_KEY not found in environment variables")
    sys.exit(1)

genai.configure(api_key=API_KEY)

# Use stable model with fallback
MODEL_NAME = os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")
try:
    MODEL = genai.GenerativeModel(MODEL_NAME)
    print(f"[INFO] Using model: {MODEL_NAME}")
except Exception as e:
    print(f"[WARN] Failed to load {MODEL_NAME}, falling back to gemini-1.5-flash")
    MODEL = genai.GenerativeModel("gemini-2.5-flash")
# ===== Topic library =====
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
    """Randomly select category and topic"""
    category = random.choice(list(TOPICS.keys()))
    topic = random.choice(TOPICS[category])
    return category, topic


def build_prompt(category: str, topic: str) -> str:
    return f"""
You are a senior technical writer.

Write ONLY a valid JSON object with NO markdown, NO extra text.

Return this structure ONLY:

{{
  "title_en": "...",
  "title_ar": "...",
  "excerpt_en": "...",
  "excerpt_ar": "...",
  "tags": ["tag1", "tag2", "tag3"]
}}

Topic: {topic}
Category: {category}

Rules:
- No long articles
- No content field
- JSON only
"""


def clean_json_response(text: str) -> str:
    """Remove potential markdown fences around JSON"""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def write_post(article: dict, category: str, lang: str) -> Path:
    today = datetime.date.today().isoformat()

    title = article[f"title_{lang}"]
    excerpt = article[f"excerpt_{lang}"]
    content = article["content_en"] if lang == "en" else article["content_ar"]

    slug = slugify(article["title_en"])[:60] or "post"

    filename = f"{today}-{slug}-{lang}.md"
    filepath = Path("_posts") / filename
    filepath.parent.mkdir(exist_ok=True)

    safe_title = title.replace('"', "'").replace("\n", " ")
    safe_excerpt = excerpt.replace('"', "'").replace("\n", " ")

    tags_yaml = "\n".join([f"  - {t}" for t in article.get("tags", [])])

    front_matter = f"""---
layout: post
title: "{safe_title}"
date: {today} 12:00:00 +0000
categories: [{category}]
tags:
{tags_yaml}
lang: {lang}
excerpt: "{safe_excerpt}"
---

{content}
"""

    filepath.write_text(front_matter, encoding="utf-8")
    print(f"[OK] Created: {filepath}")
    return filepath

def generate_content(category: str, topic: str, lang: str) -> str:
    prompt = f"""
Write a detailed blog post in {lang} about: {topic}

Rules:
- 600 to 800 words
- Include sections with ##
- Include one code example if relevant
- Do NOT output JSON
- Only plain Markdown text
"""

    response = MODEL.generate_content(prompt)
    return response.text
     
def write_post(article: dict, category: str, lang: str) -> Path:
    """Write a single-language post file"""
    today = datetime.date.today().isoformat()
    title = article[f"title_{lang}"]
    content = article["content_en"] if lang == "en" else article["content_ar"]
    excerpt = article[f"excerpt_{lang}"]
    slug = slugify(article["title_en"])[:60] or "post"

    filename = f"{today}-{slug}-{lang}.md"
    filepath = Path("_posts") / filename
    filepath.parent.mkdir(exist_ok=True)

    # Escape quotes for YAML
    safe_title = title.replace('"', "'").replace("\n", " ")
    safe_excerpt = excerpt.replace('"', "'").replace("\n", " ")

    tags_yaml = "\n".join([f"  - {t}" for t in article.get("tags", [])])

    front_matter = f"""---
layout: post
title: "{safe_title}"
date: {today} 12:00:00 +0000
categories: [{category}]
tags:
{tags_yaml}
lang: {lang}
excerpt: "{safe_excerpt}"
---

{content}
"""
    filepath.write_text(front_matter, encoding="utf-8")
    print(f"[OK] Created: {filepath}")
    return filepath


def main():

    category, topic = pick_topic()
    print(f"[INFO] Category: {category} | Topic: {topic}")

    try:
        article = generate_article(category, topic)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON from Gemini: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Gemini API call failed: {e}")
        sys.exit(1)

    content_en = generate_content(category, topic, "English")
    content_ar = generate_content(category, topic, "Arabic")

    write_post(article | {"content_en": content_en, "content_ar": content_ar}, category, "en")
    write_post(article | {"content_en": content_en, "content_ar": content_ar}, category, "ar")

    print("[SUCCESS] Generation completed successfully!")

if __name__ == "__main__":
    main()
