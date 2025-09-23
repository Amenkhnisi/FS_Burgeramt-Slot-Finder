type Props = {
    city: string;
    setCity: (c: string) => void;
    service: string;
    setService: (s: string) => void;
};

const cities = ["Berlin", "Hamburg", "Munich"];
const services = ["Anmeldung", "Pass", "Führerschein"];

export default function Sidebar({ city, setCity, service, setService }: Props) {
    return (
        <aside className="w-full md:w-64 bg-white shadow-lg rounded-xl p-6">
            <h2 className="text-xl font-semibold text-blue-600 mb-4">Filters</h2>

            <div className="mb-4">
                <label className="block text-gray-700 font-medium mb-1">City</label>
                <select
                    value={city}
                    onChange={(e) => setCity(e.target.value)}
                    className="w-full p-2 border rounded-lg"
                >
                    {cities.map((c) => (
                        <option key={c}>{c}</option>
                    ))}
                </select>
            </div>

            <div>
                <label className="block text-gray-700 font-medium mb-1">Service</label>
                <select
                    value={service}
                    onChange={(e) => setService(e.target.value)}
                    className="w-full p-2 border rounded-lg"
                >
                    {services.map((s) => (
                        <option key={s}>{s}</option>
                    ))}
                </select>
            </div>
        </aside>
    );
}
