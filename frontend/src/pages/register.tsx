import React, { useState } from 'react';

import { NextResponse } from "next/server";
import { Toaster } from 'react-hot-toast';
import { redirect } from 'next/navigation';
import toast from 'react-hot-toast';
import { useAuth } from '../contexts/AuthContext';
import {useRouter} from 'next/router';

const Register: React.FC = () => {
  const { register, login } = useAuth();
  const router = useRouter();
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [repeatPassword, setRepeatPassword] = useState<string>('');
  const [error, setError] = useState<string>('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    if (username && password) {
        try {
            const success = await register(username, password);
            if(!success) {
                toast.error('Unknown error');
                return;
            }
            const success2 = await login(username, password);
        } catch(e) {
            toast.error(e.toString());
            return;
        };
        router.push(`/tasks/`); // Navigate to the new post page
    } else {
      toast.error('Please fill your username/password');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <Toaster/>
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
