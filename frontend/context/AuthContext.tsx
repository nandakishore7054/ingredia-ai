"use client";

import { createContext, useContext, useEffect, useState } from "react";
import { api } from "@/services/api";
import toast from "react-hot-toast";

type User = {
  id: number;
  name: string;
  email: string;
  favorites: string[];
  history: string[];
};

type AuthContextType = {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
};

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  /* 🔁 Restore session */
  useEffect(() => {
    const t = localStorage.getItem("token");
    const u = localStorage.getItem("user");

    if (t && u) {
      setToken(t);
      try {
        setUser(JSON.parse(u));
      } catch {
        // Handle invalid JSON gracefully
        localStorage.removeItem("user");
        localStorage.removeItem("token");
      }
    }
    setLoading(false);
  }, []);

  /* 🔐 LOGIN */
  const login = async (email: string, password: string) => {
    try {
      const res = await api.post("/auth/login", { email, password });

      const { access_token, user } = res.data;

      setToken(access_token);
      setUser(user);

      localStorage.setItem("token", access_token);
      localStorage.setItem("user", JSON.stringify(user));
      toast.success("Successfully logged in!");
    } catch (err: any) {
      toast.error(err.response?.data?.detail || "Login failed. Please check your credentials.");
      throw err;
    }
  };

  /* 📝 REGISTER + AUTO LOGIN */
  const register = async (name: string, email: string, password: string) => {
    try {
      await api.post("/auth/register", { name, email, password });
      // auto login
      await login(email, password);
    } catch (err: any) {
      toast.error(err.response?.data?.detail || "Registration failed.");
      throw err;
    }
  };

  /* 🚪 LOGOUT */
  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    toast.success("Logged out successfully");
    window.location.href = "/login";
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used inside AuthProvider");
  }
  return ctx;
}
