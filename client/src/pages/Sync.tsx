import { useState } from 'react';
import { api } from '../services/api';

export default function Sync() {
  const [syncing, setSyncing] = useState(false);
  const [lastSync, setLastSync] = useState<string | null>(null);
  const [syncStatus, setSyncStatus] = useState('');
  const [skillSyncing, setSkillSyncing] = useState(false);
  const [skillSyncResult, setSkillSyncResult] = useState<any>(null);

  const handleSync = async (forceAll: boolean = false) => {
    setSyncing(true);
    setSyncStatus('Syncing...');
    try {
      const result = await api.sync.run(forceAll);
      setLastSync(new Date().toISOString());
      setSyncStatus(result.status || 'Sync completed');
    } catch (error) {
      setSyncStatus('Sync failed');
    } finally {
      setSyncing(false);
    }
  };

  const handleSkillSync = async () => {
    setSkillSyncing(true);
    try {
      const result = await api.skills.sync();
      setSkillSyncResult(result);
    } catch (error) {
      setSkillSyncResult({ status: 'error', message: 'Skill sync failed' });
    } finally {
      setSkillSyncing(false);
    }
  };

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-6 text-gray-800 dark:text-white">Synchronization</h2>
      
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-6">
        <h3 className="text-lg font-semibold mb-4 text-gray-700 dark:text-gray-300">IDE Sync</h3>
        {syncStatus && (
          <div className="mb-4 p-3 bg-blue-50 dark:bg-blue-900/20 rounded text-blue-800 dark:text-blue-200">
            {syncStatus}
          </div>
        )}
        {lastSync && (
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
            Last sync: {new Date(lastSync).toLocaleString()}
          </p>
        )}
        <div className="flex gap-4">
          <button
            onClick={() => handleSync(false)}
            disabled={syncing}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
          >
            {syncing ? 'Syncing...' : 'Sync'}
          </button>
          <button
            onClick={() => handleSync(true)}
            disabled={syncing}
            className="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600 disabled:opacity-50"
          >
            {syncing ? 'Syncing...' : 'Force Sync All'}
          </button>
        </div>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-6">
        <h3 className="text-lg font-semibold mb-4 text-gray-700 dark:text-gray-300">Skill Sync (External)</h3>
        {skillSyncResult && (
          <div className="mb-4 p-3 bg-purple-50 dark:bg-purple-900/20 rounded text-purple-800 dark:text-purple-200">
            <p>Status: {skillSyncResult.status}</p>
            {skillSyncResult.synced !== undefined && <p>Synced: {skillSyncResult.synced} skills</p>}
            {skillSyncResult.failed !== undefined && <p>Failed: {skillSyncResult.failed} skills</p>}
          </div>
        )}
        <button
          onClick={handleSkillSync}
          disabled={skillSyncing}
          className="px-4 py-2 bg-purple-500 text-white rounded hover:bg-purple-600 disabled:opacity-50"
        >
          {skillSyncing ? 'Syncing...' : 'Sync Skills from agentskills'}
        </button>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold mb-4 text-gray-700 dark:text-gray-300">IDE Targets</h3>
        <ul className="space-y-2 text-gray-600 dark:text-gray-400">
          <li className="flex items-center gap-2">
            <span className="w-2 h-2 bg-green-500 rounded-full"></span>
            .cursor/ (Cursor IDE)
          </li>
          <li className="flex items-center gap-2">
            <span className="w-2 h-2 bg-green-500 rounded-full"></span>
            .windsurf/ (Windsurf IDE)
          </li>
          <li className="flex items-center gap-2">
            <span className="w-2 h-2 bg-green-500 rounded-full"></span>
            .idea/ (JetBrains IDEs)
          </li>
        </ul>
      </div>
    </div>
  );
}
