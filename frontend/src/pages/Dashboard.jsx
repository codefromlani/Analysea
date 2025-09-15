import React, { useState, useEffect, useCallback } from "react";
import MetricCard from "../components/MetricCard";
import FilterBar from "../components/FilterBar";

const Dashboard = () => {
  const [metrics, setMetrics] = useState({
    totalLearners: 0,
    supportPartners: 0,
    volunteerHours: 0,
    activeVolunteers: 0,
  });
  const [loading, setLoading] = useState(false); 

  const fetchMetrics = useCallback(async (year, program) => {
    try {
      setLoading(true); 
      const params = new URLSearchParams();
      if (year) params.append("year", year);
      if (program) params.append("program_id", program);

      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/api/metrics/summary?${params.toString()}`
      );
      const data = await response.json();

      setMetrics(data);
    } catch (error) {
      console.error("Failed to fetch metrics:", error);
    } finally {
      setLoading(false); 
    }
  }, []);

  useEffect(() => {
    fetchMetrics(new Date().getFullYear(), null);
  }, [fetchMetrics]);

  return (
    <div style={{ padding: "20px", maxWidth: "1200px", margin: "auto" }}>
      <h1 style={{ marginBottom: "20px" }}>Analysea</h1>

      <FilterBar onFilterChange={fetchMetrics} onGenerate={fetchMetrics} />

      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "space-between",
        }}
      >
        {loading ? (
          <>
            <MetricCard title="Total Learners" value="Loading..." />
            <MetricCard title="Support Partners" value="Loading..." />
            <MetricCard title="Volunteer Hours Contributed" value="Loading..." />
            <MetricCard title="Active Volunteers" value="Loading..." />
          </>
        ) : (
          <>
            <MetricCard title="Total Learners" value={metrics.totalLearners} />
            <MetricCard title="Support Partners" value={metrics.supportPartners} />
            <MetricCard
              title="Volunteer Hours Contributed"
              value={`${metrics.volunteerHours}h`}
            />
            <MetricCard
              title="Active Volunteers"
              value={metrics.activeVolunteers}
            />
          </>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
