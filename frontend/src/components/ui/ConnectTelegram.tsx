import { useEffect, useState } from "react";
import { Button } from "./button";
import Settings from "./Settings";
import api from "../../api/api";


export default function ConnectTelegram() {
    const [loading, setLoading] = useState(false);
    const [isConnected, setIsConnected] = useState(false);


    const handleConnect = async () => {
        try {
            setLoading(true);
            const res = await api.post(
                `/telegram/connect`,
                {},
                { withCredentials: true }
            );
            if (res.data.deep_link) {
                window.open(res.data.deep_link, "_blank");
            }
        } catch (err) {
            console.error("Failed to generate deep link", err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        // You can use this to show a different UI if already connected or not 
        const fetchTelegramInfo = async () => {
            try {
                const res = await api.get(`/telegram/me`, { withCredentials: true });
                if (res.data.chat_id) {
                    setIsConnected(true);
                } else {
                    setIsConnected(false);
                }
            } catch (err) {
                console.error("Failed to fetch telegram info", err);
            }
        };
        fetchTelegramInfo();

    }, []);

    return (
        <div className="flex flex-col items-center gap-4">

            {!isConnected &&
                <>
                    <p className="text-lg text-gray-700">
                        Connect your Telegram to receive daily appointment alerts
                    </p>
                    <Button onClick={handleConnect} disabled={loading}>
                        {loading ? "Connecting..." : "Connect Telegram"}
                    </Button>
                </>
            }

            {isConnected && (
                <>
                    <p className="text-green-600 font-medium">
                        ✅ Connected! You will receive notifications.
                    </p>
                    <Settings />
                </>

            )}
        </div>
    );
}
