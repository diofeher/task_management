"use client";

import React, { useState } from 'react';

import toast from 'react-hot-toast';
import { useAuth } from '../contexts/AuthContext';

const Register: React.FC = () => {
  const { login } = useAuth();
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [repeatPassword, setRepeatPassword] = useState<string>('');
  const [error, setError] = useState<string>('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    if (username && password) {
        try {
            const success = await login(username, password);
            if(!success) {
                toast.error('Unknown error when registering');
            }
            const success2 = await login(username, password);
            if(!success2) {
              toast.error('Unknown error when logging in');
          }
        } catch(e) {
            toast.error(e.toString());
        }
    } else {
      toast.error('Please fill your username/password');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Username</label>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
      </div>
      <div>
        <label>Password</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>
      <div>
        <label>Repeat Password</label>
        <input
          type="password"
          value={repeatPassword}
          onChange={(e) => setRepeatPassword(e.target.value)}
        />
      </div>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <button type="submit">Register</button>
    </form>
  );
};

export default Register;
