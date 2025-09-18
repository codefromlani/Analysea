// src/components/DemographicsByAge.jsx
import React, { useState, useEffect } from 'react';

const DemographicsByAge = ({ year, programId }) => {
  const [data, setData] = useState({
    total_beneficiaries: 0,
    demographics: []
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const colorMap = {
    "18 - 25": "#86efac", 
    "26 - 35": "#fde68a", 
    "36 - 40": "#fbbf24" 
  };

  useEffect(() => {
    const fetchDemographics = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const params = new URLSearchParams();
        if (year) params.append("year", year);
        if (programId) params.append("program_id", programId);
        
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/api/learner_demographics?${params.toString()}`
        );
        
        if (!response.ok) {
          throw new Error('Failed to fetch demographics data');
        }
        
        const result = await response.json();
        setData(result);
      } catch (err) {
        console.error('Error fetching demographics data:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchDemographics();
  }, [year, programId]);

  const LoadingSpinner = () => (
    <div className="flex items-center justify-center h-64">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-pink-500"></div>
    </div>
  );

  const ErrorMessage = () => (
    <div className="flex items-center justify-center h-64">
      <div className="text-red-500 text-sm">
        Error loading demographics data: {error}
      </div>
    </div>
  );

  const EmptyState = () => (
    <div className="flex items-center justify-center h-64">
      <div className="text-gray-500 text-sm">
        No demographics data available
      </div>
    </div>
  );

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage />;
  if (!data.demographics || data.demographics.length === 0) return <EmptyState />;

  return (
    <div className="bg-white p-6 rounded-lg border border-gray-200">
      {/* Title */}
      <h3 className="text-lg font-semibold text-gray-900 mb-6">
        Demography by Age
      </h3>
      
      {/* Total Beneficiaries */}
      <div className="text-center mb-8">
        <div className="text-gray-500 text-sm mb-2">
          Total Learners
        </div>
        <div className="text-4xl font-bold text-gray-900">
          {data.total_beneficiaries}
        </div>
      </div>
      
      {/* Horizontal Segmented Bar Chart */}
      <div className="mb-6">
        <div className="flex h-8 rounded-lg overflow-hidden bg-gray-100">
          {data.demographics.map((demo, index) => (
            <div
              key={demo.age_range}
              className="transition-all duration-300"
              style={{
                width: `${demo.percentage}%`,
                backgroundColor: colorMap[demo.age_range],
              }}
            />
          ))}
        </div>
      </div>
      
      {/* Legend */}
      <div className="space-y-3">
        {data.demographics.map((demo) => (
          <div key={demo.age_range} className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div 
                className="w-3 h-3 rounded-full"
                style={{ backgroundColor: colorMap[demo.age_range] }}
              />
              <span className="text-sm text-gray-700">
                {demo.age_range}
              </span>
            </div>
            <span className="text-sm font-medium text-green-600">
              {demo.percentage}%
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default DemographicsByAge;