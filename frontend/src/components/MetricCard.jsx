// src/components/MetricCard.jsx
import React from 'react';

const MetricCard = ({ title, value }) => {
  return (
    <div className="bg-gray-50 p-6 rounded-lg flex-1 min-w-0">
      <div className="text-4xl font-bold text-gray-900 mb-2">
        {value}
      </div>
      <div className="text-sm text-gray-600 leading-tight">
        {title}
      </div>
    </div>
  );
};

export default MetricCard;