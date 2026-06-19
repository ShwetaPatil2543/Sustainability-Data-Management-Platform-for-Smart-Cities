import api from "@/services/api";
import React, { createContext, useContext, useState, useCallback } from "react";

export type UserRole = "admin" | "manager" | "analyst" | "supervisor" | "data_entry";

export interface User {
  id: string;
  name: string;
  email: string;
  role: UserRole;
  avatar?: string;
}

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string, role: UserRole) => Promise<void>;
  updateUser: (updates: Partial<User>) => void;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | null>(null);

const MOCK_USERS: Record<string, User & { password: string }> = {
  "admin@sdmp.com": { id: "1", name: "Sarah Chen", email: "admin@sdmp.com", role: "admin", password: "admin123" },
  "manager@sdmp.com": { id: "2", name: "James Wilson", email: "manager@sdmp.com", role: "manager", password: "manager123" },
  "analyst@sdmp.com": { id: "3", name: "Priya Sharma", email: "analyst@sdmp.com", role: "analyst", password: "analyst123" },
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(() => {
    const stored = localStorage.getItem("sdmp_user");
    return stored ? JSON.parse(stored) : null;
  });

  const login = useCallback(async (email: string, password: string) => {

  const res = await api.post("/token/", {
    username: email,
    password: password
  });

  const access = res.data.access;
  const refresh = res.data.refresh;

  localStorage.setItem("sdmp_token", access);
  localStorage.setItem("sdmp_refresh", refresh);

  // get user details
  const userRes = await api.get("/users/me/");
  const userData = userRes.data;

  setUser(userData);
  localStorage.setItem("sdmp_user", JSON.stringify(userData));

}, []);

  const register = useCallback(async (name: string, email: string, password: string, role: UserRole) => {
  try {
    const res = await api.post("/auth/register/", {
      username: name,
      email: email,
      password: password,
      role: role
    });

    const userData = res.data;

    setUser({
      id: userData.id,
      name: userData.username,
      email: userData.email,
      role: userData.role
    });

    localStorage.setItem("sdmp_user", JSON.stringify(userData));

  } catch (error) {
    console.error("Registration error:", error);
    alert("Registration failed");
  }
}, []);

  const updateUser = useCallback((updates: Partial<User>) => {
    setUser((currentUser) => {
      if (!currentUser) return null;
      const updatedUser = { ...currentUser, ...updates };
      localStorage.setItem("sdmp_user", JSON.stringify(updatedUser));
      return updatedUser;
    });
  }, []);

  const logout = useCallback(() => {
    setUser(null);
    localStorage.removeItem("sdmp_user");
  }, []);

  return (
    <AuthContext.Provider value={{ user, login, register, updateUser, logout, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
};
