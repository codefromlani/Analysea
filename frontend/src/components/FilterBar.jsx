// src/components/FilterBar.jsx
import React, { useState, useEffect } from "react";

const FilterBar = ({ onFilterChange, onGenerate }) => {
  const [year, setYear] = useState(new Date().getFullYear());
  const [program, setProgram] = useState(null);
  const [programs, setPrograms] = useState([]);

  useEffect(() => {
    const fetchPrograms = async () => {
      try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/api/programs`);
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
  <div
    style={{
      display: "flex",
      justifyContent: "space-between", 
      alignItems: "center",
      marginBottom: "40px",
    }}
  >
    
    <div style={{ display: "flex", gap: "10px" }}>
      {/* Year Selector */}
      <select
        value={year}
        onChange={(e) => setYear(parseInt(e.target.value))}
        style={{
          padding: "8px",
          borderRadius: "4px",
          border: "1px solid #ccc",
        }}
      >
        {[2025, 2024, 2023, 2022].map((y) => (
          <option key={y} value={y}>
            {y}
          </option>
        ))}
      </select>

      {/* Program Selector */}
      <select
        value={program || ""}
        onChange={(e) => setProgram(parseInt(e.target.value))}
        style={{
          padding: "8px",
          borderRadius: "4px",
          border: "1px solid #ccc",
        }}
      >
        {programs.map((p) => (
          <option key={p.id} value={p.id}>
            {p.name}
          </option>
        ))}
      </select>
    </div>

    {/* Generate Button */}
    <button
      onClick={() => onGenerate(year, program)}
      style={{
        padding: "10px 20px",
        backgroundColor: "#ff1493",
        color: "white",
        border: "none",
        borderRadius: "4px",
        cursor: "pointer",
      }}
      disabled={!program}
    >
      Generate
    </button>
  </div>
);
};

export default FilterBar;
