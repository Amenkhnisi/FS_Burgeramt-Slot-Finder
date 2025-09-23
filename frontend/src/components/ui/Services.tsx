
import { useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { fetchAppointments } from "../../api/api";
import Sidebar from "./Sidebar";
import StatsWidget from "./StatsWidget";
import AppointmentsTabs from "./AppointmentsTabs";
import ChartWidget from "./ChartWidget";


type ApiResponse =
    | { error: string }
    | {
        city: string
        service: string
        slots: []
    };

function logUserAction(action: string) {
    const logs = JSON.parse(localStorage.getItem("logs") || "[]");
    logs.push({ action, timestamp: new Date().toISOString() });
    localStorage.setItem("logs", JSON.stringify(logs));
}


export default function Services() {

    const [city, setCity] = useState(localStorage.getItem("city") || "Berlin");
    const [service, setService] = useState(localStorage.getItem("service") || "Anmeldung");

    const { data, error, isLoading, refetch } = useQuery<ApiResponse>({
        queryKey: ["appointments", city, service],
        queryFn: () => fetchAppointments(city, service),
        retry: 2,
        staleTime: 1000 * 60 * 2, // cache 2 mins

    });



    useEffect(() => {
        localStorage.setItem("city", city);
        localStorage.setItem("service", service);
    }, [city, service]);

    const handleRefresh = () => {
        logUserAction(`Manual refresh: ${city} - ${service}`);
        refetch();
    };


    return (

        <div className="min-h-screen flex flex-col md:flex-row  md:justify-center md:items-center bg-gray-100">
            {/* Sidebar */}
            <div className="md:w-1/4 p-2 md:self-start self-center ">
                <Sidebar
                    city={city}
                    setCity={setCity}
                    service={service}
                    setService={setService}
                />
            </div>

            {/* Main Content */}
            <main className="flex flex-col sm:flex-1 md:flex-1 p-6 space-y-6   max-w-5xl">
                <h1 className="self-center sm:text-base md:text-base lg:text-3xl font-bold text-blue-600">
                    🏛️ Bürgeramt Slot Finder
                </h1>

                <button
                    onClick={() => handleRefresh}
                    disabled={isLoading}
                    className="w-3xs self-center px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-xl shadow disabled:opacity-50"
                >
                    {isLoading ? "Refreshing..." : "🔄 Refresh"}
                </button>

                {error && (
                    <p className="text-red-600 font-medium">
                        ⚠️ {(error as Error).message}
                    </p>
                )}
                {data && "error" in data && (
                    <p className="text-red-600 text-center">{data.error}</p>
                )}
                {
                    data && "slots" in data && (
                        <>
                            <StatsWidget slots={data["slots"]} />
                            <AppointmentsTabs slots={data["slots"]} />
                            <ChartWidget slots={data["slots"]} />


                        </>
                    )

                }


                {data && "slots" in data && Array.isArray(data["slots"]) && data["slots"].length === 0 && (
                    <p className="text-gray-600 text-center">No appointments available.</p>
                )}

            </main>
        </div>
    );


}



