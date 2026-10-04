<div align="center">

<img src="assets/banner.png" alt="KaguneBin Banner" width="100%"/>

<br/>

# 🩸 KaguneBin

### Paste Fear. Share Power.

[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-0ea5e9?style=flat-square&logo=postgresql&logoColor=white)](https://neon.tech)
[![PyPI](https://img.shields.io/badge/PyPI-v1.0.1-blue?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/kagunebin/)
[![Vercel](https://img.shields.io/badge/Deployed_on-Vercel-000000?style=flat-square&logo=vercel&logoColor=white)](https://kagunebin.vercel.app)
[![License](https://img.shields.io/badge/License-MIT-crimson?style=flat-square)](LICENSE)

A dark-themed, developer-focused pastebin inspired by the world of Tokyo Ghoul.  
Fast. Minimal. Deadly simple.

[**🌐 Web App**](https://kagunebin.vercel.app) • [**📚 Interactive API Docs**](https://kagunebin.vercel.app/docs) • [**📦 Python SDK**](https://pypi.org/project/kagunebin/)

</div>

---

## 🩸 What is KaguneBin?

In Tokyo Ghoul, a **Kagune** is a ghoul's predatory organ and weapon — concealed until needed, then unfolding instantly to attack, defend, and disappear.

That's exactly what a modern pastebin should be. Your content stays concealed and secure until you share it.

KaguneBin is an anonymous, developer-first paste service built for fast code sharing, log dumps, API debugging, and secret distribution.

---

## ✨ Core Features

| Feature | Description |
|---|---|
| 📝 **Create & Share** | Instant paste creation with unique IDs (`kgn_...`) |
| 🔒 **Password Protection** | Zero-trust password protection hashed with bcrypt |
| 🔥 **Burn After Read** | Self-destructing pastes deleted on first read or download |
| ⏳ **Expiring Pastes** | Automated expiration (hours, days, or custom timestamp) |
| 📄 **Raw Content** | Direct plaintext endpoint (`/raw/:id`) for `curl` & automation |
| 📥 **File Downloads** | One-click downloads with automatic syntax extension mapping |
| 📊 **Real-time Analytics** | Live view count and download counters |
| 🛡️ **CORS & Rate Safety** | Full CORS support for external integrations and bots |
| 📚 **Interactive Docs** | Built-in Swagger (`/api/docs`), ReDoc (`/api/redoc`), and Docs UI (`/docs`) |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Framework** | [FastAPI](https://fastapi.tiangolo.com) (Python 3.11 / 3.12) |
| **Database** | [PostgreSQL](https://postgresql.org) via [Neon Serverless](https://neon.tech) |
| **Driver & Pooling** | `psycopg` 3.x with connection validation |
| **Validation** | [Pydantic v2](https://docs.pydantic.dev) |
| **Security** | `bcrypt` password hashing with SHA-256 pre-hashing |
| **Frontend** | Vanilla HTML5, CSS3, JavaScript, Highlight.js |
| **Hosting** | Vercel Serverless Functions |

---

## 🚀 Running Locally

**1. Clone the repository**
```bash
git clone https://github.com/MKishoreDev/KaguneBin.git
cd KaguneBin
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set environment variables**
```bash
cp .env.example .env
# Edit .env with your Neon PostgreSQL URI
```

**4. Start the development server**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**5. Access the services**
- Web UI: `http://localhost:8000`
- Documentation: `http://localhost:8000/docs`
- OpenAPI Swagger: `http://localhost:8000/api/docs`

---

## 📦 Python SDK Quickstart

Install the official Python SDK:

```bash
pip install kagunebin
```

```python
from kagunebin import KaguneBin

# Initialize client
kb = KaguneBin()

# Create a paste
paste = kb.create(
    title="Main Server Log",
    content="[INFO] System initialized successfully.",
    syntax="bash",
    expires_in_hours=24
)

print(f"Paste URL: https://kagunebin.vercel.app{paste['url']}")
```

---

## 📌 API Endpoints Overview

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Web application home |
| `GET` | `/p/{id}` | Web view for paste |
| `GET` | `/docs` | Custom documentation page |
| `GET` | `/status` / `/health` | Service health status |
| `POST` | `/paste` | Create new paste |
| `GET` | `/api/paste/{id}` | Fetch paste JSON payload |
| `GET` | `/raw/{id}` | Fetch raw plaintext content |
| `GET` | `/download/{id}` | Stream file download |

---

## 🏗️ Project Architecture

```
KaguneBin/
├── assets/                  # Logos, banners, visual assets
├── database/
│   ├── __init__.py          # Connection management & schema creation
│   └── funcs.py             # Database CRUD helper queries
├── templates/
│   ├── index.html           # Homepage & paste creation UI
│   ├── paste.html           # Paste viewing & syntax rendering UI
│   ├── docs.html            # Interactive documentation UI
│   └── 404.html             # Custom 404 error page
├── .env.example             # Environment variable template
├── .gitignore               # Git ignore rules
├── config.py                # Environment configuration
├── main.py                  # FastAPI application entry point
├── models.py                # Pydantic v2 schemas
├── requirements.txt         # Production dependencies
├── vercel.json              # Vercel serverless routing
└── LICENSE                  # MIT License
```

---

## 📄 License

MIT License © 2026 **Kishore M**

---

<div align="center">

Built with passion by **[Kishore M](https://github.com/MKishoreDev)**.

**🩸 [kagunebin.vercel.app](https://kagunebin.vercel.app)**

</div>
