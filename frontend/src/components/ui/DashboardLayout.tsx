import { useState } from "react";
import { Link, Outlet } from "react-router-dom";
import { useAuth } from "../../api/AuthContext";
import { useNavigate } from "react-router-dom";

export default function DashboardLayout() {
    const { logout, user, loading } = useAuth();
    const nav = useNavigate();
    const [sidebarOpen, setSidebarOpen] = useState(false);

    const handleLogout = async () => {
        try {
            await logout();         // 👈 Await the logout request
            nav("/");               // Redirect
        } catch (err) {
            console.error("Logout failed:", err);
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center h-screen bg-gray-100">
                <div className="w-12 h-12 border-4 border-blue-400 border-t-transparent rounded-full animate-spin"></div>
            </div>
        );
    }


    return (
        <div className="flex h-screen bg-gradient-to-br from-gray-50 to-gray-100 text-gray-900">
            {/* Sidebar */}
            <aside
                className={`fixed inset-y-0 left-0 z-30 w-72 backdrop-blur-md bg-white/80 shadow-xl transform 
        ${sidebarOpen ? "translate-x-0" : "-translate-x-full"} 
        transition-transform duration-300 ease-in-out md:translate-x-0 md:static md:flex md:flex-col`}
            >
                <div className="p-6 text-2xl font-extrabold border-b border-gray-200 flex justify-between items-center">
                    <Link to={"/"} > Bürgeramt</Link>
                    <button
                        onClick={() => setSidebarOpen(false)}
                        className="md:hidden px-2 py-1 text-gray-500 hover:text-gray-800"
                    >
                        ✖
                    </button>
                </div>
                <nav className="flex-1 p-6 space-y-3">
                    <Link
                        to="/dashboard"
                        className="block p-3 rounded-xl hover:bg-blue-100 transition"
                        onClick={() => setSidebarOpen(false)}
                    >
                        <div className="inline-flex items-center gap-2">

                            <img width="48" height="48" src="https://img.icons8.com/fluency/48/overview-pages-2.png" alt="overview-pages-2" /> Übersicht                        </div>

                    </Link>
                    <Link
                        to="/dashboard/appointments"
                        className="block p-3 rounded-xl hover:bg-blue-100 transition"
                        onClick={() => setSidebarOpen(false)}
                    >
                        <div className="inline-flex items-center gap-2">

                            <img width="48" height="48" src="https://img.icons8.com/fluency/48/tear-off-calendar.png" alt="tear-off-calendar" /> Termine                        </div>

                    </Link>
                    <Link
                        to="/dashboard/TelegramBot"
                        className="block p-3 rounded-xl hover:bg-blue-100 transition"
                        onClick={() => setSidebarOpen(false)}
                    >
                        <div className="inline-flex items-center gap-2">

                            <img width="48" height="48" src="https://img.icons8.com/color/48/telegram-app--v1.png" alt="telegram-app--v1" /> Telegram Bot                         </div>
                    </Link>
                    <Link
                        to="/dashboard/Ai-simplifier"
                        className="block p-3 rounded-xl hover:bg-blue-100 transition"
                        onClick={() => setSidebarOpen(false)}
                    >
                        <div className="inline-flex items-center gap-2">

                            <img width="48" height="48" src="https://img.icons8.com/color/48/bot.png" alt="bot" />  Ai Simplifier
                        </div>
                    </Link>
                </nav>
            </aside>

            {/* Main content */}
            <div className="flex-1 flex flex-col overflow-hidden">
                {/* Navbar */}
                <header className="flex justify-between items-center bg-white/70 backdrop-blur-md shadow-md p-4">
                    <div className="flex items-center gap-4">
                        <button
                            className="md:hidden px-2 py-1 border rounded-lg shadow-sm"
                            onClick={() => setSidebarOpen(!sidebarOpen)}
                        >
                            ☰
                        </button>
                        <h1 className="text-xl font-semibold tracking-tight">
                            {user ? `Welcome,  ${user.username}` : "Dashboard"}
                        </h1>
                    </div>
                    <button
                        onClick={handleLogout}
                        className="px-4 py-2 bg-gradient-to-r from-red-500 to-pink-500 text-white rounded-xl shadow hover:opacity-90 transition"
                    >
                        Logout
                    </button>
                </header>

                {/* Page content */}
                <main className="flex-1 overflow-y-auto p-8">
                    <Outlet />
                </main>
            </div>
        </div>
    );
}
