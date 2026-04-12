import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';

export function useAuth() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const checkAuth = () => {
      const authenticated = api.auth.isAuthenticated();
      setIsAuthenticated(authenticated);
      setLoading(false);
    };

    checkAuth();

    // Listen for storage changes (for multi-tab support)
    const handleStorageChange = () => {
      checkAuth();
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, []);

  const login = async (username: string, password: string) => {
    try {
      await api.auth.login(username, password);
      setIsAuthenticated(true);
      navigate('/');
      return true;
    } catch (error) {
      return false;
    }
  };

  const logout = () => {
    api.auth.logout();
    setIsAuthenticated(false);
    navigate('/login');
  };

  return {
    isAuthenticated,
    loading,
    login,
    logout,
  };
}
