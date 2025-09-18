// src/pages/Dashboard.jsx
import React, { useState, useEffect, useCallback } from "react";
import MetricCard from "../components/MetricCard";
import FilterBar from "../components/FilterBar";
import LearnerImpactChart from "../components/LearnerImpactChart";
import DemographicsByAge from "../components/DemographicsByAge";
import ImpactDistribution from "../components/ImpactDistribution";

const Dashboard = () => {
  const [metrics, setMetrics] = useState({
    totalLearners: 0,
    supportPartners: 0,
    volunteerHours: 0,
    activeVolunteers: 0,
  });
  const [loading, setLoading] = useState(false);
  const [selectedProgramId, setSelectedProgramId] = useState(null);
  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());
  const [reportUrl, setReportUrl] = useState(null);
  const [reportLoading, setReportLoading] = useState(false);
  const [reportError, setReportError] = useState(null);

  const fetchMetrics = useCallback(async (year, program) => {
    setSelectedProgramId(program);
    setSelectedYear(year);
    try {
      setLoading(true);

      const params = new URLSearchParams();
      if (year) params.append("year", year);
      if (program) params.append("program_id", program);

      const response = await fetch(
        `${
          import.meta.env.VITE_API_URL
        }/api/metrics/summary?${params.toString()}`
      );
      const data = await response.json();

      setMetrics(data);
    } catch (error) {
      console.error("Failed to fetch metrics:", error);
    } finally {
      setLoading(false);
    }
  }, []);

  const LoadingSpinner = () => (
    <div className="flex items-center justify-center h-64">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-pink-500"></div>
    </div>
  );

  // ---- PDF generation handler ----
  const handleGenerate = (year, program) => {
    if (!program) return;
    const endpoint = `${
      import.meta.env.VITE_API_URL
    }/api/report/start?year=${year}&program_id=${program}`;
    window.open(endpoint, "_blank", "noopener,noreferrer");
  };

  useEffect(() => {
    return () => {
      if (reportUrl) URL.revokeObjectURL(reportUrl);
    };
  }, [reportUrl]);

  const MetricCardSkeleton = () => (
    <div className="bg-gray-50 p-6 rounded-lg flex-1 min-w-0 animate-pulse">
      <div className="h-10 bg-gray-200 rounded mb-2 w-3/4"></div>
      <div className="h-4 bg-gray-200 rounded w-1/2"></div>
    </div>
  );

  return (
    <div className="min-h-screen bg-white">
      <div className="max-w-7xl mx-auto">
        <FilterBar onFilterChange={fetchMetrics} onGenerate={handleGenerate} />

        <div className="px-6">
          <div className="flex gap-6">
            {loading ? (
              <>
                <MetricCardSkeleton />
                <MetricCardSkeleton />
                <MetricCardSkeleton />
                <MetricCardSkeleton />
              </>
            ) : (
              <>
                <MetricCard
                  title="Total Learners"
                  value={metrics.totalLearners}
                />
                <MetricCard
                  title="Support Partners"
                  value={metrics.supportPartners}
                />
                <MetricCard
                  title="Volunteers Hours Contributed"
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

        <div className="px-6 mt-8">
          <div className="flex gap-6 bg-gray-50 p-6 rounded-lg">
            {/* LearnerImpactChart */}
            <div className="flex-[0.5]">
              <LearnerImpactChart
                programId={selectedProgramId}
                year={selectedYear}
              />
            </div>

            {/* DemographicsByAge */}
            <div className="flex-[0.25]">
              <DemographicsByAge
                year={selectedYear}
                programId={selectedProgramId}
              />
            </div>

            {/* ImpactDistribution */}
            <div className="flex-[0.25]">
              <ImpactDistribution
                year={selectedYear}
                programId={selectedProgramId}
              />
            </div>
          </div>
        </div>

        {/* PDF preview area */}
        {/* Full page loading overlay */}
        {reportLoading && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40">
            <LoadingSpinner />
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
