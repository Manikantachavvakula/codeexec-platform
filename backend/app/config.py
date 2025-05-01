import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API configurations
API_PREFIX = "/api"
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
PROJECT_NAME = "CodeExplorer API"

# Piston API configuration
PISTON_API_URL = os.getenv("PISTON_API_URL", "https://emkc.org/api/v2/piston")

# Supported languages
SUPPORTED_LANGUAGES = [
    "python", "javascript", "typescript", "java", "c", "cpp", "csharp", 
    "go", "ruby", "rust", "php"
]

# Database configuration (for future use)
DATABASE_TYPE = os.getenv("DATABASE_TYPE", "mongodb")
DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017/code_explorer")