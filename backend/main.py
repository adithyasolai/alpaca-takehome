from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
from redis import Redis
# Load environment variables from .env file in the upper directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Connect to the Redis server
r = Redis(host='localhost', port=6379, db=0)

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

system_instruction = "You are an assistant to an Applied Behavior Analysis therapist that is supposed to take their notes \
    from a session with an autism patient and re-write the notes into a professional summary of the session while maintaining \
    clinical accuracy. Make sure to include the Date, Session Time, Therapist Name, and Patient Name at the top of the summary. \
    These details will be included in the notes."

# define a data model for the input (simple for now, but this is more extensible in the future)
class Note(BaseModel):
    body: str

TEST_USER_ID = 1000

@app.post("/note")
async def synthesize(note: Note):
    # prepare to store in Redis db
    userKey = f'user:{TEST_USER_ID}'
    userNotesKey = userKey + ":notes"

    # store in redis DB
    r.rpush(userNotesKey, note.body)

    # print list of notes in Redis db right now
    redisNotes = r.lrange(userNotesKey, 0, -1)  # Get all notes from the list
    redisNotes = [note.decode('utf-8') for note in redisNotes]
    print("redisNotes:", redisNotes)

    return {"message": "Note saved successfully!"}


@app.get("/summary")
async def summarize():
    # get notes from Redis
    userKey = f'user:{TEST_USER_ID}'
    userNotesKey = userKey + ":notes"
    redisNotes = r.lrange(userNotesKey, 0, -1)  # Get all notes from the list
    redisNotes = [note.decode('utf-8') for note in redisNotes]

    # concatenate notes into a single input for API
    notes_input = " ".join(redisNotes)

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