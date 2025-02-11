import os

class Config:
    # Database
    SHEET_ID = os.getenv('SHEET_ID')
    
    # API Settings
    OLLAMA_API = os.getenv('OLLAMA_API_URL', 'http://localhost:11434/api/generate')
    
    # Model Settings
    NUM_THREADS = int(os.getenv('NUM_THREADS', 4))
    CONTEXT_SIZE = int(os.getenv('CONTEXT_SIZE', 512))
    
    # Server Settings
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true' 