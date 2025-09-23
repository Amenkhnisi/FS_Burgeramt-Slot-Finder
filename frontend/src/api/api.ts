import axios from "axios";

const API_BASE = import.meta.env.VITE_BACKEND_URL;
const API_VERSION = import.meta.env.VITE_API_VERSION;
const FULL_API_BASE = `${API_BASE}/${API_VERSION}`;
const VITE_APP_X_KEY = import.meta.env.VITE_APP_X_KEY;

// Create an Axios instance with default settings

const api = axios.create({
  baseURL: `${FULL_API_BASE}`,
  headers: {
    "X-API-KEY": VITE_APP_X_KEY,
  },
  withCredentials: true,
  timeout: 10000,
});
export default api;

// Fetch appointment slots
export async function fetchAppointments(city: string, service: string) {
  try {
    const response = await api.get("/appointments", {
      params: { city, service },
    });
    return response.data;
  } catch (error: any) {
    if (error.response) {
      throw new Error(`API error: ${error.response.status}`);
    }
    throw new Error("Network error. Please try again later.");
  }
}
