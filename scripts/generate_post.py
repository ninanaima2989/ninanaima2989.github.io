#!/usr/bin/env python3
"""
Robust bilingual blog generator (EN/AR)
- Resilient to Gemini downtime
- Auto retry + fallback models
- Never stops execution
"""

import os
import sys
import random
import datetime
import json
import re
import time
from pathlib import Path
from slugify import slugify
from google import genai


# ================= CONFIG =================
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("[ERROR] Missing GEMINI_API_KEY")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)

# fallback model chain (important)
MODELS = [
    os.environ.get("GEMINI_MODEL", "gemini-2.5-flash"),
    "gemini-1.5-flash-001",
    "gemini-1.5-pro-001",
]


# ================= TOPICS =================
TOPICS = {
    "AI": [
        "Large Language Models advancements",
        "Generative AI in production",
        "AI agents and autonomous systems",
    ],
    "Cybersecurity": [
        "Container and Kubernetes security",
        "Zero-trust architecture",
        "Cloud security best practices",
    ],
    "Data Science": [
        "Data visualization storytelling",
        "MLOps pipelines",
        "Time series forecasting",
    ],
}


# ================= UTIL =================
def pick_topic():
    cat = random.choice(list(TOPICS.keys()))
    topic = random.choice(TOPICS[cat])
    return cat, topic


def build_prompt(category, topic):
    return f"""
Return ONLY valid JSON.

Write a bilingual blog post (EN + AR) about: "{topic}"

Schema:
{{
  "title_en": "",
  "title_ar": "",
  "excerpt_en": "",
  "excerpt_ar": "",
  "tags": ["AI", "Tech", "Data"],
  "content_en": "",
  "content_ar": ""
}}

Requirements:
- 800–1200 words English
- Natural Arabic translation
- Include code example
"""


def clean_json(text):
    text = text.strip()
    text = re.sub(r"^```(?:json)?", "", text)
    text = re.sub(r"```$", "", text)
    return text.strip()


# ================= CORE AI CALL =================
def call_gemini(prompt):
    last_error = None

    for model in MODELS:
        for attempt in range(3):  # retry per model
            try:
                print(f"[INFO] Trying {model} (attempt {attempt+1})")

                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )

                if response and response.text:
                    return response.text

            except Exception as e:
                last_error = e
                print(f"[WARN] Model {model} failed: {e}")
                time.sleep(2 * (attempt + 1))

    raise Exception(f"All models failed. Last error: {last_error}")


# ================= FALLBACK ARTICLE =================
def fallback_article(category, topic):
    print("[FALLBACK] Generating offline article")

    return {
        "title_en": f"{topic} Overview",
        "title_ar": f"نظرة حول {topic}",
        "excerpt_en": "Generated offline due to API unavailability.",
        "excerpt_ar": "تم إنشاء المقال بدون الاتصال بـ Gemini.",
        "tags": [category, "fallback", "offline"],
        "content_en": f"## {topic}\n\nAI service is temporarily unavailable.",
        "content_ar": f"## {topic}\n\nالخدمة غير متاحة حالياً."
    }


# ================= GENERATE =================
def generate_article(category, topic):
    prompt = build_prompt(category, topic)

    try:
        raw = call_gemini(prompt)
        raw = clean_json(raw)
        return json.loads(raw)

    except Exception as e:
        print(f"[ERROR] Gemini failed completely: {e}")
        return fallback_article(category, topic)


# ================= WRITE POST =================
def write_post(article, category, lang):
    today = datetime.date.today().isoformat()
    slug = slugify(article["title_en"])[:60]

    filename = f"{today}-{slug}-{lang}.md"
    path = Path("_posts") / filename
    path.parent.mkdir(exist_ok=True)

    content = article[f"content_{lang}"]
    title = article[f"title_{lang}"]
    excerpt = article[f"excerpt_{lang}"]

    tags = "\n".join([f"  - {t}" for t in article.get("tags", [])])

    md = f"""---
layout: post
title: "{title}"
date: {today} 12:00:00 +0000
categories: [{category}]
tags:
{tags}
lang: {lang}
excerpt: "{excerpt}"
---

{content}
"""

    path.write_text(md, encoding="utf-8")
    print(f"[OK] Saved {path}")


# ================= MAIN =================
def main():
    category, topic = pick_topic()
    print(f"[INFO] Category: {category} | Topic: {topic}")

    article = generate_article(category, topic)

    required = ["title_en", "title_ar", "content_en", "content_ar"]
    for f in required:
        if f not in article:
            print(f"[WARN] Missing {f}, using fallback")
            article = fallback_article(category, topic)
            break

    write_post(article, category, "en")
    write_post(article, category, "ar")

    print("[SUCCESS] Done")


if __name__ == "__main__":
    main()
