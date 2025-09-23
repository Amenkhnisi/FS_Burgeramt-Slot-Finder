type Props = { slots: Slots[] };

interface Slots {
    date: string
    label: string
    link: string
}
function getStats(slots: Slots[]) {
    const totalSlots = slots.length;

    // Unique days
    const uniqueDays = new Set(
        slots.map((s) => {
            const [year, month, day] = s.date.split("-");
            return `${day}.${month}.${year}`;
        })
    );

    const availableDays = uniqueDays.size;

    // Current month availability
    const now = new Date();
    const currentMonth = now.getMonth();
    const currentYear = now.getFullYear();
    const m = slots.map((s) => s.date)

    const slotsThisMonth = m.filter((s) => {
        const [year, month] = s.split("-");
        return +month - 1 === currentMonth && +year === currentYear;
    });
    console.log(slotsThisMonth)
    const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
    const percentAvailability = Math.round(
        (new Set(m.map((s) => s.split("-"))).size / daysInMonth) *
        100
    );

    return { totalSlots, availableDays, percentAvailability };
}

export default function StatsWidget({ slots }: Props) {
    const { totalSlots, availableDays, percentAvailability } = getStats(slots);

    return (
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="bg-white shadow-lg rounded-xl p-6 text-center ">
                <h3 className="text-gray-500 text-sm">Total Slots</h3>
                <p className="text-2xl font-bold text-blue-600">{totalSlots}</p>
            </div>
            <div className="bg-white shadow-lg rounded-xl p-6 text-center">
                <h3 className="text-gray-500 text-sm">Available Days</h3>
                <p className="text-2xl font-bold text-green-600">{availableDays}</p>
            </div>
            <div className="bg-white shadow-lg rounded-xl p-6 text-center">
                <h3 className="text-gray-500 text-sm">This Month</h3>
                <p className="text-2xl font-bold text-purple-600">
                    {percentAvailability}%
                </p>
            </div>
        </div>
    );
}
