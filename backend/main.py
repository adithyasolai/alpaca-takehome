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

# TODO: put this into a sqlite db and fetch it. this is for testing purposes only.
notes = [
    "Date: 11/18/24",
    "Session Time: 8 PM - 9 PM EST",
    "Therapist Name: Adithya Solai",
    "Patient Name: John Abraham"
    "John arrived at the session calm and greeted the therapist with a smile.",
    "During the first activity (matching colors), John successfully matched 8 out of 10 colors with 80% accuracy.",
    "He required minimal prompts (2 verbal prompts) to complete the task.",
    "Used visual aids for color matching.",
    "Reinforced correct matches with verbal praise and a small reward (sticker).",
    "John exhibited signs of frustration (e.g., frowning, vocal protests) when he was unable to match two specific colors. \
        This behavior lasted approximately 2 minutes before he was able to refocus with support.",
    "For future session: Continue to use visual aids and consider introducing a timer to help John manage task completion."
]

system_instruction = "You are an assistant to an Applied Behavior Analysis therapist that is supposed to take their notes \
    from a session with an autism patient and re-write the notes into a professional summary of the session while maintaining \
    clinical accuracy. Make sure to include the Date, Session Time, Therapist Name, and Patient Name at the top of the summary. \
    These details will be included in the notes."

@app.get("/synthesize")
async def synthesize():
    # concatenate notes into a single input for API
    notes_input = " ".join(notes)

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_instruction},
                {
                    "role": "user",
                    "content": notes_input,
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