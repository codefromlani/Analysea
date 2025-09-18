// src/components/LearnerImpactChart.jsx
import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const LearnerImpactChart = ({ programId, year }) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchImpactData = async () => {
      if (!programId) {
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        setError(null);
        
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/api/impact/learner_impact_trend?program_id=${programId}&year=${year}`
        );
        
        if (!response.ok) {
          throw new Error('Failed to fetch impact data');
        }
        
        const result = await response.json();
        setData(result);
      } catch (err) {
        console.error('Error fetching impact data:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchImpactData();
  }, [programId, year]);

  const LoadingSpinner = () => (
    <div className="flex items-center justify-center h-64">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-pink-500"></div>
    </div>
  );

  const ErrorMessage = () => (
    <div className="flex items-center justify-center h-64">
      <div className="text-red-500 text-sm">
        Error loading chart data: {error}
      </div>
    </div>
  );

  const EmptyState = () => (
    <div className="flex items-center justify-center h-64">
      <div className="text-gray-500 text-sm">
        No data available for this program
      </div>
    </div>
  );

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 border border-gray-200 rounded shadow-lg">
          <p className="text-sm font-medium text-gray-900">{`Cohort: ${label}`}</p>
          <p className="text-sm text-pink-600">
            {`Completion: ${payload[0].value}%`}
          </p>
        </div>
      );
    }
    return null;
  };

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage />;
  if (!data || data.length === 0) return <EmptyState />;

  return (
    <div className="bg-white p-6 rounded-lg border border-gray-200">
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">
          Learners Impact Growth Trend
        </h3>
      </div>
      
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart
            data={data}
            margin={{
              top: 10,
              right: 20,
              left: -20,
              bottom: 5,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis 
              dataKey="cohort" 
              tick={{ fontSize: 12, fill: '#6b7280' }}
              tickLine={{ stroke: '#d1d5db' }}
              axisLine={{ stroke: '#d1d5db' }}
              padding={{ left: 20}}
            />
            <YAxis 
              domain={[0, 100]}
              ticks={[0, 25, 50, 75, 100]}
              tick={{ fontSize: 12, fill: '#6b7280' }}
              tickLine={{ stroke: '#d1d5db' }}
              axisLine={{ stroke: '#d1d5db' }}
              tickFormatter={(value) => `${value}%`}
              label={{ 
                angle: -90, 
                position: 'insideLeft',
                style: { textAnchor: 'middle', fontSize: '12px', fill: '#6b7280' }
              }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Line 
              type="monotone" 
              dataKey="percentage" 
              stroke="#ec4899" 
              strokeDasharray="5 5"
              strokeWidth={2}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default LearnerImpactChart;