// src/app/page.tsx
"use client"; // I don't know NextJS at all, so just going to use vanilla ReactJS with typing.

import Link from "next/link";
import React, { useEffect, useState } from "react";

function Summaries() {
  const [numSummaries, setNumSummaries] = useState<number>(0);
  const [selectedNumber, setSelectedNumber] = useState<number>(1);
  const [summaryFetched, setSummaryFetched] = useState<boolean>(false);
  const [summaryText, setSummaryText] = useState<string>("");

  const getNumSummaries = async () => {
    // fetch summary from backend, and update state
    try {
      const response = await fetch("http://localhost:8000/numSummaries");

      if (!response.ok) {
        throw new Error("API response was not OK.");
      }

      const responseData = await response.json();

      setNumSummaries(responseData.num_summaries);
    } catch (error) {
      console.error("Error submitting note: ", error);
      // TODO: trigger some error message to user
    }
  };

  useEffect(() => {
    // fetch number of summaries for this user from backend
    (async () => {
      await getNumSummaries();
    })();
  }, []);

  const handleSelectChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedNumber(Number(event.target.value));
  };

  const handleViewSummary = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    // fetch summary from backend, and update state
    try {
      const response = await fetch(
        `http://localhost:8000/savedSummary?summary_num=${selectedNumber}`,
      );

      if (!response.ok) {
        throw new Error("API response was not OK.");
      }

      const responseData = await response.json();
      setSummaryText(responseData.summary);
      setSummaryFetched(true);
    } catch (error) {
      console.error("Error submitting note: ", error);
      // TODO: trigger some error message to user
    }
  };

  // Generate an array of numbers from 1 to numSummaries
  const options = Array.from({ length: numSummaries }, (_, i) => i + 1);

  return (
    <div className="flex flex-col items-center justify-center gap-6 p-6 text-center">
      <h1 className="text-2xl font-bold">Welcome to the Summary Viewer</h1>

      <p>Number of Summaries Available: {numSummaries}</p>

      <form
        className="flex flex-col items-center gap-4"
        onSubmit={handleViewSummary}
      >
        <label htmlFor="summarySelect" className="font-semibold">
          Select a summary number:
        </label>

        <select
          id="summarySelect"
          value={selectedNumber}
          onChange={handleSelectChange}
          className="p-2 border rounded-md"
        >
          {options.map((num) => (
            <option key={num} value={num}>
              {num}
            </option>
          ))}
        </select>
        <button
          type="submit"
          className="rounded-md bg-blue-500 text-white p-2 hover:bg-blue-600 transition-colors"
        >
          View Summary
        </button>
      </form>

      {summaryFetched && (
        <div>
          <h2 className="text-white">{summaryText}</h2>
        </div>
      )}

      <Link href="/">
        <button className="rounded-md bg-yellow-50 text-black p-1">Home</button>
      </Link>
    </div>
  );
}

export default Summaries;
