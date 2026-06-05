# 🤖 Automated AI · Cybersecurity · Data Science Blog

A fully automated bilingual (English + Arabic) blog that publishes one new article every day at **12:00 UTC** using Google Gemini AI and GitHub Actions.

🌐 **Live site**: https://ninanaima2989.github.io

---

## 📋 Setup Instructions (5 minutes)

### Step 1: Copy all files to your repo
Copy the entire content of this folder into your repository `ninanaima2989.github.io`.

### Step 2: Get a free Google Gemini API key
1. Go to https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Click **"Create API Key"** → copy the key

### Step 3: Add the API key as a GitHub Secret
1. Open your repo on GitHub
2. Go to **Settings → Secrets and variables → Actions**
3. Click **"New repository secret"**
4. Name: `GEMINI_API_KEY`
5. Value: paste your Gemini API key → **Add secret**

### Step 4: Enable GitHub Pages
1. Go to **Settings → Pages**
2. Under **"Build and deployment"** → Source: **GitHub Actions**
3. Save

### Step 5: Test the automation now
1. Go to the **Actions** tab on your repo
2. Click on **"📝 Daily Blog Post Generator"**
3. Click **"Run workflow"** → **Run workflow** (green button)
4. Wait 2-3 minutes
5. ✅ A new article should appear in `_posts/` and on the live site!

---

## 🔍 How to Verify It's Working

| Check | Where | Success indicator |
|-------|-------|-------------------|
| Workflow ran | Actions tab | ✅ Green checkmark |
| Article generated | `_posts/` folder | 2 new `.md` files (EN + AR) |
| Auto commit | Commits history | "🤖 Auto-post: YYYY-MM-DD" |
| Site deployed | Settings → Pages | "Your site is live at..." |
| Content visible | https://ninanaima2989.github.io | New article on homepage |
| Gemini quota | https://aistudio.google.com | < 1500 requests/day |

---

## 📁 Project Structure

```
ninanaima2989.github.io/
├── _config.yml                 # Jekyll configuration
├── Gemfile                     # Ruby dependencies
├── index.html                  # Homepage
├── about.md                    # About page
├── README.md                   # This file
├── _layouts/
│   ├── default.html            # Base layout
│   └── post.html               # Post layout
├── _posts/                     # Articles (auto-populated daily)
│   ├── 2026-06-05-welcome-en.md
│   └── 2026-06-05-welcome-ar.md
├── assets/css/style.css        # Stylesheet (RTL-aware)
├── scripts/
│   ├── generate_post.py        # AI generation script
│   └── requirements.txt        # Python dependencies
└── .github/workflows/
    └── daily-post.yml          # Automation workflow
```

---

## ⚙️ Customization

### Change publication time
Edit `.github/workflows/daily-post.yml`, line with `cron:`:
```yaml
- cron: '0 12 * * *'   # 12:00 UTC daily
- cron: '0 8 * * *'    # 08:00 UTC daily
- cron: '0 18 * * 1,3,5' # 18:00 UTC on Mon/Wed/Fri
```

### Add/edit topics
Open `scripts/generate_post.py` and modify the `TOPICS` dictionary.

### Change AI model
Edit `scripts/generate_post.py`:
```python
MODEL_NAME = "gemini-2.0-flash-exp"  # default
# or: "gemini-1.5-flash" (more stable)
# or: "gemini-1.5-pro" (higher quality but slower)
```

---

## 🐛 Troubleshooting

**Workflow fails with "GEMINI_API_KEY not found"**
→ The secret was not added. Repeat Step 3 above.

**Workflow runs but no commit appears**
→ Check the logs. Gemini may have returned invalid JSON. Re-run manually.

**Site doesn't update**
→ Verify GitHub Pages source is set to "GitHub Actions" (Step 4).

**Arabic text displays incorrectly**
→ Browsers should auto-handle RTL. Check that `lang: ar` is in the post front matter.

---

## 💡 Future Enhancements

- 🖼️ Auto-generate cover images via DALL-E or Stable Diffusion
- 🔁 Anti-duplicate check using previous post hashes
- 📱 Auto-share on Twitter/LinkedIn
- 💬 Comments via Giscus (GitHub Discussions)
- 📊 Analytics with Plausible

---

## 📜 License

MIT — feel free to fork and customize.
