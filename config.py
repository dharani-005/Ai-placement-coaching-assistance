import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    NAVIGATE_API_KEY = "key"
    NAVIGATE_BASE_URL = "url"
    UPLOAD_FOLDER = "uploads"
    DATABASE_URL = "sqlite:///voicehire.db"