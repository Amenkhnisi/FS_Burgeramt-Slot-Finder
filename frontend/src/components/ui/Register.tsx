import { useState } from "react";
import api from "../../api/api";
import { useNavigate } from "react-router-dom";

export default function Register() {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const nav = useNavigate();
    const [error, setError] = useState<string | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await api.post("/auth/register", { username, email, password });
            nav("/dashboard");
        } catch (err: any) {
            setError(err?.response?.data?.detail || "Registration failed");
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50 p-6">
            <div className="w-full max-w-md bg-white p-6 rounded-xl shadow">
                <h2 className="text-2xl font-bold mb-4">Register</h2>
                <form onSubmit={handleSubmit} className="space-y-4">
                    <input value={username} onChange={e => setUsername(e.target.value)} required placeholder="Username" className="w-full p-2 border rounded" />
                    <input value={email} onChange={e => setEmail(e.target.value)} placeholder="Email" className="w-full p-2 border rounded" />
                    <input value={password} onChange={e => setPassword(e.target.value)} required type="password" placeholder="Password" className="w-full p-2 border rounded" />
                    <button type="submit" className="w-full py-2 bg-blue-600 text-white rounded">Create account</button>
                </form>
                {error && <p className="mt-3 text-red-600">{error}</p>}
            </div>
        </div>
    );
}
