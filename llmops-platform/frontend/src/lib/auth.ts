import api from './api';
import { AuthResponse, User } from '@/types';

// Helper to safely access localStorage (only on client-side)
const safeLocalStorage = {
  getItem: (key: string): string | null => {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem(key);
  },
  setItem: (key: string, value: string): void => {
    if (typeof window !== 'undefined') {
      localStorage.setItem(key, value);
    }
  },
  removeItem: (key: string): void => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem(key);
    }
  },
};

export const authService = {
  async login(email: string, password: string): Promise<AuthResponse> {
    const response = await api.post<AuthResponse>('/auth/login', { email, password });
    if (response.data.access_token) {
      safeLocalStorage.setItem('token', response.data.access_token);
      safeLocalStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  async register(email: string, username: string, password: string): Promise<AuthResponse> {
    const response = await api.post<AuthResponse>('/auth/register', { email, username, password });
    if (response.data.access_token) {
      safeLocalStorage.setItem('token', response.data.access_token);
      safeLocalStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  logout() {
    safeLocalStorage.removeItem('token');
    safeLocalStorage.removeItem('user');
    if (typeof window !== 'undefined') {
      window.location.href = '/login';
    }
  },

  getCurrentUser(): User | null {
    const userStr = safeLocalStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  },

  isAuthenticated(): boolean {
    return !!safeLocalStorage.getItem('token');
  },
};
