import React, { useState, useEffect } from "react";
import { Bell, Search, Sun, Moon, ChevronDown } from "lucide-react";
import { useAuth } from "../../api/AuthContext";
import { Link, useNavigate } from "react-router-dom";


const Navbar: React.FC = () => {
    const [darkMode, setDarkMode] = useState(true);
    const [open, setOpen] = useState(false);
    const { user, logout } = useAuth()
    const nav = useNavigate();


    const handleLogout = async () => {
        try {
            await logout();         // 👈 Await the logout request
            nav("/");               // Redirect
        } catch (err) {
            console.error("Logout failed:", err);
        }
    };

    useEffect(() => {
        if (darkMode) document.documentElement.classList.add("dark");
        else document.documentElement.classList.remove("dark");
    }, [darkMode]);


    return (
        <div className="flex justify-between items-center p-4 bg-white dark:bg-gray-900 shadow-md relative">
            {/* Search */}
            <div className="flex items-center gap-2 bg-gray-100 dark:bg-gray-700 rounded-md px-2 py-1">
                <Search size={16} className="text-gray-500 dark:text-gray-300" />
                <input
                    type="text"
                    placeholder="Search..."
                    className="bg-transparent outline-none text-gray-700 dark:text-gray-200"
                />
            </div>

            {/* Right Section */}
            <div className="flex items-center gap-4 relative">
                {/* Dark mode toggle */}
                <button
                    onClick={() => setDarkMode(!darkMode)}
                    className="text-gray-600 dark:text-gray-300"
                >
                    {darkMode ? <Sun size={20} /> : <Moon size={20} />}
                </button>

                {/* Notifications */}
                <Bell size={20} className="text-gray-600 dark:text-gray-300 cursor-pointer" />

                {/* User avatar and dropdown */}
                <div className="relative">
                    <button
                        onClick={() => setOpen(!open)}
                        className="flex items-center gap-2"
                    >
                        <div className="w-10 h-10 rounded-full bg-gray-400 dark:bg-gray-600" >
                            {/* Placeholder for user avatar */}
                            <img
                                src={"https://www.shutterstock.com/shutterstock/photos/265136639/display_1500/stock-vector-round-german-flag-vector-icon-isolated-german-flag-button-265136639.jpg"}
                                alt="User Avatar"
                                className="w-full h-full rounded-full object-fill"
                            />
                        </div>
                        <span className="text-gray-700 dark:text-gray-200 font-medium">{user?.username || "Guest"}</span>
                        <ChevronDown size={16} className="text-gray-700 dark:text-gray-200" />
                    </button>

                    {/* Dropdown */}
                    {open && user && (
                        <div className="absolute right-0 mt-2 w-40 bg-white dark:bg-gray-800 shadow-lg rounded-md overflow-hidden z-50">
                            <button
                                onClick={handleLogout}
                                className="block w-full text-left px-4 py-2 text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700"
                            >
                                Logout
                            </button>
                        </div>
                    )}
                    {open && !user && (
                        <div className="absolute right-0 mt-2 w-40 bg-white dark:bg-gray-800 shadow-lg rounded-md overflow-hidden z-50">
                            <Link to="/Login">
                                <button
                                    className="block w-full text-left px-4 py-2 text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700"
                                >
                                    Login
                                </button>
                            </Link >
                        </div>
                    )}

                </div>
            </div>
        </div>
    );
};

export default Navbar;
