import { useState, useEffect } from 'react';
import { api } from '../services/api';

export default function MCPGateway() {
  const [services, setServices] = useState<any[]>([]);

  useEffect(() => {
    loadServices();
  }, []);

  const loadServices = async () => {
    const data = await api.mcp.listServices();
    setServices(data);
  };

  const startService = async (name: string) => {
    await api.mcp.startService(name);
    loadServices();
  };

  const stopService = async (name: string) => {
    await api.mcp.stopService(name);
    loadServices();
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">MCP Gateway</h1>

      <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
        <h2 className="text-xl font-semibold mb-4">Services</h2>
        <div className="space-y-2">
          {services.map((service) => (
            <div key={service.name} className="flex justify-between items-center p-4 bg-gray-50 dark:bg-gray-700 rounded">
              <div>
                <p className="font-medium text-lg">{service.name}</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {service.host}:{service.port}
                </p>
              </div>
              <div className="flex items-center space-x-4">
                <span
                  className={`px-3 py-1 rounded text-sm ${
                    service.status === 'running'
                      ? 'bg-green-100 text-green-800'
                      : 'bg-red-100 text-red-800'
                  }`}
                >
                  {service.status}
                </span>
                {service.status === 'stopped' ? (
                  <button
                    onClick={() => startService(service.name)}
                    className="bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600 text-sm"
                  >
                    Start
                  </button>
                ) : (
                  <button
                    onClick={() => stopService(service.name)}
                    className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600 text-sm"
                  >
                    Stop
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
