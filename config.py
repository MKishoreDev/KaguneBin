import os

DATABASE_URI = os.getenv("DATABASE_URI", "postgresql://postgres:password@localhost:5432/pastebin")