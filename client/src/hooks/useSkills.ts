import { useState, useEffect } from 'react';
import { api } from '../services/api';

export function useSkills() {
  const [skills, setSkills] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadSkills = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.skills.list();
      setSkills(data);
    } catch (err) {
      setError('Failed to load skills');
    } finally {
      setLoading(false);
    }
  };

  const createSkill = async (skillData: any) => {
    setLoading(true);
    setError(null);
    try {
      const newSkill = await api.skills.create(skillData);
      setSkills([...skills, newSkill]);
      return newSkill;
    } catch (err) {
      setError('Failed to create skill');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const deleteSkill = async (id: number) => {
    setLoading(true);
    setError(null);
    try {
      await api.skills.delete(id);
      setSkills(skills.filter(s => s.id !== id));
    } catch (err) {
      setError('Failed to delete skill');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const syncSkills = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await api.skills.sync();
      await loadSkills();
      return result;
    } catch (err) {
      setError('Failed to sync skills');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const executeSkill = async (id: number, input: any) => {
    setLoading(true);
    setError(null);
    try {
      const result = await api.skills.execute(id, input);
      return result;
    } catch (err) {
      setError('Failed to execute skill');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSkills();
  }, []);

  return {
    skills,
    loading,
    error,
    loadSkills,
    createSkill,
    deleteSkill,
    syncSkills,
    executeSkill,
  };
}
