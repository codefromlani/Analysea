// src/components/FilterBar.jsx
import React, { useState, useEffect } from "react";

const FilterBar = ({ onFilterChange }) => {
  const [year, setYear] = useState(new Date().getFullYear());
  const [program, setProgram] = useState(null);
  const [programs, setPrograms] = useState([]);

  useEffect(() => {
    const fetchPrograms = async () => {
      try {
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/api/programs`
        );
        const data = await response.json();
        setPrograms(data);
        if (data.length > 0) {
          setProgram(data[0].id);
        }
      } catch (error) {
        console.error("Error fetching programs:", error);
      }
    };

    fetchPrograms();
  }, []);

  useEffect(() => {
    if (program !== null) {
      onFilterChange(year, program);
    }
  }, [year, program, onFilterChange]);

  return (
    <div className="bg-gray-50 mb-10">
      <div className="px-6 pt-6">
        {/* Logo */}
        <div className="text-xl font-bold text-gray-800 mb-4">ANALYSEA</div>
      </div>
      
      <div className="px-6 pb-6">
        <div className="flex justify-between items-center">
          {/* Left side - Selectors */}
          <div className="flex items-center gap-4">
            {/* Year Selector */}
            <div className="relative">
              <select
                value={year}
                onChange={(e) => setYear(parseInt(e.target.value))}
                className="appearance-none bg-white border border-gray-300 rounded px-4 py-2 pr-8 text-sm focus:outline-none focus:ring-2 focus:border-transparent"
              >
                {[2025, 2024, 2023, 2022].map((y) => (
                  <option key={y} value={y}>
                    📅 {y}
                  </option>
                ))}
              </select>
              <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
                <svg
                  className="fill-current h-4 w-4"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                >
                  <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
                </svg>
              </div>
            </div>

            {/* Program Selector */}
            <div className="relative">
              <select
                value={program || ""}
                onChange={(e) => setProgram(parseInt(e.target.value))}
                className="appearance-none bg-white border border-gray-300 rounded px-4 py-2 pr-8 text-sm focus:outline-none focus:ring-2 focus:border-transparent"
              >
                {programs.map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.name}
                  </option>
                ))}
              </select>
              <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
                <svg
                  className="fill-current h-4 w-4"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                >
                  <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
                </svg>
              </div>
            </div>
          </div>

          {/* Right side - Generate Button */}
          <button
            className="bg-pink-500 hover:bg-pink-600 text-white font-medium px-6 py-2 rounded transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            disabled
          >
            Generate
          </button>
        </div>
      </div>
    </div>
  );
};

export default FilterBar;