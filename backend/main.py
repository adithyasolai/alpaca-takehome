from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables from .env file in the upper directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    output = os.environ['OPENAI_API_KEY']
    return {"status": "healthy", "output": output}