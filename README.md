# Alpaca Health Software Engineering Take-Home Project

_Candidate: Adithya Solai_


### Project Description

Visit this link for details:
[Project Description](./ProjectDescription.md)

## My Project Scoping

_I wrote this up before starting to code._

- First, get backend to just take in 1 sample note from an ABA and respond with a more professionally-written version of that note. Completely ignore frontend for now and just make GET/POST requests directly to server to test.
- Then, implement a simple in-memory DB like sqlite to store all previous notes. Write a new POST API that simply allows users to log a note. No ChatGPT response is given/generated here. Then, write a separate GET API that will synthesize all existing notes as input and return a professionally-written summary of all notes in the input.
  - I will ignore implementing user authentication for this project due to time constraints. It is also something I have implemented in my personal projects, so I know I can do it if given time (example project: https://apex-pies.com/).
  - Still ignoring frontend at this point.
- Finally start working on frontend. Make a box for users to just submit notes. Make a button at the bottom called "synthesize" or something that will actually return the AI summary.
- Write some new APIs that allow users to also save AI-generated summaries to the DB, retrieve summaries, and then hand-edit them and re-save them.

Stretch Goals:
- user can input session parameters (duration, type, etc.) (tbh I don't have much industry context for what this means, but I can look into it if I have time)
- Ability to retrieve and update original notes, and then re-synthesize to effectively try and meet the stretch goal of being able to refine/regenerate the summary.
- Ability for user to modify the starting prompt given to the LLM to dictate the formatting/style of the output.
  - This might be the quickest stretch goal to implement, so I might start here if there is time.
- Improved style/CSS/UX

## Some Caveats/Context

- I don't know any NextJS, so I wrote the frontend as vanilla ReactJS with typing (and made it client-side rendering).
- I didn't know TailwindCSS before this, but it was straight-forward to use its built-in classes after looking it up.
- I haven't used OpenAI API much before, but it was pretty intuitive. I had an account and API key from earlier, so I wasn't slowed down too much.

## Setup Instructions

### Backend Setup (Python 3.11+ required)

```bash
# Create and activate virtual environment
python -m venv alpaca_venv
source alpaca_venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Start the server
fastapi dev main.py

# worked better for me (Adithya Solai)
uvicorn main:app --reload
```

### Frontend Setup (Node.js 18+ required)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The application will be available at:

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Default Project Structure

- `frontend/`: Next.js application
  - `src/components/`: Reusable React components
  - `src/app/`: Next.js app router pages
- `backend/`: FastAPI application
  - `app/main.py`: API endpoints

## Development

- Frontend runs on port 3000 with hot reload enabled
- Backend runs on port 8000 with auto-reload enabled
- API documentation available at http://localhost:8000/docs
- Update backend dependencies: `pipreqs --force`

