// src/components/SimplifyText.tsx
import React, { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import api from "../../api/api";

type SummarizePayload = {
    text: string;
    translate_to_en: boolean;
    level: string;
};

type SummarizeResp = {
    simplified_de: string | "This is experimental. Please try again.";
    simplified_en?: string | null;

};



export default function SimplifyText() {
    const [text, setText] = useState("");
    const [translate, setTranslate] = useState(false);
    const [level, setLevel] = useState("A2");
    const [error, setError] = useState<string | null>(null);


    async function postSummarize(payload: SummarizePayload): Promise<SummarizeResp> {
        try {
            const res = await api.post("/summarize", payload);
            setError(null);
            return res.data as SummarizeResp;
        } catch (error: any) {
            setError(error.response?.data?.error || "Summarization failed");
            throw new Error(error.response?.data?.error || "Summarization failed");
        }
    }

    const mutation = useMutation<SummarizeResp, Error, SummarizePayload>({
        mutationFn: postSummarize,
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        mutation.mutate({ text, translate_to_en: translate, level });
    };

    return (
        <div className="max-w-3xl mx-auto p-6 bg-white/80 backdrop-blur-md rounded-2xl shadow-lg space-y-6">
            <h2 className="text-2xl font-bold tracking-tight">Simplify Bureaucratic German</h2>

            {/* Form */}
            <form onSubmit={handleSubmit} className="space-y-4">
                <textarea
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    rows={6}
                    placeholder="Paste the official German text here..."
                    className="w-full border border-gray-300 rounded-xl p-4 shadow-sm focus:ring-2 focus:ring-blue-500 outline-none"
                />

                <div className="flex flex-col md:flex-row items-center gap-4">
                    <label className="flex items-center gap-2 text-gray-700">
                        <input
                            type="checkbox"
                            checked={translate}
                            onChange={(e) => setTranslate(e.target.checked)}
                            className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                        />
                        Translate to English
                    </label>

                    <label className="flex items-center gap-2 text-gray-700">
                        Level:
                        <select
                            value={level}
                            onChange={(e) => setLevel(e.target.value)}
                            className="border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-blue-500 outline-none"
                        >
                            <option value="A2">A2 (Very Simple)</option>
                            <option value="B1">B1 (Clearer)</option>
                            <option value="B2">B2 (More Detailed)</option>
                        </select>
                    </label>

                    <button
                        type="submit"
                        disabled={mutation.isPending || text.trim().length === 0}
                        className="ml-auto px-6 py-2 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-medium shadow hover:opacity-90 transition disabled:opacity-50"
                    >
                        {mutation.isPending ? "Simplifying..." : "Simplify"}
                    </button>
                </div>
            </form>

            {/* Loading */}
            {mutation.isPending && (
                <div className="flex items-center justify-center h-32">
                    <div className="w-10 h-10 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                </div>
            )}


            {/* Error */}
            {error && (
                <p className="text-red-600 bg-red-100 p-3 rounded-xl">
                    {error || "Summarization failed. Try again."}
                </p>
            )}


            {/* Results */}
            {mutation.isSuccess && mutation.data && (
                <div className="space-y-6">
                    <div>
                        <h3 className="text-lg font-semibold mb-2">📘 Simplified German</h3>
                        <div className="p-4 bg-gray-50 rounded-xl shadow-inner whitespace-pre-line">
                            {mutation.data.simplified_de}
                        </div>
                    </div>

                    {mutation.data.simplified_en && (
                        <div>
                            <h3 className="text-lg font-semibold mb-2">🌍 English Translation</h3>
                            <div className="p-4 bg-gray-50 rounded-xl shadow-inner whitespace-pre-line">
                                {mutation.data.simplified_en}
                            </div>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
