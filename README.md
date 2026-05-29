<div align="center">

<img src="assets/banner.png" alt="KaguneBin Banner" width="100%"/>

<br/>

# 🩸 KaguneBin

### Paste Fear. Share Power.

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-0ea5e9?style=flat-square&logo=postgresql&logoColor=white)](https://neon.tech)
[![Vercel](https://img.shields.io/badge/Deployed_on-Vercel-000000?style=flat-square&logo=vercel&logoColor=white)](https://vercel.com)
[![Status](https://img.shields.io/badge/Status-Stable-22c55e?style=flat-square)](https://kagunebin.vercel.app)

A dark-themed, developer-focused pastebin inspired by the world of Tokyo Ghoul.  
Fast. Minimal. Deadly simple.

[**Live API Docs →**](https://kagunebin.vercel.app/docs)

</div>

---

## 🩸 What is KaguneBin?

In Tokyo Ghoul, a **Kagune** is a ghoul's hidden weapon — concealed until needed, then unfolding instantly to attack, defend, and disappear.

That's exactly what a pastebin should be. Your content stays hidden until shared.

KaguneBin is a modern pastebin I built because I use paste services every single day — for code snippets, API debugging, log dumps, quick collaboration, and temporary storage. So I built my own.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📝 **Create & Share** | Instant paste creation with unique IDs |
| 🔒 **Password Protection** | Secure pastes with bcrypt hashing |
| 🔥 **Burn After Read** | Self-destructing pastes |
| ⏳ **Expiring Pastes** | Time-limited content |
| 📄 **Raw Endpoint** | Direct raw content access |
| 📊 **View Tracking** | Track how many times a paste is seen |
| 🆔 **UUID-based IDs** | Clean, unique paste identifiers |
| 📚 **Auto API Docs** | Interactive Swagger & ReDoc documentation |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Language** | ![Python](https://img.shields.io/badge/-Python_3.12-3776AB?style=flat-square&logo=python&logoColor=white) |
| **Framework** | ![FastAPI](https://img.shields.io/badge/-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white) |
| **Database** | ![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white) via ![Neon](https://img.shields.io/badge/-Neon_Serverless-0ea5e9?style=flat-square&logo=neon&logoColor=white) |
| **Validation** | ![Pydantic](https://img.shields.io/badge/-Pydantic-E92063?style=flat-square&logo=pydantic&logoColor=white) |
| **Security** | ![Passlib](https://img.shields.io/badge/-Passlib_+_bcrypt-4A4A4A?style=flat-square&logo=letsencrypt&logoColor=white) |
| **Server** | ![Uvicorn](https://img.shields.io/badge/-Uvicorn-499848?style=flat-square&logo=gunicorn&logoColor=white) |
| **Deployment** | ![Vercel](https://img.shields.io/badge/-Vercel-000000?style=flat-square&logo=vercel&logoColor=white) |

---

## 🚀 Running Locally

**1. Clone the repo**
```bash
git clone https://github.com/MKishoreDev/KaguneBin.git
cd KaguneBin
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set environment variables**
```env
DATABASE_URI=your_neon_postgresql_url
```

**4. Start the server**
```bash
uvicorn main:app --reload
```

**5. Open API docs**
```
http://localhost:8000/docs
```

---

## 🌐 Live Demo

| Interface | URL |
|---|---|
| **Swagger UI** | https://kagunebin.vercel.app/docs |
| **ReDoc** | https://kagunebin.vercel.app/redoc |

---

## 📌 Example API Response

```json
{
  "id": "kgn_a1b2c3d4",
  "title": "Example Paste",
  "content": "print('Hello World')",
  "syntax": "python",
  "is_protected": false,
  "is_burn_after_read": false,
  "views": 1,
  "created_at": "2026-05-27T12:00:00+00:00",
  "expires_at": null
}
```

---

## 🏗️ Architecture

```
KaguneBin/
├── main.py          # App entry point & route handlers
├── models.py        # Pydantic request/response models
├── config.py        # Environment configuration
├── database/
│   ├── __init__.py  # DB connection & lifespan events
│   └── funcs.py     # Reusable DB query functions
└── templates/       # HTML templates
```

---

## 🤝 Contributing

Ideas, feedback, and contributions are welcome. Open an issue or PR anytime.

---

## 📌 Note

KaguneBin is an independent developer project. Tokyo Ghoul and related characters belong to their respective creators and studios.

---

<div align="center">

Built for developers who prefer dark themes and clean APIs.

**🩸 [kagunebin.vercel.app](https://kagunebin.vercel.app)**

</div>
