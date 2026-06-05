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
if no
