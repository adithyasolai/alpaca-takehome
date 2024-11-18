// src/app/page.tsx
"use client"; // I don't know NextJS at all, so just going to use vanilla ReactJS with typing.

import React, { useEffect, useState } from "react";

function Home() {
  const [noteInputText, setNoteInputText] = useState('')
  const [submittedText, setSubmittedText] = useState<boolean>(false);
  const [submittedSummary, setSubmittedSummary] = useState<boolean>(false);

  const handleInputChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setNoteInputText(event.target.value)
  }

  const handleNoteSubmit = (event: React.FormEvent<HTMLFormElement>) => {
      event.preventDefault();
      setSubmittedText(true);
      setNoteInputText('');
  };

  const handleSummarySubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSubmittedSummary(true);
  };


  useEffect(() => {
    if (submittedText) {
      // set to false after 2 seconds to make the text pop-up go away
      setTimeout(() => {
        setSubmittedText(false)
      }, 2000)
    }
    
  }, [submittedText])

  return (
    <div className="flex flex-col items-center justify-center gap-6 p-6 text-center">
      <h1 className="text-2xl font-bold">
        Welcome to the Alpaca Note Summarizing Platform
      </h1>

      <div>
        <form onSubmit={handleNoteSubmit}>
          <textarea
            value={noteInputText}
            className="text-black"
            onChange={handleInputChange}
            placeholder="Type your session note here..."
            rows={5}
            cols={50}
            style={{
              width: '80%'
            }}
          />

          <br/>

          <button className="rounded-md bg-yellow-50 text-black p-1" type="submit">Submit</button>
        </form>

        {submittedText && (
          <div>
              <h2 className="text-white">Submitted Note!</h2>
          </div>
        )}
      </div>

      <div>
        <h1 className="text-xl font-bold">When ready, summarize notes below:</h1>

        <form onSubmit={handleSummarySubmit}>
          <button className="rounded-md bg-yellow-50 text-black p-1" type="submit">Summarize</button>
        </form>

        {submittedSummary && (
          <div>
              <h2 className="text-white">Summary Text Will Go Here...</h2>
          </div>
        )}
      </div>
    </div>
  );
}

export default Home;
