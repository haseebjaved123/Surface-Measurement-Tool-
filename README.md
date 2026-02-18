# Surface Measurement Tool

## Calculator (runs on GitHub)

**[→ Open the calculator](https://haseebjaved123.github.io/Surface-Measurement-Tool-/)** — surface area for **cylinder**, **rectangular**, **frustum**, **bucket**, **scoop**. No install, runs in the browser.

*If the link above doesn’t load:* In this repo go to **Settings → Pages → Source: Deploy from a branch → Branch: main, Folder: /docs → Save**. Wait 1–2 minutes, then the link will work.

---

## About

- **Calculator (this repo):** The link above runs a **static calculator** from the `docs/` folder on GitHub Pages. It works entirely in the browser.
- **Full app (OCR + calculator):** The same repo contains the **full app** (upload image → OCR dimensions → surface area). OCR needs a server, so it **does not run on GitHub**. Run it locally or deploy to Render (see below).

---

## Repository contents

| What | Where |
|------|--------|
| **Calculator (live on GitHub)** | `docs/index.html` — used by GitHub Pages |
| **Full app (server + OCR)** | `server.py`, `main.py`, `ocr_detector.py`, etc. |
| **Run full app locally** | Double‑click **RUN.bat** or run `python server.py` |
| **Deploy full app online** | [Deploy to Render (free)](https://render.com/deploy?repo=https://github.com/haseebjaved123/Surface-Measurement-Tool-) |

---

## Run the full app locally (OCR + calculator)

1. Install once: double‑click **INSTALL.bat** or run `pip install -r requirements.txt`
2. Run: double‑click **RUN.bat** (or run `python server.py`)
3. Open http://127.0.0.1:8000 — upload images for OCR and use the calculator

OCR runs only when the app is run locally or deployed to a host (e.g. Render); it does not run on GitHub Pages.

---

## Deploy the full app (with OCR) for free

**[→ Deploy to Render](https://render.com/deploy?repo=https://github.com/haseebjaved123/Surface-Measurement-Tool-)** — sign in with GitHub, click Create Web Service. You’ll get a URL like `https://surface-measurement-tool-xxxx.onrender.com`.  
Free tier may sleep after 15 min of no use; first visit after that can take 30–60 seconds.

---

## Repository structure

```
├── docs/
│   └── index.html          ← Calculator (GitHub Pages — runs on GitHub)
├── server.py               ← Full web app (Flask + OCR)
├── main.py                  ← CLI: process images with OCR
├── ocr_detector.py
├── image_preprocessor.py
├── geometry_calculator.py
├── smart_calculator.py
├── config.py
├── requirements.txt
├── RUN.bat                  ← Run full app (double‑click)
├── INSTALL.bat              ← Install dependencies
├── PUSH.bat                 ← Push this repo to GitHub
├── Procfile, Dockerfile     ← For Render / Docker deploy
├── input_images/
├── output_images/
├── processed_images/
└── results/
```

---

## Push this project to GitHub

Your repo [Surface-Measurement-Tool-](https://github.com/haseebjaved123/Surface-Measurement-Tool-) currently has only a README. To add all files and get the calculator running:

1. Open a terminal in this folder and run:
   ```bash
   git init
   git remote add origin https://github.com/haseebjaved123/Surface-Measurement-Tool-.git
   git add .
   git commit -m "Add full app and calculator"
   git branch -M main
   git push -u origin main
   ```
2. On GitHub: **Settings → Pages → Deploy from a branch → main → /docs → Save**.
3. After 1–2 minutes, the calculator will be live at: **https://haseebjaved123.github.io/Surface-Measurement-Tool-/**  

Detailed steps (no coding): see **PUSH_INSTRUCTIONS.md**. You can also double‑click **PUSH.bat** after setting the remote once.
