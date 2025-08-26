# ⚽ Soccer Tracker – Web App (Accounts, Types, Friends & Leaderboard)

A Flask app to log soccer training minutes by **type**, earn points, and climb ranks. Points **decay** if you don't train (5 pts/day after your last log). Create an account, add friends, and compare on a leaderboard.

## Features
- Email/password **signup & login**
- Log training minutes with **type** + optional notes
- **Ranks** with progress bar (Beginner → Soccer God)
- **Weekly minutes** chart + **Minutes by Type** chart
- Points **decay** if you miss days (5 pts/day since your last log)
- **Friends** (add by email) and **Leaderboard** (global + friends)

## Local Setup (Mac/Windows/Linux)
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

> If you ran a previous version: delete `app.db` once to recreate the database with new columns (`kind`, friends table).

## Free Deploy on Render — Step by Step
1. **Create a GitHub repo** and push this folder.
2. Go to **render.com** → **New** → **Web Service** → connect your repo.
3. Fill in:
   - **Runtime:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
4. **Environment Variables** (Settings → Environment):
   - `SECRET_KEY` = any random string (e.g. from https://randomkeygen.com)
   - _(Optional but recommended)_ **Persistent DB**: add a **Render PostgreSQL** instance (Free) and copy its `DATABASE_URL` into your service's environment.
     - If you skip Postgres, SQLite will reset when the instance redeploys.
5. Click **Deploy**. On first boot, the app auto-creates tables.
6. Open the URL → create an account → start logging.
7. Share the URL with friends; they create accounts and you can add them by email on the **Friends** page.

## Switching DB later (from SQLite to Postgres)
- Add a Postgres instance in Render.
- Set the service env var `DATABASE_URL` to the Postgres URL.
- Redeploy. The app will create tables in Postgres automatically.

## Files
```
app.py
requirements.txt
templates/
  base.html
  landing.html
  login.html
  register.html
  dashboard.html
  friends.html
  leaderboard.html
static/
README.md
```

## Notes
- For real migrations across versions, consider **Flask-Migrate** later.
- Leaderboard points are computed live from logs + decay, so recent inactivity reduces your score automatically.
