import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    NAVIGATE_API_KEY = "sk-CRClC_K-jlNd_v3qAY4HGQ"
    NAVIGATE_BASE_URL = "https://apidev.navigatelabsai.com/"
    UPLOAD_FOLDER = "uploads"
    DATABASE_URL = "sqlite:///voicehire.db"