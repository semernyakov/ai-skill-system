import { useState, useEffect } from 'react';
import { api } from '../services/api';

export default function SkillsManager() {
  const [skills, setSkills] = useState<any[]>([]);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');

  useEffect(() => {
    loadSkills();
  }, []);

  const loadSkills = async () => {
    const data = await api.skills.list();
    setSkills(data);
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

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Skills Manager</h1>

      <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow mb-6">
        <h2 className="text-xl font-semibold mb-4">Create New Skill</h2>
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

      <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
        <h2 className="text-xl font-semibold mb-4">Skills</h2>
        <div className="space-y-2">
          {skills.map((skill) => (
            <div key={skill.id} className="flex justify-between items-center p-3 bg-gray-50 dark:bg-gray-700 rounded">
              <div>
                <p className="font-medium">{skill.name}</p>
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
    </div>
  );
}
