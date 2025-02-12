import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # DeepSeek Settings
    DEEPSEEK_API_KEY = "sk-af749e21804b40f4ba5da1381b749879"
    DEEPSEEK_MODEL = "deepseek-chat"
    DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
    
    # Database
    SHEET_ID = "1_gFP3lKUEWAvKAuXbpPT-2hRp7Mvy11TJjoAwz_ck80"
    
    # Server Settings
    PORT = int(os.getenv("PORT", 5000))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true" 