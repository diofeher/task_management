"use client";

import { AuthProvider, useAuth } from '../contexts/AuthContext';

import Login from '../components/Login';
import React from 'react';
import TaskInput from '../components/TaskInput';
import TaskList from '../components/TaskList';
import { TaskProvider } from '../contexts/TaskContext';
import { Toaster } from 'react-hot-toast';

const Home: React.FC = () => {
  const { user, logout } = useAuth();
  return (
    <TaskProvider>
      <h1>Welcome, {user?.username}</h1>
      <button onClick={logout}>Logout</button>
      
      <div style={{ padding: '20px' }}>
        <h1>Task Manager</h1>
        <TaskInput />
        <TaskList />
      </div>
    </TaskProvider>
  );
};

const App: React.FC = () => {
  const { user, loading } = useAuth();

  if (loading) return <div>Loading...</div>;

  return user ? <Home /> : <Login />;
};

const WrappedApp: React.FC = () => (

    <App />
);

export default WrappedApp;
