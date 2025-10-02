import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.tsx";
import { RouterProvider, createBrowserRouter, Navigate } from "react-router-dom";
import LandingPage from "./components/ui/LandingPage.tsx";
import Services from "./components/ui/Services.tsx";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import AuthPage from "./components/ui/AuthPage.tsx";
import { ProtectedRoute } from "./hooks/ProtectedRoute.tsx";
import { AuthProvider } from "./api/AuthContext.tsx";
import DashboardLayout from "./components/ui/DashboardLayout.tsx";
import Overview from "./components/ui/Overview.tsx";
import ConnectTelegram from "./components/ui/ConnectTelegram.tsx";
import SimplifyText from "./components/ui/SimplifyText.tsx";


const queryClient = new QueryClient();

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      {
        path: "/",
        element: <LandingPage />,
      },
      {
        path: "/services",
        element: <Services />,
      },
    ],
  },
  { path: "/login", element: <AuthPage /> },

  {
    path: "/dashboard",
    element: <ProtectedRoute />, // wrap with ProtectedRoute
    children: [
      {
        element: <DashboardLayout />, // layout wraps all child pages
        children: [
          { index: true, element: <Overview /> },
          { path: "appointments", element: <Services /> },
          { path: "TelegramBot", element: <ConnectTelegram /> },
          { path: "Ai-simplifier", element: <SimplifyText /> }
        ],
      },
    ],
  },
  { path: "*", element: <Navigate to="/login" /> },

]);

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <AuthProvider >
        <RouterProvider router={router} />
      </AuthProvider>
    </QueryClientProvider>
  </StrictMode>
);
