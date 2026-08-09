from dotenv import load_dotenv
import os

# Load environment variables from .env if present
load_dotenv()

DATABASE_PATH = os.getenv('DATABASE_PATH', 'database/expenses.db')
API_PORT = int(os.getenv('API_PORT', '5000'))
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:5000')
FRONTEND_ORIGIN = os.getenv('FRONTEND_ORIGIN', 'http://localhost:3000')
