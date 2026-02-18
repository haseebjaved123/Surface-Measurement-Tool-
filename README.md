# Surface Measurement Tool

> Surface area calculator for industrial shapes — **cylinder**, **rectangular**, **frustum**, **bucket**, **scoop**. No install, runs in the browser.

---

## Try the calculator

**[→ Open calculator](https://haseebjaved123.github.io/Surface-Measurement-Tool-/)** — runs on GitHub Pages, no sign-in.

*If the link doesn’t load yet:* In this repo go to **Settings → Pages → Deploy from a branch → Branch: main, Folder: /docs → Save**, then wait 1–2 minutes.

---

## What’s in this repo

| | |
|--|--|
| **Calculator (live)** | `docs/index.html` — the link above. Static, runs 100% in the browser. |
| **Full app (OCR + calculator)** | `server.py`, `main.py`, etc. Upload image → OCR detects dimensions → surface area. Needs a server (local or Render). |
| **Run full app locally** | Double‑click **RUN.bat** or run `python server.py`, then open http://127.0.0.1:8000 |
| **Deploy full app free** | [Deploy to Render](https://render.com/deploy?repo=https://github.com/haseebjaved123/Surface-Measurement-Tool-) |

---

## Run locally (full app with OCR)

1. **Install once:** Double‑click **INSTALL.bat** or run `pip install -r requirements.txt`
2. **Run:** Double‑click **RUN.bat** (or `python server.py`)
3. Open **http://127.0.0.1:8000** — upload images for OCR and use the calculator

OCR runs only when you run the app locally or deploy it (e.g. Render); it does not run on GitHub Pages.

---

## Deploy full app (with OCR) for free

**[→ Deploy to Render](https://render.com/deploy?repo=https://github.com/haseebjaved123/Surface-Measurement-Tool-)** — sign in with GitHub, create web service. Free tier may sleep after 15 min of no use.

---

## Repository structure

```
├── docs/index.html     ← Calculator (GitHub Pages)
├── server.py           ← Full web app (Flask + OCR)
├── main.py             ← CLI: process images with OCR
├── ocr_detector.py, image_preprocessor.py, geometry_calculator.py, smart_calculator.py, config.py
├── requirements.txt
├── RUN.bat             ← Run full app
├── INSTALL.bat         ← Install dependencies
├── Procfile, Dockerfile ← For Render / Docker
├── input_images/, output_images/, processed_images/, results/
```

---

## Push to GitHub

To put all files on [Surface-Measurement-Tool-](https://github.com/haseebjaved123/Surface-Measurement-Tool-):

```bash
git add .
git commit -m "Update calculator and README"
git push origin main
```

Then enable **Settings → Pages → Deploy from branch → main → /docs** so the calculator link works.
