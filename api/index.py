import sys
import os

# Include current root directory in path for Vercel imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

# Export handler for Vercel Python Serverless Engine
handler = app
