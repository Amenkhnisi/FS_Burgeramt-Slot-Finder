import { useState } from "react";
import AppointmentList from "./AppointmentList";
import CalendarView from "./CalendarView";

export type Slot = { date: string, label: string, link: string };
type Props = { slots: Slot[] };


export default function AppointmentsTabs({ slots }: Props) {
    const [activeTab, setActiveTab] = useState<"list" | "calendar">("list");

    return (
        <div className="bg-white shadow-lg rounded-xl p-6">
            {/* Tabs header */}
            <div className="flex border-b mb-4">
                <button
                    onClick={() => setActiveTab("list")}
                    className={`px-4 py-2 font-medium ${activeTab === "list"
                        ? "border-b-2 border-blue-600 text-blue-600"
                        : "text-gray-600 hover:text-gray-800"
                        }`}
                >
                    📋 List View
                </button>
                <button
                    onClick={() => setActiveTab("calendar")}
                    className={`px-4 py-2 font-medium ${activeTab === "calendar"
                        ? "border-b-2 border-blue-600 text-blue-600"
                        : "text-gray-600 hover:text-gray-800"
                        }`}
                >
                    📅 Calendar View
                </button>
            </div>

            {/* Tabs content */}
            {activeTab === "list" ? (
                <AppointmentList slots={slots} />
            ) : (
                <CalendarView slots={slots} />
            )}
        </div>
    );
}
