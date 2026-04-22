# AI Music Web

A Django web app that lets users generate AI-powered songs using the Suno API. Sign in with Google, describe your song, and get a fully generated track with lyrics and album art saved to your personal library.

---

## Features

- **Google OAuth login** via django-allauth
- **AI song generation** powered by [Suno API](https://sunoapi.org)
- **Custom song settings** — mood, genre, occasion, voice type, and optional story
- **Instrumental toggle** — generate music-only tracks with no vocals
- **Personal library** — song cards with album art, audio player, and collapsible lyrics
- **Pending song tracking** — generating songs show a "Check Status" button; page does not auto-refresh so existing songs keep playing

---

## Tech Stack

- Python 3.13 / Django 6
- Bootstrap 5 + Bootstrap Icons
- SQLite (development database)
- Suno API (external AI music generation)
- django-allauth (Google OAuth)
- Django REST Framework

---

## Prerequisites

- Python 3.10 or higher
- pip
- A [Suno API](https://sunoapi.org) key
- A Google OAuth client ID and secret (via Google Cloud Console)

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd aimusicweb
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the `aimusicweb/` directory:

```env
SUNO_API_KEY=your_suno_api_key_here
GENERATOR_STRATEGY=suno
```

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Set up Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com/) and create an OAuth 2.0 client
2. Set the redirect URI to `http://127.0.0.1:8000/accounts/google/login/callback/`
3. In Django admin (`/admin`), go to **Sites** and update the domain to `127.0.0.1:8000`
4. Go to **Social applications** → Add → select Google, enter your client ID and secret

### 7. Run the development server

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000` in your browser.

---

## How It Works

1. Sign in with your Google account
2. Click **Create Song** and fill in the form (mood, genre, occasion, etc.)
3. Submit — the app calls the Suno API and saves a pending request
4. Go to your **Library** and click **Check Status** after ~2-3 minutes
5. Once ready, the song card appears with album art, an audio player, and a lyrics panel

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SUNO_API_KEY` | Your Suno API bearer token | — |
| `GENERATOR_STRATEGY` | `suno` for real API, `mock` for offline testing | `suno` |

---

## Project Structure

```
aimusicweb/
├── apps/
│   ├── song/                  # Song model, library view
│   ├── song_gen_request/      # Generation request model, Suno API integration
│   ├── user/                  # Custom user model, auth views
│   └── shared_link/           # Shared link model
├── templates/
│   ├── layouts/base.html
│   ├── components/nav-bar.html
│   ├── home.html
│   ├── library.html
│   ├── create-song-form.html
│   └── login.html
├── static/
│   └── css/
├── aimusicweb/                # Django project settings and URLs
└── requirements.txt
```
