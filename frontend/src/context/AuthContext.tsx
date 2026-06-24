import React, { createContext, useContext, useState, useEffect } from 'react';

interface AuthContextType {
  name: string | null;
  login: (name: string) => void;
  logout: () => void;
  isSurveyor: boolean;
  setSurveyorMode: (active: boolean) => void;
  checkSession: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType>({} as AuthContextType);

export const AuthProvider: React.FC<{children: React.ReactNode}> = ({ children }) => {
  const [name, setName] = useState<string | null>(localStorage.getItem('name'));
  const [isSurveyor, setIsSurveyor] = useState<boolean>(false);

  const checkSession = async () => {
    try {
      const apiUrl = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '');
      const res = await fetch(`${apiUrl}/api/auth/me`, { credentials: 'include' });
      if (res.ok) {
        const data = await res.json();
        setName(data.name);
        localStorage.setItem('name', data.name);
      } else {
        setName(null);
        localStorage.removeItem('name');
      }
    } catch (e) {
      // ignore
    }
  };

  useEffect(() => {
    if (!isSurveyor) {
      checkSession();
    }
  }, [isSurveyor]);

  const login = (newName: string) => {
    setName(newName);
    setIsSurveyor(false);
    localStorage.setItem('name', newName);
  };

  const logout = async () => {
    try {
      const apiUrl = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '');
      await fetch(`${apiUrl}/api/auth/logout`, { method: 'POST', credentials: 'include' });
    } catch (e) {}
    
    setName(null);
    setIsSurveyor(false);
    localStorage.removeItem('name');
  };

  const setSurveyorMode = async (active: boolean) => {
    setIsSurveyor(active);
    if (active) {
      setName('Demo Surveyor');
      try {
        const apiUrl = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '');
        await fetch(`${apiUrl}/api/auth/demo`, { method: 'POST', credentials: 'include' });
      } catch (e) {}
    } else {
      logout();
    }
  };

  return (
    <AuthContext.Provider value={{ name, login, logout, isSurveyor, setSurveyorMode, checkSession }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
