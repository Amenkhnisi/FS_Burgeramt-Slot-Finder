import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { type Slot } from "./AppointmentsTabs"

type ChartDataPoint = {
    date: string;   // e.g. "18.09.2025"
    count: number;  // number of slots available that day
};

type Props = { slots: Slot[] };

function prepareData(slots: Slot[]): ChartDataPoint[] {
    const map = new Map<string, number>();

    slots.forEach(({ date }) => {
        // Expecting YYYY-MM-DD
        const [year, month, day] = date.split("-");
        const formattedDate = `${day}.${month}.${year}`;
        map.set(formattedDate, (map.get(formattedDate) ?? 0) + 1);
    });

    // Return sorted data (chronological order)
    return Array.from(map.entries())
        .map(([date, count]) => ({ date, count }))
        .sort((a, b) => {
            const [dA, mA, yA] = a.date.split(".").map(Number);
            const [dB, mB, yB] = b.date.split(".").map(Number);
            return new Date(yA, mA - 1, dA).getTime() - new Date(yB, mB - 1, dB).getTime();
        });
}

export default function ChartWidget({ slots }: Props) {
    const data = prepareData(slots);

    return (
        <div className="p-6 bg-white dark:bg-gray-800 rounded-xl shadow-md">
            <h2 className="text-lg font-semibold mb-4 text-gray-800 dark:text-gray-200">
                Slots per Day
            </h2>
            <ResponsiveContainer width="100%" height={300}>
                <BarChart data={data}>
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="count" fill="#3b82f6" radius={[6, 6, 0, 0]} />
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
}
