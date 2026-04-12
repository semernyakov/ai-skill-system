const API_BASE = 'http://127.0.0.1:8000/api/v1';

// Token management
const getAuthToken = () => localStorage.getItem('auth_token');
const setAuthToken = (token: string) => localStorage.setItem('auth_token', token);
const removeAuthToken = () => localStorage.removeItem('auth_token');

// Helper to add auth headers
const getAuthHeaders = () => {
  const token = getAuthToken();
  return token ? { 'Authorization': `Bearer ${token}` } : {};
};

export const api = {
  auth: {
    login: async (username: string, password: string) => {
      const response = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Login failed');
      }
      const data = await response.json();
      setAuthToken(data.access_token);
      return data;
    },
    logout: () => {
      removeAuthToken();
    },
    isAuthenticated: () => !!getAuthToken(),
  },
  rules: {
    list: async () => {
      const response = await fetch(`${API_BASE}/rules`, {
        headers: getAuthHeaders(),
      });
      if (!response.ok) throw new Error('Failed to fetch rules');
      return response.json();
    },
    create: async (data: any) => {
      const response = await fetch(`${API_BASE}/rules`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...getAuthHeaders() },
        body: JSON.stringify(data),
      });
      if (!response.ok) throw new Error('Failed to create rule');
      return response.json();
    },
    update: async (id: number, data: any) => {
      const response = await fetch(`${API_BASE}/rules/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json', ...getAuthHeaders() },
        body: JSON.stringify(data),
      });
      if (!response.ok) throw new Error('Failed to update rule');
      return response.json();
    },
    delete: async (id: number) => {
      const response = await fetch(`${API_BASE}/rules/${id}`, {
        method: 'DELETE',
        headers: getAuthHeaders(),
      });
      if (!response.ok) throw new Error('Failed to delete rule');
      return response;
    },
  },
  skills: {
    list: async () => {
      const response = await fetch(`${API_BASE}/skills`, {
        headers: getAuthHeaders(),
      });
      if (!response.ok) throw new Error('Failed to fetch skills');
      return response.json();
    },
    create: async (data: any) => {
      const response = await fetch(`${API_BASE}/skills`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...getAuthHeaders() },
        body: JSON.stringify(data),
      });
      if (!response.ok) throw new Error('Failed to create skill');
      return response.json();
    },
    delete: async (id: number) => {
      const response = await fetch(`${API_BASE}/skills/${id}`, {
        method: 'DELETE',
        headers: getAuthHeaders(),
      });
      if (!response.ok) throw new Error('Failed to delete skill');
      return response;
    },
    sync: async () => {
      const response = await fetch(`${API_BASE}/skills/sync/run`, {
        method: 'POST',
        headers: getAuthHeaders(),
      });
      if (!response.ok) throw new Error('Failed to sync skills');
      return response.json();
    },
    execute: async (id: number, input: any) => {
      const response = await fetch(`${API_BASE}/skills/${id}/execute`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...getAuthHeaders() },
        body: JSON.stringify(input),
      });
      if (!response.ok) throw new Error('Failed to execute skill');
      return response.json();
    },
  },
  mcp: {
    listServices: async () => {
      const response = await fetch(`${API_BASE}/mcp/services`, {
        headers: getAuthHeaders(),
      });
      if (!response.ok) throw new Error('Failed to fetch MCP services');
      return response.json();
    },
    startService: async (serviceName: string) => {
      const response = await fetch(`${API_BASE}/mcp/services/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...getAuthHeaders() },
        body: JSON.stringify({ service_name: serviceName }),
      });
      if (!response.ok) throw new Error('Failed to start service');
      return response.json();
    },
    stopService: async (serviceName: string) => {
      const response = await fetch(`${API_BASE}/mcp/services/stop`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...getAuthHeaders() },
        body: JSON.stringify({ service_name: serviceName }),
      });
      if (!response.ok) throw new Error('Failed to stop service');
      return response.json();
    },
  },
  audit: {
    run: async (type: string) => {
      const response = await fetch(`${API_BASE}/audit/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...getAuthHeaders() },
        body: JSON.stringify({ audit_type: type }),
      });
      if (!response.ok) throw new Error('Failed to run audit');
      return response.json();
    },
  },
  sync: {
    run: async (forceAll: boolean = false) => {
      const response = await fetch(`${API_BASE}/sync`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...getAuthHeaders() },
        body: JSON.stringify({ force_all: forceAll }),
      });
      if (!response.ok) throw new Error('Failed to run sync');
      return response.json();
    },
  },
  logs: {
    view: async (filters: any = {}) => {
      const params = new URLSearchParams();
      if (filters.service) params.append('service', filters.service);
      if (filters.level) params.append('level', filters.level);
      if (filters.limit) params.append('limit', filters.limit.toString());
      const response = await fetch(`${API_BASE}/logs?${params}`, {
        headers: getAuthHeaders(),
      });
      if (!response.ok) throw new Error('Failed to fetch logs');
      return response.json();
    },
  },
};
