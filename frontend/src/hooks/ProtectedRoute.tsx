import React from "react";
import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../api/AuthContext";

export const ProtectedRoute: React.FC<{ redirectTo?: string }> = ({ redirectTo = "/login" }) => {
    const { user, loading } = useAuth();

    if (loading) return <div className="text-center text-white mt-20">Loading...</div>;

    return user ? <Outlet /> : <Navigate to={redirectTo} replace />;
};


