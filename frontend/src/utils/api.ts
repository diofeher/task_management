import { User } from "../contexts/AuthContext";

const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
// TODO: Pass this url as configuration

type FetchOptions = {
  method?: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';
  headers?: Record<string, string>;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  body?: any;
};

export const apiForm = async (endpoint: string, options: FetchOptions = {}) => {
  const { method = 'GET', body } = options;

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    method,
    body: body,
  });

  return response;
};

export const apiFetch = async (endpoint: string, options: FetchOptions = {}) => {
  const { method = 'GET', headers, body } = options;

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    method,
    headers: {
      "Content-Type": "application/json",
      ...headers,
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  return response;
};

export const authHeader = (user: User | null) => {
  const requestHeaders: Record<string, string> = {};
  if(!user) {
    return requestHeaders;
  }
  
  requestHeaders["Authorization"] = `Bearer ${user.access_token}`;
  return requestHeaders;
};
