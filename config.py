import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    NAVIGATE_API_KEY = os.getenv("NAVIGATE_API_KEY")
    if NAVIGATE_API_KEY is None:
        raise ValueError("NAVIGATE_API_KEY environment variable is not set")
    
    NAVIGATE_BASE_URL = os.getenv("NAVIGATE_BASE_URL")
    if NAVIGATE_BASE_URL is None:
        raise ValueError("NAVIGATE_BASE_URL environment variable is not set")
    
    UPLOAD_FOLDER = "uploads"
    DATABASE_URL = "sqlite:///voicehire.db"
