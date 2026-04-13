import { useState, useEffect } from 'react';
import { api } from '../services/api';

export default function SkillsManager() {
  const [skills, setSkills] = useState<any[]>([]);
  const [externalSkills, setExternalSkills] = useState<any[]>([]);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [filter, setFilter] = useState<'all' | 'internal' | 'agentskills'>('all');
  const [selectedExternalSkill, setSelectedExternalSkill] = useState<any>(null);
  const [validationResult, setValidationResult] = useState<any>(null);
  const [skillProperties, setSkillProperties] = useState<any>(null);
  const [generatedPrompt, setGeneratedPrompt] = useState<any>(null);

  useEffect(() => {
    loadSkills();
    loadExternalSkills();
  }, []);

  const loadSkills = async () => {
    const data = await api.skills.list();
    setSkills(data);
  };

  const loadExternalSkills = async () => {
    try {
      const data = await api.externalSkills.list();
      setExternalSkills(data);
    } catch (error) {
      console.error('Failed to load external skills:', error);
    }
  };

  const createSkill = async (e: React.FormEvent) => {
    e.preventDefault();
    await api.skills.create({ name, description });
    setName('');
    setDescription('');
    loadSkills();
  };

  const deleteSkill = async (id: number) => {
    await api.skills.delete(id);
    loadSkills();
  };

  const validateExternalSkill = async (skillPath: string) => {
    try {
      const result = await api.externalSkills.validate(skillPath);
      setValidationResult(result);
    } catch (error) {
      console.error('Failed to validate skill:', error);
    }
  };

  const readSkillProperties = async (skillPath: string) => {
    try {
      const props = await api.externalSkills.readProperties(skillPath);
      setSkillProperties(props);
    } catch (error) {
      console.error('Failed to read skill properties:', error);
    }
  };

  const generatePromptForSkills = async (skillPaths: string[]) => {
    try {
      const result = await api.externalSkills.generatePrompt(skillPaths);
      setGeneratedPrompt(result);
    } catch (error) {
      console.error('Failed to generate prompt:', error);
    }
  };

  const filteredSkills = skills.filter(skill => {
    if (filter === 'all') return true;
    return skill.source === filter;
  });

  const getSourceBadge = (source: string) => {
    if (source === 'agentskills') {
      return <span className="bg-purple-100 text-purple-800 text-xs px-2 py-1 rounded">External</span>;
    }
    return <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">Internal</span>;
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Skills Manager</h1>

      <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow mb-6">
        <h2 className="text-xl font-semibold mb-4">Create New Internal Skill</h2>
        <form onSubmit={createSkill} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Name</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full p-2 border rounded dark:bg-gray-700 dark:border-gray-600"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Description</label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full p-2 border rounded dark:bg-gray-700 dark:border-gray-600"
              required
              rows={3}
            />
          </div>
          <button
            type="submit"
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          >
            Create Skill
          </button>
        </form>
      </div>

      <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow mb-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">Internal Skills</h2>
          <div className="space-x-2">
            <button
              onClick={() => setFilter('all')}
              className={`px-3 py-1 rounded text-sm ${filter === 'all' ? 'bg-gray-800 text-white' : 'bg-gray-200'}`}
            >
              All
            </button>
            <button
              onClick={() => setFilter('internal')}
              className={`px-3 py-1 rounded text-sm ${filter === 'internal' ? 'bg-gray-800 text-white' : 'bg-gray-200'}`}
            >
              Internal
            </button>
            <button
              onClick={() => setFilter('agentskills')}
              className={`px-3 py-1 rounded text-sm ${filter === 'agentskills' ? 'bg-gray-800 text-white' : 'bg-gray-200'}`}
            >
              External
            </button>
          </div>
        </div>
        <div className="space-y-2">
          {filteredSkills.map((skill) => (
            <div key={skill.id} className="flex justify-between items-center p-3 bg-gray-50 dark:bg-gray-700 rounded">
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <p className="font-medium">{skill.name}</p>
                  {getSourceBadge(skill.source)}
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-400">{skill.description}</p>
              </div>
              <button
                onClick={() => deleteSkill(skill.id)}
                className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600 text-sm"
              >
                Delete
              </button>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">External Skills (agentskills)</h2>
          <button
            onClick={loadExternalSkills}
            className="bg-gray-500 text-white px-3 py-1 rounded hover:bg-gray-600 text-sm"
          >
            Refresh
          </button>
        </div>
        <div className="space-y-2 mb-6">
          {externalSkills.map((skill, index) => (
            <div key={index} className="flex justify-between items-center p-3 bg-gray-50 dark:bg-gray-700 rounded">
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <p className="font-medium">{skill.name}</p>
                  {getSourceBadge(skill.source)}
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-400">{skill.description}</p>
                <p className="text-xs text-gray-500 dark:text-gray-500">Path: {skill.path}</p>
              </div>
              <div className="space-x-2">
                <button
                  onClick={() => validateExternalSkill(skill.path)}
                  className="bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600 text-sm"
                >
                  Validate
                </button>
                <button
                  onClick={() => readSkillProperties(skill.path)}
                  className="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600 text-sm"
                >
                  Properties
                </button>
              </div>
            </div>
          ))}
        </div>

        {validationResult && (
          <div className="mt-4 p-4 bg-gray-50 dark:bg-gray-700 rounded">
            <h3 className="font-semibold mb-2">Validation Result</h3>
            <pre className="text-sm overflow-x-auto">
              {validationResult.success ? '✅ Valid' : '❌ Invalid'}
              {validationResult.output && <div className="mt-2">{validationResult.output}</div>}
              {validationResult.error && <div className="mt-2 text-red-500">{validationResult.error}</div>}
            </pre>
          </div>
        )}

        {skillProperties && (
          <div className="mt-4 p-4 bg-gray-50 dark:bg-gray-700 rounded">
            <h3 className="font-semibold mb-2">Skill Properties</h3>
            <pre className="text-sm overflow-x-auto">{JSON.stringify(skillProperties, null, 2)}</pre>
          </div>
        )}

        {generatedPrompt && (
          <div className="mt-4 p-4 bg-gray-50 dark:bg-gray-700 rounded">
            <h3 className="font-semibold mb-2">Generated Prompt</h3>
            <pre className="text-sm overflow-x-auto whitespace-pre-wrap">{generatedPrompt.prompt}</pre>
          </div>
        )}
      </div>
    </div>
  );
}
