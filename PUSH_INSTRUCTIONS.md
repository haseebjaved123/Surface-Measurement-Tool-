# How to push to GitHub (no coding needed)

I can’t push to GitHub from here — only you can, because it’s your account. Follow these steps once to get the app online.

---

## Step 1: Install Git (if you don’t have it)

1. Go to **https://git-scm.com/download/win**
2. Download and run the installer. Keep the default options and click Next until it finishes.

---

## Step 2: Open your project folder in Terminal

1. In File Explorer, go to your project folder: **OCR Tool 2 - git**
2. Click the **address bar** at the top (where it shows the path), type **cmd** and press **Enter**.  
   A black window (Command Prompt) will open in that folder.

---

## Step 3: Run these 3 commands (copy and paste one at a time)

**First time only** — tell Git where your GitHub repo is:

```
git remote add origin https://github.com/haseebjaved123/Surface-Measurement-Tool-.git
```

(If it says "already exists", that’s fine — skip to the next.)

**Then every time you want to update the site**, run these three:

```
git init
git add .
git commit -m "Update app"
git push -u origin main
```

When you run `git push`, Windows may ask you to sign in. Use your **GitHub username** and a **Personal Access Token** (not your normal password):

- To create a token: GitHub.com → your profile (top right) → **Settings** → **Developer settings** → **Personal access tokens** → **Generate new token**. Give it a name, tick **repo**, then generate and **copy the token**. Paste it when the command line asks for a password.

---

## Step 4: Turn on GitHub Pages

1. Open **https://github.com/haseebjaved123/Surface-Measurement-Tool-**
2. Click **Settings** → **Pages** (left sidebar).
3. Under **Source**, choose **Deploy from a branch**.
4. Branch: **main**, Folder: **/docs**.
5. Click **Save**.

After 1–2 minutes your app will be live at:

**https://haseebjaved123.github.io/Surface-Measurement-Tool-/**

---

**Summary:** You only need to do Step 1 and Step 2 once. Step 3 you run whenever you want to update the site. Step 4 you do once to make the site public.
