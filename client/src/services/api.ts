const API_BASE = 'http://127.0.0.1:8000/api/v1';

export const api = {
  rules: {
    list: async () => {
      const response = await fetch(`${API_BASE}/rules`);
      return response.json();
    },
    create: async (data: any) => {
      const response = await fetch(`${API_BASE}/rules`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      return response.json();
    },
    update: async (id: number, data: any) => {
      const response = await fetch(`${API_BASE}/rules/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      return response.json();
    },
    delete: async (id: number) => {
      const response = await fetch(`${API_BASE}/rules/${id}`, {
        method: 'DELETE',
      });
      return response;
    },
  },
  skills: {
    list: async () => {
      const response = await fetch(`${API_BASE}/skills`);
      return response.json();
    },
    create: async (data: any) => {
      const response = await fetch(`${API_BASE}/skills`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      return response.json();
    },
  },
  mcp: {
    listServices: async () => {
      const response = await fetch(`${API_BASE}/mcp/services`);
      return response.json();
    },
    startService: async (serviceName: string) => {
      const response = await fetch(`${API_BASE}/mcp/services/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ service_name: serviceName }),
      });
      return response.json();
    },
    stopService: async (serviceName: string) => {
      const response = await fetch(`${API_BASE}/mcp/services/stop`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ service_name: serviceName }),
      });
      return response.json();
    },
  },
};
