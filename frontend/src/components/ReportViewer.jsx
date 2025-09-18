// src/components/ReportViewer.jsx
import React from "react";

const ReportViewer = ({ reportUrl }) => {
  if (!reportUrl) {
    return <p className="text-gray-500">No report generated yet.</p>;
  }

  return (
    <div className="mt-6">
      {/* PDF Preview */}
      <object
        data={reportUrl}
        type="application/pdf"
        width="100%"
        height="600"
        className="border rounded"
      >
        <p>
          PDF preview not available.{" "}
          <a href={reportUrl} download="impact-report.pdf" className="text-blue-600 underline">
            Download here
          </a>
        </p>
      </object>

      {/* Download Button */}
      <div className="mt-4">
        <a
          href={reportUrl}
          download="impact-report.pdf"
          className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded"
        >
          Download PDF
        </a>
      </div>
    </div>
  );
};

export default ReportViewer;
