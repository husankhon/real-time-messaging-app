# 💬 Django Real-Time Chat App

A real-time multi-room chat application built with **Django**, **Django Channels**, and **WebSockets**. Users can register, create chat rooms, and exchange messages that appear instantly — no page refresh needed.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![Django](https://img.shields.io/badge/Django-4.2-green?logo=django)
![Channels](https://img.shields.io/badge/Channels-4.3-blueviolet)
![Daphne](https://img.shields.io/badge/Daphne-4.2-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

| Feature | Detail |
|---|---|
| 🔐 **Authentication** | Register, login, logout with Django's built-in auth |
| 💬 **Multiple chat rooms** | Create and join any number of named rooms |
| ⚡ **Real-time messaging** | WebSocket-powered — messages appear instantly for all users in the room |
| 🔒 **Secure WebSocket** | Anonymous connections are rejected at the ASGI layer |
| 📜 **Message history** | Last 50 messages loaded from the database on room entry |
| 🌑 **Dark UI** | Polished dark-theme interface with no external CSS framework required |
| 🔁 **Auto-reconnect** | Client reconnects automatically with exponential back-off on disconnect |

---

## 🗂 Project Structure

```
mysite/
├── manage.py
├── requirements.txt
├── .gitignore
│
├── mysite/                  # Django project config
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py              # ASGI entry-point (Daphne + Channels)
│   └── wsgi.py
│
└── myapp/                   # Main application
    ├── models.py            # ChatRoom, ChatMessage
    ├── views.py             # HTTP views (index, chatroom, auth)
    ├── consumers.py         # WebSocket consumer (AsyncWebsocketConsumer)
    ├── routing.py           # WebSocket URL routing
    ├── urls.py              # HTTP URL routing
    ├── admin.py             # Admin registration
    └── templates/myapp/
        ├── base.html        # Shared layout & design system
        ├── index.html       # Room listing + create-room form
        ├── room.html        # Chat UI with live WebSocket
        ├── login.html       # Login page
        └── register.html    # Registration page
```

---

## 🛠 Tech Stack

- **Backend:** Python 3.9+, Django 4.2
- **WebSocket layer:** Django Channels 4.3 + Daphne 4.2 (ASGI)
- **Channel layer:** In-memory (default) — swap for Redis in production
- **Database:** SQLite (development) — swap for PostgreSQL in production
- **Frontend:** Vanilla HTML/CSS/JS (zero external dependencies)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or later
- `pip` and `venv`

### 1 — Clone the repo

```bash
git clone https://github.com/your-username/django-realtime-chat.git
cd django-realtime-chat/mysite
```

### 2 — Create & activate a virtual environment

```bash
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### 4 — Apply migrations

```bash
python manage.py migrate
```

### 5 — Create a superuser (optional, for admin access)

```bash
python manage.py createsuperuser
```

### 6 — Run the development server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000** — it redirects to `/rooms/`.

---

## 🧭 Usage

1. **Register** an account at `/rooms/register/`
2. **Create a room** — type a name in the bar on the index page and click *Create Room*
3. **Share the URL** with friends (e.g. `http://127.0.0.1:8000/rooms/general/`)
4. **Chat in real time** — messages appear instantly for everyone in the room

---

## ⚙️ Configuration

All settings live in [`mysite/settings.py`](mysite/settings.py).

### Channel layer (default: in-memory)

The in-memory channel layer works for a **single-process** server. For multi-process or production, switch to **Redis**:

```bash
pip install channels-redis
```

```python
# settings.py
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
```

### Database (default: SQLite)

For production, replace SQLite with PostgreSQL:

```bash
pip install psycopg2-binary
```

```python
# settings.py
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "chatdb",
        "USER": "youruser",
        "PASSWORD": "yourpassword",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

### Secret key & debug

Never commit a real `SECRET_KEY`. Use environment variables:

```bash
# .env  (never commit this file)
SECRET_KEY=your-very-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
```

```python
# settings.py
import os
SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-dev-key')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
```

---

## 🌐 Deployment (production checklist)

- [ ] Set `DEBUG = False` and configure `ALLOWED_HOSTS`
- [ ] Generate a new `SECRET_KEY` and store it in an env variable
- [ ] Switch `CHANNEL_LAYERS` to Redis
- [ ] Switch `DATABASES` to PostgreSQL
- [ ] Run `python manage.py collectstatic` and serve static files via nginx
- [ ] Use **Daphne** (already installed) or **Uvicorn** behind nginx as the ASGI server
- [ ] Enable HTTPS and set `SESSION_COOKIE_SECURE = True`, `CSRF_COOKIE_SECURE = True`

---

## 🗺 URL Map

| URL | View | Description |
|---|---|---|
| `/` | redirect | Redirects to `/rooms/` |
| `/rooms/` | `index` | List all rooms; create-room form |
| `/rooms/<slug>/` | `chatroom` | Enter a specific chat room |
| `/rooms/login/` | `login_view` | Login page |
| `/rooms/logout/` | `logout_view` | POST to log out |
| `/rooms/register/` | `register_view` | Registration page |
| `/rooms/create-room/` | `create_room` | POST: create a new room |
| `/admin/` | Django admin | Manage rooms, messages, users |
| `ws://.../ws/<slug>/` | `ChatConsumer` | WebSocket endpoint |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "feat: add my feature"`
4. Push to your fork: `git push origin feature/my-feature`
5. Open a Pull Request

Please follow [conventional commits](https://www.conventionalcommits.org/) for commit messages.

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

