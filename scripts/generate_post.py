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
MODEL_NAME = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash-exp")
try:
    MODEL = genai.GenerativeModel(MODEL_NAME)
    print(f"[INFO] Using model: {MODEL_NAME}")
except Exception as e:
    print(f"[WARN] Failed to load {MODEL_NAME}, falling back to gemini-1.5-flash")
    MODEL = genai.GenerativeModel("gemini-1.5-flash")

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
    """Build the bilingual generation prompt"""
    return f"""You are a senior technical writer specialized in {category}.
Write a comprehensive bilingual blog post on this topic: "{topic}"

Return STRICTLY a valid JSON object (no markdown fences, no commentary) with this exact schema:

{{
  "title_en": "Catchy English title, max 70 chars",
  "title_ar": "عنوان جذاب بالعربية",
  "excerpt_en": "1-2 sentence English summary",
  "excerpt_ar": "ملخص قصير بالعربية من جملة أو جملتين",
  "tags": ["tag1", "tag2", "tag3", "tag4"],
  "content_en": "Full English Markdown article (800-1200 words) with: intro, 3-4 ## sections, at least one code example or practical example, bullet points, and a conclusion section",
  "content_ar": "نفس المقال كاملا بالعربية بنفس البنية مع عناوين ## وأمثلة عملية ونقاط رئيسية وخاتمة"
}}

Constraints:
- Use Markdown only inside content_en and content_ar fields
- Do NOT escape newlines as \\n in the Markdown content (use real newlines, the JSON encoder will handle escaping)
- Do NOT use triple backticks outside of code blocks
- The Arabic content must be fluent and natural, not a literal translation
- Include at least one practical, runnable code snippet relevant to {topic}
"""


def clean_json_response(text: str) -> str:
    """Remove potential markdown fences around JSON"""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def generate_article(category: str, topic: str) -> dict:
    """Call Gemini API and parse JSON response"""
    prompt = build_prompt(category, topic)
    response = MODEL.generate_content(
        prompt,
        generation_config={
            "temperature": 0.85,
            "max_output_tokens": 8192,
            "response_mime_type": "application/json",
        },
    )
    raw = clean_json_response(response.text)
    return json.loads(raw)


def write_post(article: dict, category: str, lang: str) -> Path:
    """Write a single-language post file"""
    today = datetime.date.today().isoformat()
    title = article[f"title_{lang}"]
    content = article[f"content_{lang}"]
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

    # Validate required fields
    required = ["title_en", "title_ar", "excerpt_en", "excerpt_ar",
                "content_en", "content_ar", "tags"]
    missing = [f for f in required if f not in article]
    if missing:
        print(f"[ERROR] Missing fields in response: {missing}")
        sys.exit(1)

    write_post(article, category, "en")
    write_post(article, category, "ar")
    print("[SUCCESS] Generation completed successfully!")


if __name__ == "__main__":
    main()

