// src/pages/Settings.tsx
import { useState } from "react";
import api from "../../api/api";



export default function Settings() {
    const [time, setTime] = useState("09:00");

    const saveSettings = async () => {
        const res = await api.put(`/telegram/time`, { notify_time: time }, { withCredentials: true });
        if (res.status === 200)
            alert("Settings saved!");
        else
            alert("Failed to save settings.");
    };

    return (
        <div className="space-y-6">
            <h2 className="text-2xl font-bold">Notification Settings</h2>
            <div className="p-6 bg-white/80 backdrop-blur-md rounded-2xl shadow-md space-y-4">
                <label className="block text-gray-700 font-medium">
                    Notification Time:
                    <input
                        type="time"
                        value={time}
                        onChange={(e) => setTime(e.target.value)}
                        className="ml-2 border p-2 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500 outline-none"
                    />
                </label>
                <button
                    onClick={saveSettings}
                    className="px-6 py-2 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-xl shadow hover:opacity-90 transition"
                >
                    Save
                </button>
            </div>
        </div>
    );
}
