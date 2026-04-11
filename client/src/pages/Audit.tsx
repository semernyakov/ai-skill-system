import { useState } from 'react';
import { api } from '../services/api';

export default function Audit() {
  const [results, setResults] = useState<any[]>([]);
  const [selectedType, setSelectedType] = useState('SECURITY');

  const runAudit = async () => {
    const result = await api.audit.run(selectedType);
    setResults([result, ...results]);
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">System Audit</h1>

      <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow mb-6">
        <h2 className="text-xl font-semibold mb-4">Run Audit</h2>
        <div className="flex space-x-4">
          <select
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value)}
            className="p-2 border rounded dark:bg-gray-700 dark:border-gray-600"
          >
            <option value="SECURITY">Security</option>
            <option value="PERFORMANCE">Performance</option>
            <option value="ARCHITECTURE">Architecture</option>
            <option value="COMPLIANCE">Compliance</option>
          </select>
          <button
            onClick={runAudit}
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          >
            Run Audit
          </button>
        </div>
      </div>

      <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
        <h2 className="text-xl font-semibold mb-4">Audit Results</h2>
        <div className="space-y-4">
          {results.map((result) => (
            <div key={result.id} className="p-4 bg-gray-50 dark:bg-gray-700 rounded">
              <div className="flex justify-between items-center mb-2">
                <h3 className="font-medium">Audit #{result.id}</h3>
                <span className="text-sm text-gray-600 dark:text-gray-400">
                  {result.audit_type}
                </span>
              </div>
              <p className="text-sm mb-2">{result.summary}</p>
              <div className="space-y-2">
                {result.findings.map((finding: any, idx: number) => (
                  <div
                    key={idx}
                    className={`p-3 rounded ${
                      finding.severity === 'HIGH'
                        ? 'bg-red-100 dark:bg-red-900'
                        : finding.severity === 'MEDIUM'
                        ? 'bg-yellow-100 dark:bg-yellow-900'
                        : 'bg-green-100 dark:bg-green-900'
                    }`}
                  >
                    <p className="font-medium text-sm">{finding.category}</p>
                    <p className="text-sm">{finding.message}</p>
                    <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                      {finding.recommendation}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
