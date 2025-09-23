import Calendar from "react-calendar";
import { useMemo } from "react";
import { type Slot } from "./AppointmentsTabs"


type Props = { slots: Slot[] };

export default function CalendarView({ slots }: Props) {
    // Convert slot strings like "15.10.2025" into JS Dates
    const availableDates = useMemo(
        () =>
            slots.map((s) => {
                const [year, month, day] = s.date.split("-");
                return new Date(+year, +month - 1, +day);
            }),
        [slots]
    );
    const tileClassName = ({ date }: { date: Date }) => {
        const isAvailable = availableDates.some(
            (d) => d.toDateString() === date.toDateString()
        );
        return isAvailable
            ? "bg-green-100 text-green-900 font-bold rounded-full"
            : undefined;
    };

    return (
        <div className=" flex flex-col items-center bg-white shadow-lg rounded-xl p-6 w-full">
            <h2 className="self-center text-lg font-semibold text-gray-700 mb-4">
                📅 Appointment Calendar
            </h2>
            <Calendar className="w-full " tileClassName={tileClassName} />
        </div>
    );
}
