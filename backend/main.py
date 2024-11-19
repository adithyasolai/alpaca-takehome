from fastapi import FastAPI, HTTPException, Query
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

# define a data model for the Note input (simple for now, but this is more extensible in the future)
class Note(BaseModel):
    body: str

TEST_USER_ID = 1000

'''
Saves given note to user's data in the Redis DB to be
used later by the Open AI agent to generate a summary.
'''
@app.post("/note")
async def saveNote(note: Note):
    # prepare to store in Redis db
    userKey = f'user:{TEST_USER_ID}'
    userNotesKey = userKey + ":notes"

    # store in redis DB
    r.rpush(userNotesKey, note.body)

    return {"message": "Note saved successfully!"}

# define a data model for the Note input (simple for now, but this is more extensible in the future)
class Summary(BaseModel):
    body: str

'''
Saves given summary to user's data in Redis DB
'''
@app.post("/summary")
async def saveSummary(summary: Summary):
    # prepare to store in Redis db
    userKey = f'user:{TEST_USER_ID}'
    userSummariesKey = userKey + ":summaries"

    # store in redis DB
    r.rpush(userSummariesKey, summary.body)

    return {"message": "Summary saved successfully!"}

'''
Gets Number of Summaries for this user
'''
@app.get("/numSummaries")
async def numSummaries():
    # prepare to fetch from Redis db
    userKey = f'user:{TEST_USER_ID}'
    userSummariesKey = userKey + ":summaries"

    # get list of summaries in Redis db right now
    redisSummaries = r.lrange(userSummariesKey, 0, -1)  # Get all notes from the list
    redisSummaries = [note.decode('utf-8') for note in redisSummaries]

    return {"num_summaries": len(redisSummaries)}

'''
Gets a particular saved Summary for the user
'''
@app.get("/savedSummary")
async def getSavedSummary(summary_num: int = Query(default=1)):
    # prepare to fetch from Redis db
    userKey = f'user:{TEST_USER_ID}'
    userSummariesKey = userKey + ":summaries"

    # get list of summaries in Redis db right now
    redisSummaries = r.lrange(userSummariesKey, 0, -1)  # Get all notes from the list
    redisSummaries = [note.decode('utf-8') for note in redisSummaries]

    return {"summary": redisSummaries[summary_num-1]}

'''
Gets all notes for the user from Redis DB, and then synthesizes a summary using
the Open AI agent.
'''
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