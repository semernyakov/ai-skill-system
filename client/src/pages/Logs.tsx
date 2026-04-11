import { useState, useEffect } from 'react';
import { api } from '../services/api';

interface LogEntry {
  timestamp: string;
  level: string;
  message: string;
  service?: string;
}

export default function Logs() {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState({
    service: '',
    level: '',
    limit: 50
  });

  const loadLogs = async () => {
    setLoading(true);
    try {
      const data = await api.logs.view(filter);
      setLogs(data);
    } catch (error) {
      console.error('Failed to load logs:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadLogs();
  }, []);

  const getLevelColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'error': return 'text-red-600 dark:text-red-400';
      case 'warn': return 'text-yellow-600 dark:text-yellow-400';
      case 'info': return 'text-blue-600 dark:text-blue-400';
      case 'debug': return 'text-gray-600 dark:text-gray-400';
      default: return 'text-gray-700 dark:text-gray-300';
    }
  };

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-6 text-gray-800 dark:text-white">Log Viewer</h2>
      
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-6">
        <div className="grid grid-cols-3 gap-4 mb-4">
          <input
            type="text"
            placeholder="Service filter"
            value={filter.service}
            onChange={(e) => setFilter({ ...filter, service: e.target.value })}
            className="px-3 py-2 border rounded dark:bg-gray-700 dark:border-gray-600 dark:text-white"
          />
          <select
            value={filter.level}
            onChange={(e) => setFilter({ ...filter, level: e.target.value })}
            className="px-3 py-2 border rounded dark:bg-gray-700 dark:border-gray-600 dark:text-white"
          >
            <option value="">All Levels</option>
            <option value="ERROR">ERROR</option>
            <option value="WARN">WARN</option>
            <option value="INFO">INFO</option>
            <option value="DEBUG">DEBUG</option>
          </select>
          <input
            type="number"
            placeholder="Limit"
            value={filter.limit}
            onChange={(e) => setFilter({ ...filter, limit: parseInt(e.target.value) || 50 })}
            className="px-3 py-2 border rounded dark:bg-gray-700 dark:border-gray-600 dark:text-white"
          />
        </div>
        <button
          onClick={loadLogs}
          disabled={loading}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
        >
          {loading ? 'Loading...' : 'Refresh'}
        </button>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <div className="space-y-2 max-h-96 overflow-y-auto">
          {logs.length === 0 ? (
            <p className="text-gray-500 dark:text-gray-400">No logs available</p>
          ) : (
            logs.map((log, index) => (
              <div key={index} className="p-2 bg-gray-50 dark:bg-gray-700 rounded font-mono text-sm">
                <div className="flex gap-2">
                  <span className="text-gray-500 dark:text-gray-400">
                    {log.timestamp}
                  </span>
                  <span className={getLevelColor(log.level)}>
                    {log.level}
                  </span>
                  {log.service && (
                    <span className="text-purple-600 dark:text-purple-400">
                      [{log.service}]
                    </span>
                  )}
                </div>
                <div className="text-gray-700 dark:text-gray-300 mt-1">
                  {log.message}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
