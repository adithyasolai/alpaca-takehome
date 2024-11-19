# Alpaca Health Software Engineering Take-Home Project

_Candidate: Adithya Solai_

### Project Description

Visit this link:
[Project Description](./ProjectDescription.md)

### API Documentation

Visit this link: [API Documentation](./api-documentation.md)

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

# Results

I ended up achieving all of my non-stretch-goal goals from my Project Scoping above.

I kind of also implemented the session parameters stretch goal using the AI agent prompt. I made the AI agent format the summary in a way that has time, patient name, therapist name, etc in the header of the summary write-up, and told it to expect that in the notes. One clunky downside is that the AI agent sometimes does not give a proper summary and asks for the user to input those header fields (duration, patient name, etc.), but maybe this is a feature and not a bug?

## Some Caveats/Context (Challenges)

- I don't know any NextJS, so I wrote the frontend as vanilla ReactJS (and made it client-side rendering) and tried my best with typing (not super comfortable with Typescript yet either).
- I didn't know TailwindCSS before this, but it was straight-forward to use its built-in classes after looking it up.
- I haven't used OpenAI API much before, but it was pretty intuitive. I had an account and API key from earlier, so I wasn't slowed down too much.
- I haven't worked with Redis before, but I knew what it was conceptually. I figured a NoSQL store like Redis makes more sense for unstructured data like this than a relational DB like sqlite. But I chose Redis because it is in-memory and fast to get set up.

# Approach & Design Decisions & Challenges

- (Approach) As seen in my scoping above, I deliberately focused on getting some backend functionality working before adding the frontend layer.
- (Approach) I ended up deviating a bit from the original plan. I just used an in-memory Python global list variable on the server for a while as my "database" while implementing frontend. Then I added the Redis DB to replace the Python global list.
- (Approach) I focused first on fully implementing the core customer flow of saving a note, and then creating a summary from those notes. Then, I implemented the save/view summary feature last.
- (Design Decision / Challenge) I knew I wanted to use a simple in-memory database for the sake of time. I was deciding between sqlite (relational) and redis (NoSQL). I opted for Redis because we are mainly storing unstructured data. If given more time, I would consider the pros/cons of using Vector Databases because those are tuned for use with AI Agents (but that could also come with extra overhead of using a framework like LangChain to smoothe the process of retrieving data from the Vector Database and sending it to the AI agent.)
- (Challenge) Due to time constraints, I also opted to completely ignore user authentication or supporting multiple users. It is an undifferentiated engineering effort that is not core to the customer experience this app is trying to provide. I've also proven I can implement this in my personal projects (example project: https://apex-pies.com/), so I decided to not implement it here.
- (Challenge) Due to time, there are no safety precautions on the API and I don't do all the error-checking and input validations I wouldn't normally done if given more time. I've documented some of these in the code and API documentation.

# Assumptions

- The user will put in the session info in the notes (patient name, therapist name, date, time, etc.)
- Scaling this core feature to many users and for many different sessions will be handled outside of the scope of this project. This tool shows how the summarization would work for a single session's worth of notes.
- Authenticating users will be handled outside of the scope of this project.


## Setup Instructions

### Backend Setup (Python 3.11+ required)

Adithya's Setup:

```bash
# Setting up Redis Server
# (Confirm that it does spin up in localhost Port 6379)

redis-server

```

```bash
# I noticed the Python 3.11+ too late, but my stuff still worked with Python 3.10, but I had to 
# modify the commands to make it work with Redis (because I installed Redis with Python3.10 on 
# my macbook, but the Python Env was still defaulting to 3.9.6)

# For simplicity, just do all of this in the /backend directory
cd backend

# Create and activate virtual environment
python3.10 -m venv alpaca_venv
source alpaca_venv/bin/activate

# Install dependencies
python3.10 -m pip install -r requirements.txt

# Start the server (uvicorn worked better for me)
python3.10 -m pip install uvicorn
python3.10 -m uvicorn main:app --reload
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

## Development

- Frontend runs on port 3000 with hot reload enabled
- Backend runs on port 8000 with auto-reload enabled
- Update backend dependencies: `pipreqs --force`

