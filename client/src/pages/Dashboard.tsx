import { useState, useEffect } from 'react';
import { api } from '../services/api';

export default function Dashboard() {
  const [rules, setRules] = useState<any[]>([]);
  const [skills, setSkills] = useState<any[]>([]);
  const [services, setServices] = useState<any[]>([]);

  useEffect(() => {
    loadAll();
  }, []);

  const loadAll = async () => {
    const [rulesData, skillsData, servicesData] = await Promise.all([
      api.rules.list(),
      api.skills.list(),
      api.mcp.listServices(),
    ]);
    setRules(rulesData);
    setSkills(skillsData);
    setServices(servicesData);
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">AI Skill System Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-2">Rules</h2>
          <p className="text-4xl font-bold">{rules.length}</p>
        </div>
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-2">Skills</h2>
          <p className="text-4xl font-bold">{skills.length}</p>
        </div>
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-2">MCP Services</h2>
          <p className="text-4xl font-bold">{services.length}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">MCP Gateway Services</h2>
          <div className="space-y-2">
            {services.map((service) => (
              <div key={service.name} className="flex justify-between items-center p-3 bg-gray-50 dark:bg-gray-700 rounded">
                <span className="font-medium">{service.name}</span>
                <span className={`px-2 py-1 rounded text-sm ${
                  service.status === 'running' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                }`}>
                  {service.status}
                </span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Recent Rules</h2>
          <div className="space-y-2">
            {rules.slice(0, 5).map((rule) => (
              <div key={rule.id} className="p-3 bg-gray-50 dark:bg-gray-700 rounded">
                <p className="font-medium">{rule.name}</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">{rule.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
