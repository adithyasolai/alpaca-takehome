from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file in the upper directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# make OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)



app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/test")
async def test():
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "give a list of the past 5 presidents",
                }
            ],
            model="gpt-4o-mini",
        )
        return {"generated_text": chat_completion.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def health_check():
    return {"status": "healthy"}