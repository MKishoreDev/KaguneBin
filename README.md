<div align="center">

<img src="assets/banner.png" alt="KaguneBin Banner"/>

<br>

# 🩸 KaguneBin

### Paste Fear. Share Power.

A dark-themed modern pastebin inspired by the world of Tokyo Ghoul.

Fast. Minimal. Developer-focused.

</div>

---

## 📖 About The Project

After building [Redirox](https://github.com/MKishoreDev/Redirox), my URL shortener project, I wanted to build something I actually use almost every day.

I constantly use pastebin services for:
- sharing code snippets
- debugging APIs
- temporary storage
- logs
- testing responses
- quick collaboration

Then I thought:

> “Why not build my own pastebin?”

At the same time, I was rewatching Tokyo Ghoul and the entire aesthetic instantly matched the vision I had in mind.

That’s how **KaguneBin** was born.

---

## 🩸 Why "KaguneBin"?

In Tokyo Ghoul, a **Kagune** is a ghoul's hidden weapon.

It stays concealed until needed and can:
- unfold instantly
- attack
- defend
- disappear seamlessly

That concept perfectly matched a pastebin.

Your content stays hidden until shared.

Minimal.  
Fast.  
Deadly simple.

---

## ⚔️ Current Development Status

KaguneBin has now moved beyond the early prototype phase.

The backend API is fully functional and currently includes:

- ⚡ FastAPI backend
- 🗄 PostgreSQL database integration
- 🔐 Password-protected pastes
- 🔥 Burn-after-read pastes
- ⏳ Expiring pastes
- 📄 Raw paste endpoints
- 📊 View tracking
- 🧠 Structured JSON responses
- 📚 Automatic Swagger/OpenAPI documentation
- 🔑 Secure password hashing using bcrypt
- 🆔 UUID-based paste generation

The biggest recent upgrade was moving from a temporary in-memory Python dictionary database to a proper PostgreSQL setup.

Right now the main thing pending is the HTML frontend UI, which will be added later once the backend architecture is finalized properly.

A few developer-focused endpoints and testing features currently exist for debugging and development purposes and may be removed before the public release version.

---

## 🌐 Live Demo

### API Documentation

- Swagger UI:
```bash
https://kagunebin.vercel.app/docs
```

- ReDoc:
```bash
https://kagunebin.vercel.app/redoc
```

> Public deployment URL will be added later.

---

## 🧠 What I'm Learning From This Project

KaguneBin became much more than just “building a pastebin.”

For a long time I used Flask for almost everything and genuinely thought:

> “FastAPI and Flask are basically just two different packages for APIs.”

But after building a real project using FastAPI, I finally understood why FastAPI exists and what problems it actually solves.

While building KaguneBin, I started learning:
- asynchronous API architecture
- request validation with Pydantic
- scalable backend design
- structured response models
- OpenAPI standards
- reusable backend architecture
- password hashing & security handling
- database-driven systems
- lifecycle events in FastAPI
- production-oriented API structure

One of the biggest mindset changes came from moving away from:

> “Just make it work.”

towards:

> “Understand why systems are designed this way.”

---

## 🔄 From Random Codes To UUIDs

One thing I changed during development was how paste IDs are generated.

Earlier, I used a random generator like this:

```python
def generate_code():
    values = string.ascii_letters + string.digits

    while True:
        code = "".join(random.choices(values, k=6))
        exist = db.links.find_one({"code": code})

        if not exist:
            return code
```

It worked, but I slowly realized:
- collisions still needed manual checking
- generation logic became repetitive
- scaling this approach would become annoying later

After learning more about backend architecture and scalable systems, I switched to UUID-based IDs instead:

```python
paste_id = f"kgn_{uuid4().hex[:8]}"
```

This simplified the system significantly and made the codebase cleaner and easier to maintain.

It also helped me better understand:
- uniqueness guarantees
- scalable identifier generation
- cleaner backend patterns
- why modern systems often prefer UUIDs

---

## 🗄 Database Journey

KaguneBin originally started with a temporary Python dictionary database while I focused on understanding the API architecture first.

Now the project has been migrated to a proper PostgreSQL-based setup.

This transition taught me a lot about:
- persistent storage
- schema design
- API-to-database interaction
- scalable backend systems
- structured queries
- production-oriented architecture

Interestingly, I had used SQL years ago in older projects without really understanding what databases were actually solving.

This project finally gave me a chance to revisit databases properly and understand them from a backend engineering perspective instead of just “saving data somewhere.”

---

## 🧩 API Structure

The backend currently uses:
- FastAPI lifespan events
- reusable database functions
- Pydantic request/response models
- UTC timezone handling
- structured API responses
- password hashing using bcrypt
- PostgreSQL persistence
- UUID-based paste IDs

The architecture is intentionally separated into:
- models
- database layer
- reusable database functions
- route handlers
- utility logic

This made the codebase significantly cleaner and easier to maintain compared to how I previously structured backend projects.

---


## ✨ Current Features

- 📝 Create & share pastes
- 🔒 Password-protected pastes
- ⏳ Expiring pastes
- 🔥 Burn-after-reading pastes
- 📄 Raw content endpoint
- 📊 View tracking
- 🧠 Structured JSON responses
- 📚 Interactive API documentation
- ⚡ Fast paste retrieval
- 🗄 PostgreSQL storage
- 🔑 Secure password hashing
- 🆔 UUID-based paste IDs

---

## 🚧 Planned Features

- 🎨 Syntax highlighting UI
- 🌑 Full dark-themed frontend
- 📱 Responsive interface
- 🔗 Public share pages
- 📦 PyPI wrapper package
- 🧹 Cleanup system for expired pastes
- 🩸 Advanced Tokyo Ghoul-inspired branding
- 📋 Copy/share utilities
- 🌐 Public deployment

---

## 🧪 Development Philosophy

I don't want KaguneBin to become another bloated platform overloaded with unnecessary features.

The goal is simple:

> A fast, clean, stylish place to instantly share code.

---

## 🛠 Tech Stack

### Current Stack

- FastAPI
- Python
- PostgreSQL
- Pydantic
- Passlib
- bcrypt
- Uvicorn
---

## 🚀 Running Locally

### Clone the repository

```bash
git clone https://github.com/MKishoreDev/KaguneBin.git
cd KaguneBin
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the server

```bash
uvicorn main:app --reload
```

### API Docs

```bash
https://kagunebin.vercel.app/docs
```

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
  "downloads": 0,
  "created_at": "2026-05-27T12:00:00+00:00",
  "expires_at": null
}
```

---

## 🤝 Contributing

The project is still actively evolving, and ideas, feedback, and contributions are always welcome.

---

## 📌 Project Note

KaguneBin is an independent developer project inspired by anime aesthetics and developer culture.

Tokyo Ghoul and related characters belong to their respective creators and studios.

---

<div align="center">

# 🩸 KaguneBin

### Paste Fear. Share Power.

Built with caffeine, code, PostgreSQL, and anime inspiration.

</div>