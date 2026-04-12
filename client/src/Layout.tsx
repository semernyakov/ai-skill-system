import { Routes, Route, Link, useLocation, Navigate } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import RulesManager from './pages/RulesManager';
import SkillsManager from './pages/SkillsManager';
import MCPGateway from './pages/MCPGateway';
import Audit from './pages/Audit';
import Sync from './pages/Sync';
import Logs from './pages/Logs';
import Login from './pages/Login';
import Register from './pages/Register';
import { useAuth } from './hooks/useAuth';

function NavLink({ to, children }: { to: string; children: React.ReactNode }) {
  const location = useLocation();
  const isActive = location.pathname === to;

  return (
    <Link
      to={to}
      className={`w-full text-left px-6 py-3 block text-[16px] ${
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
  const { isAuthenticated, loading, logout } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100 dark:bg-gray-900">
        <div className="text-[16px] text-gray-600 dark:text-gray-400">Loading...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    );
  }

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
        <div className="mt-6 px-6">
          <button
            onClick={logout}
            className="w-full px-6 py-3 text-[16px] text-left text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
          >
            Logout
          </button>
        </div>
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
          <Route path="/login" element={<Navigate to="/" replace />} />
          <Route path="/register" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  );
}
