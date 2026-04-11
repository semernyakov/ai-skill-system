import { useState } from 'react';
import Dashboard from './pages/Dashboard';
import RulesManager from './pages/RulesManager';
import SkillsManager from './pages/SkillsManager';
import MCPGateway from './pages/MCPGateway';
import Audit from './pages/Audit';

type Page = 'dashboard' | 'rules' | 'skills' | 'mcp' | 'audit';

export default function Layout() {
  const [currentPage, setCurrentPage] = useState<Page>('dashboard');

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard />;
      case 'rules':
        return <RulesManager />;
      case 'skills':
        return <SkillsManager />;
      case 'mcp':
        return <MCPGateway />;
      case 'audit':
        return <Audit />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="flex min-h-screen bg-gray-100 dark:bg-gray-900">
      <aside className="w-64 bg-white dark:bg-gray-800 shadow-lg">
        <div className="p-6">
          <h1 className="text-xl font-bold text-gray-800 dark:text-white">AI Skill System</h1>
        </div>
        <nav className="mt-6">
          <button
            onClick={() => setCurrentPage('dashboard')}
            className={`w-full text-left px-6 py-3 ${
              currentPage === 'dashboard'
                ? 'bg-blue-500 text-white'
                : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
            }`}
          >
            Dashboard
          </button>
          <button
            onClick={() => setCurrentPage('rules')}
            className={`w-full text-left px-6 py-3 ${
              currentPage === 'rules'
                ? 'bg-blue-500 text-white'
                : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
            }`}
          >
            Rules Manager
          </button>
          <button
            onClick={() => setCurrentPage('skills')}
            className={`w-full text-left px-6 py-3 ${
              currentPage === 'skills'
                ? 'bg-blue-500 text-white'
                : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
            }`}
          >
            Skills Manager
          </button>
          <button
            onClick={() => setCurrentPage('mcp')}
            className={`w-full text-left px-6 py-3 ${
              currentPage === 'mcp'
                ? 'bg-blue-500 text-white'
                : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
            }`}
          >
            MCP Gateway
          </button>
          <button
            onClick={() => setCurrentPage('audit')}
            className={`w-full text-left px-6 py-3 ${
              currentPage === 'audit'
                ? 'bg-blue-500 text-white'
                : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
            }`}
          >
            Audit
          </button>
        </nav>
      </aside>
      <main className="flex-1">
        {renderPage()}
      </main>
    </div>
  );
}
