import { Routes, Route, Link, useLocation } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import RulesManager from './pages/RulesManager';
import SkillsManager from './pages/SkillsManager';
import MCPGateway from './pages/MCPGateway';
import Audit from './pages/Audit';
import Sync from './pages/Sync';
import Logs from './pages/Logs';

function NavLink({ to, children }: { to: string; children: React.ReactNode }) {
  const location = useLocation();
  const isActive = location.pathname === to;

  return (
    <Link
      to={to}
      className={`w-full text-left px-6 py-3 block ${
        isActive
          ? 'bg-blue-500 text-white'
          : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
      }`}
    >
      {children}
    </Link>
  );
}

export default function Layout() {
  return (
    <div className="flex min-h-screen bg-gray-100 dark:bg-gray-900">
      <aside className="w-64 bg-white dark:bg-gray-800 shadow-lg">
        <div className="p-6">
          <h1 className="text-xl font-bold text-gray-800 dark:text-white">AI Skill System</h1>
        </div>
        <nav className="mt-6">
          <NavLink to="/">Dashboard</NavLink>
          <NavLink to="/rules">Rules Manager</NavLink>
          <NavLink to="/skills">Skills Manager</NavLink>
          <NavLink to="/mcp">MCP Gateway</NavLink>
          <NavLink to="/audit">Audit</NavLink>
          <NavLink to="/sync">IDE Sync</NavLink>
          <NavLink to="/logs">Logs</NavLink>
        </nav>
      </aside>
      <main className="flex-1">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/rules" element={<RulesManager />} />
          <Route path="/skills" element={<SkillsManager />} />
          <Route path="/mcp" element={<MCPGateway />} />
          <Route path="/audit" element={<Audit />} />
          <Route path="/sync" element={<Sync />} />
          <Route path="/logs" element={<Logs />} />
        </Routes>
      </main>
    </div>
  );
}
