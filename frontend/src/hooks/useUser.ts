import { useQuery } from "@tanstack/react-query";
import api from "../api/api";

export function useMe() {
  return useQuery({
    queryKey: ["me"],
    queryFn: async () => {
      const res = await api.get("/users/me");
      return res.data;
    },
    retry: 1,
  });
}
