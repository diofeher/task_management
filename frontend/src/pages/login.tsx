import React, { useState } from 'react';

import Link from 'next/link';
import toast from 'react-hot-toast';
import { useAuth } from '../contexts/AuthContext';
import { useRouter } from 'next/router';

const Login: React.FC = () => {
  const { login } = useAuth();
  const router = useRouter();
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [error, setError] = useState<string>('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    if (username && password) {
        try {
            const success = await login(username, password);
            if(!success) {
                return;
            }
        } catch(e) {
            toast.error(e.toString());
            return;
        }
        router.push(`/`); // Navigate to the new post page
    } else {
      toast.error('Please fill your username/password');
    }
  };

  return (
    <div className="block">
      <h1>Task Management System</h1>
      <form onSubmit={handleSubmit}>
        <input name="hidden" type="text" style={{display:"none"}} />
        <div className="input-box">
          <label>Username</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div className="input-box">
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <button className="primary" type="submit">Login</button>
        <span>Don&lsquo;t have an account yet? </span><Link className="link" href="/register">Register</Link>
      </form>
    </div>
  );
};

export default Login;
