import os

DATABASE_URI = os.environ.get("DATABASE_URI", "").strip()
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", 8000))
ENVIRONMENT = os.environ.get("ENVIRONMENT", "production")
DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1", "yes")
BASE_URL = os.environ.get("BASE_URL", "https://kagunebin.vercel.app").rstrip("/")