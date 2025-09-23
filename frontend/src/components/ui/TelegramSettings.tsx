import { useState } from "react";
import api from "../../api/api";



export default function TelegramSettings() {
    const [telegramId, setTelegramId] = useState("");
    const [notifyTime, setNotifyTime] = useState("09:00");
    const [status, setStatus] = useState("");

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const res = await api.post("/users/register", {
                telegram_chat_id: telegramId,
                notify_time: notifyTime,
            });
            setStatus(res.data.message);
        } catch (err) {
            setStatus("Error registering user");
        }
    };

    return (
        <div className="max-w-md mx-auto p-6 bg-white rounded-2xl shadow-md">
            <h2 className="text-xl font-bold mb-4">Telegram Notifications</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
                <input
                    type="text"
                    placeholder="Enter your Telegram ID"
                    value={telegramId}
                    onChange={(e) => setTelegramId(e.target.value)}
                    className="w-full border rounded-lg p-2"
                    required
                />
                <input
                    type="time"
                    value={notifyTime}
                    onChange={(e) => setNotifyTime(e.target.value)}
                    className="w-full border rounded-lg p-2"
                    required
                />
                <button
                    type="submit"
                    className="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg"
                >
                    Save Settings
                </button>
            </form>
            {status && <p className="mt-3 text-sm text-gray-600">{status}</p>}
        </div>
    );
}
