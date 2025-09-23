export interface Appointment {
  date: string;
  label: string;
  link: string;
}

export interface AppointmentResponse {
  city: string;
  service: string;
  slots: Appointment[];
}

export const city = [
  { value: "Berlin", label: "Berlin" },
  { value: "Munich", label: "Munich" },
]; // Later: expand

export const service = [{ value: "Anmeldung", label: "Anmeldung" }]; // Later: expand
