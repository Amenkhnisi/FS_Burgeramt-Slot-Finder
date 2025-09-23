import { useState } from "react";

type Slot = { date: string; label: string, link: string };
type Props = { slots: Slot[] };

export default function AppointmentList({ slots }: Props) {
    const [page, setPage] = useState(1);
    const perPage = 5; // 🔹 how many slots per page
    const totalPages = Math.ceil(slots.length / perPage);

    const start = (page - 1) * perPage;
    const currentSlots = slots.slice(start, start + perPage);

    return (
        <div className="bg-white shadow-lg rounded-xl p-6">
            <h2 className="text-lg font-semibold mb-4">📋 Available Appointments</h2>

            {slots.length === 0 ? (
                <p className="text-gray-500">No slots available.</p>
            ) : (
                <>
                    {/* Scrollable list */}
                    <div className="max-h-96 overflow-y-auto pr-2">
                        <ul className="space-y-3">
                            {currentSlots.map((slot, i) => (

                                <li
                                    key={i}
                                    className="flex items-center justify-between border-b pb-2"
                                >
                                    <span className="font-medium">{slot.date}</span>
                                    <a
                                        href={slot.link}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="px-4 py-1 bg-blue-600 text-white text-sm rounded-lg shadow hover:bg-blue-700 transition"
                                    >
                                        Book Now
                                    </a>
                                </li>
                            ))}
                        </ul>
                    </div>

                    {/* Pagination controls */}
                    <div className="flex justify-center mt-4 space-x-2">
                        <button
                            onClick={() => setPage((p) => Math.max(p - 1, 1))}
                            disabled={page === 1}
                            className="px-3 py-1 rounded-md bg-gray-200 disabled:opacity-50"
                        >
                            Prev
                        </button>
                        <span className="px-3 py-1">
                            Page {page} of {totalPages}
                        </span>
                        <button
                            onClick={() => setPage((p) => Math.min(p + 1, totalPages))}
                            disabled={page === totalPages}
                            className="px-3 py-1 rounded-md bg-gray-200 disabled:opacity-50"
                        >
                            Next
                        </button>
                    </div>
                </>
            )}
        </div>
    );
}
