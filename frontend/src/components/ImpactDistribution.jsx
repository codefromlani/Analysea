// src/components/ImpactDistribution.jsx
import React, { useState, useEffect } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

const ImpactDistribution = ({ year, programId }) => {
  const [data, setData] = useState({ distribution: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const colorPalette = [
    "#86efac", 
    "#ec4899", 
    "#22d3ee", 
    "#fbbf24",
    "#a78bfa", 
    "#fb7185", 
    "#34d399", 
    "#60a5fa"  
  ];

  useEffect(() => {
    const fetchDistribution = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const params = new URLSearchParams();
        if (year) params.append("year", year);
        if (programId) params.append("program_id", programId);
        
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/api/learner/course_distribution?${params.toString()}`
        );
        
        if (!response.ok) {
          throw new Error('Failed to fetch distribution data');
        }
        
        const result = await response.json();
        setData(result);
      } catch (err) {
        console.error('Error fetching distribution data:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchDistribution();
  }, [year, programId]);

  const LoadingSpinner = () => (
    <div className="flex items-center justify-center h-64">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-pink-500"></div>
    </div>
  );

  const ErrorMessage = () => (
    <div className="flex items-center justify-center h-64">
      <div className="text-red-500 text-sm">
        Error loading distribution data: {error}
      </div>
    </div>
  );

  const EmptyState = () => (
    <div className="flex items-center justify-center h-64">
      <div className="text-gray-500 text-sm">
        No distribution data available
      </div>
    </div>
  );

  // Prepare data for the pie chart
  const chartData = data.distribution.map((item, index) => ({
    ...item,
    color: colorPalette[index % colorPalette.length],
    name: item.course,
    value: item.percentage
  }));

  // Custom label function to show percentages on pie slices
  const renderLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent, index, name }) => {
  const radius = innerRadius + (outerRadius - innerRadius) / 2;
  const RADIAN = Math.PI / 180;
  const x = cx + radius * Math.cos(-midAngle * RADIAN);
  const y = cy + radius * Math.sin(-midAngle * RADIAN);

  return (
    <text
      x={x}
      y={y}
      fill="#fff"
      textAnchor="middle"
      dominantBaseline="central"
      fontSize={12}
      fontWeight="bold"
    >
      {`${chartData[index].value}%`}
    </text>
  );
};


  // Custom tooltip
  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 border border-gray-200 rounded shadow-lg">
          <p className="text-sm font-medium text-gray-900">
            {payload[0].payload.course}
          </p>
          <p className="text-sm text-pink-600">
            {`${payload[0].value}%`}
          </p>
        </div>
      );
    }
    return null;
  };

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage />;
  if (!data.distribution || data.distribution.length === 0) return <EmptyState />;

  return (
    <div className="bg-white p-6 rounded-lg border border-gray-200">
      {/* Title */}
      <h3 className="text-lg font-semibold text-gray-900 mt-*">
        Learners Distribution
      </h3>
      
      {/* Pie Chart */}
        <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              outerRadius={80}
              dataKey="value"
              label={renderLabel}
              labelLine={false}
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
          </PieChart>
        </ResponsiveContainer>
      </div>
      
      {/* Legend */}
      <div className="grid grid-cols-2 gap-3">
        {chartData.map((item, index) => (
          <div key={item.course} className="flex items-center gap-2">
            <div 
              className="w-3 h-3 rounded-full flex-shrink-0"
              style={{ backgroundColor: item.color }}
            />
            <span className="text-xs text-gray-500 truncate">
              {item.course}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ImpactDistribution;