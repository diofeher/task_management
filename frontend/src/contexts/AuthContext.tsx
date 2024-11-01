"use client";

import React, { ReactNode, createContext, useContext, useEffect, useState } from 'react';
import { apiFetch, apiForm } from "../utils/api";

import toast from 'react-hot-toast';

export interface User {
  id: number;
  username: string;
  access_token: string;
}

interface AuthContextType {
  user: User | null;
  login: (username: string, password: string) => Promise<boolean>;
  register: (username: string, password: string) => Promise<boolean>;
  logout: () => void;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
    setLoading(false);
  }, []);

  const login = async (username: string, password: string): Promise<boolean> => {
    const body = new URLSearchParams();
    body.append("username", username);
    body.append("password", password);
    
    const response = await apiForm('/users/token', {
      method: 'POST',
      body
    });

    const data = await response.json();
    if(response.status != 200) {
      toast.error(data.detail);
      return false;
    }
    
    if (data.username) {      
      const newUser: User = { id: data.id, username: data.username, access_token: data.access_token };
      setUser(newUser);
      localStorage.setItem('user', JSON.stringify(newUser));
      return true;
    } else {
      return false;
    }
  };

  const register = async (username: string, password: string): Promise<boolean> => {    
    const response = await apiFetch('/users', {
      method: 'POST',
      body: {username, password}
    });

    const data = await response.json();
    if(response.status != 200) {
      toast.error(data.detail);
      return false;
    }
    
    if (data.username) {
      const newUser: User = { id: data.id, username: data.username, access_token: data.access_token };
      setUser(newUser);
      localStorage.setItem('user', JSON.stringify(newUser));
      return true;
    } else {
      return false;
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('user');
  };

  return (
    <AuthContext.Provider value={{ user, login, register, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
