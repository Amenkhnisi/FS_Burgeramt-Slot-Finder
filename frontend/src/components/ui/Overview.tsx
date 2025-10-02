
export default function Overview() {
    return (
        <div className="space-y-6">
            <h2 className="text-2xl font-bold tracking-tight">Project Overview</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="p-6 bg-white/80 backdrop-blur-md rounded-2xl shadow-lg hover:shadow-xl transition">
                    <h3 className="text-lg font-semibold mb-2">Project Info</h3>
                    <ul className="space-y-1 text-gray-700">
                        <li><b>Title:</b> Bürgeramt Slot Finder</li>
                        <li><b>Version:</b> 1.0.0</li>
                        <li><b>Stack:</b> React, FastAPI, PostgreSQL ,OpenAI</li>
                    </ul>
                </div>
                <div className="p-6 bg-white/80 backdrop-blur-md rounded-2xl shadow-lg hover:shadow-xl transition">
                    <h3 className="text-lg font-semibold mb-2">Next Features</h3>
                    <ul className="list-disc pl-6 text-gray-700">
                        <li>Service/region selection</li>
                    </ul>
                </div>

            </div>
        </div>
    );
}
