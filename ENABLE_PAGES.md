# Enable GitHub Pages - Step by Step

The calculator link **will not work** until you enable GitHub Pages. Follow these steps:

## Steps to Enable GitHub Pages

1. **Open your repository:**
   - Go to: https://github.com/haseebjaved123/Surface-Measurement-Tool-

2. **Go to Settings:**
   - Click **Settings** tab (top of the repo page, next to "Insights")

3. **Open Pages settings:**
   - In the left sidebar, click **Pages** (under "Code and automation")

4. **Configure Pages:**
   - Under **"Build and deployment"** → **"Source"**
   - Select: **"Deploy from a branch"**
   - **Branch:** Choose `main`
   - **Folder:** Choose `/docs`
   - Click **Save**

5. **Wait:**
   - GitHub will show: "Your site is ready to be published at..."
   - Wait 1-2 minutes for the first build

6. **Test:**
   - Open: https://haseebjaved123.github.io/Surface-Measurement-Tool-/
   - You should see the calculator!

---

## Test Pages is Working

After enabling, test with:
- **Main calculator:** https://haseebjaved123.github.io/Surface-Measurement-Tool-/
- **Test page:** https://haseebjaved123.github.io/Surface-Measurement-Tool-/test.html

If both load, Pages is working correctly.

---

## Troubleshooting

**If you see 404:**
- Make sure you selected **branch: main** and **folder: /docs**
- Wait 2-3 minutes after saving
- Check that `docs/index.html` exists in your repo

**If calculator doesn't load:**
- Check browser console (F12) for errors
- Make sure JavaScript is enabled
- Try a different browser
