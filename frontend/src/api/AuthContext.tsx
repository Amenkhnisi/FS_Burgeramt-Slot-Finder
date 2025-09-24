// src/context/AuthContext.tsx
import { createContext, useContext, useState, useEffect } from "react";
import { useQueryClient } from "@tanstack/react-query";
import api from "./api";

interface User {
    id: string;
    username: string;
    email: string;
}

interface AuthContextType {
    user: User | null;
    loading: boolean;
    login: (data: { username: string; password: string }) => Promise<void>;
    register: (data: { username: string; email: string; password: string }) => Promise<void>;
    logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);



export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const queryClient = useQueryClient();
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true); // 👈 Track loading manually

    // Query for current user
    const fetchUser = async () => {
        try {
            const res = await api.get("/users/me", {
                withCredentials: true,
            });
            setUser(res.data);
        } catch (err: any) {
            if (err.response?.status === 401) {
                // Try refreshing token
                try {
                    await api.post(`/auth/refresh`, {}, {
                        withCredentials: true,
                    });
                    const res = await api.get(`/users/me`, {
                        withCredentials: true,
                    });
                    setUser(res.data);
                } catch {
                    console.error("Refresh failed");
                    setUser(null);
                }
            } else {
                console.error("Fetch user failed:", err);
                setUser(null);
            }
        } finally {
            setLoading(false); // ✅ Done loading
        }
    };

    useEffect(() => {
        fetchUser(); // ✅ Only call this once on mount
    }, []);






    // Login function
    const login = async (data: { username: string; password: string }) => {
        await api.post("/auth/login", data, {
            withCredentials: true, // 👈 Cookie is set automatically
        });

        await fetchUser();; // Rehydrate user after login
    };

    // Register function
    const registerUser = async (data: { username: string; email: string; password: string }) => {
        try {
            await api.post(`/auth/register`, data, {
                withCredentials: true,
            });

            await fetchUser();; // Rehydrate user after login
        } catch (err) {
            console.error("Registration failed:", err);
            throw err;
        }
    };

    // Logout function
    const logout = async () => {
        await api.post(`/auth/logout`, {}, {
            withCredentials: true,
        });
        setUser(null);
        queryClient.clear();    // Optional: clear cached queries
        // Clear user state
    };

    return (
        <AuthContext.Provider value={{ user, loading: loading, login, register: registerUser, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = (): AuthContextType => {
    const context = useContext(AuthContext);
    if (!context) throw new Error("useAuth must be used inside AuthProvider");
    return context;
};
