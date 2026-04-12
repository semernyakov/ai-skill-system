import { useState, useEffect } from 'react';
import { api } from '../services/api';

export default function SkillExecution() {
  const [skills, setSkills] = useState<any[]>([]);
  const [selectedSkill, setSelectedSkill] = useState<number | null>(null);
  const [inputData, setInputData] = useState('{}');
  const [output, setOutput] = useState<any>(null);
  const [executing, setExecuting] = useState(false);

  useEffect(() => {
    loadSkills();
  }, []);

  const loadSkills = async () => {
    const data = await api.skills.list();
    setSkills(data.filter((s: any) => s.active));
  };

  const executeSkill = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedSkill) return;

    setExecuting(true);
    try {
      const input = JSON.parse(inputData);
      const result = await api.skills.execute(selectedSkill, input);
      setOutput(result);
    } catch (error) {
      setOutput({ error: 'Failed to execute skill' });
    } finally {
      setExecuting(false);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Skill Execution</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Select Skill</h2>
          <select
            value={selectedSkill || ''}
            onChange={(e) => setSelectedSkill(Number(e.target.value))}
            className="w-full p-2 border rounded dark:bg-gray-700 dark:border-gray-600 mb-4"
          >
            <option value="">Select a skill...</option>
            {skills.map((skill) => (
              <option key={skill.id} value={skill.id}>
                {skill.name} ({skill.source})
              </option>
            ))}
          </select>

          <h2 className="text-xl font-semibold mb-4">Input Data (JSON)</h2>
          <textarea
            value={inputData}
            onChange={(e) => setInputData(e.target.value)}
            className="w-full p-2 border rounded dark:bg-gray-700 dark:border-gray-600 mb-4 font-mono"
            rows={10}
          />

          <button
            onClick={executeSkill}
            disabled={!selectedSkill || executing}
            className="w-full bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 disabled:opacity-50"
          >
            {executing ? 'Executing...' : 'Execute Skill'}
          </button>
        </div>

        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Output</h2>
          {output ? (
            <pre className="bg-gray-50 dark:bg-gray-900 p-4 rounded overflow-auto max-h-96">
              {JSON.stringify(output, null, 2)}
            </pre>
          ) : (
            <p className="text-gray-500 dark:text-gray-400">Output will appear here</p>
          )}
        </div>
      </div>
    </div>
  );
}
