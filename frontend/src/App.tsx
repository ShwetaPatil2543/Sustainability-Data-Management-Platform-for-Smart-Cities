import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "@/contexts/AuthContext";
import { ThemeProvider } from "@/contexts/ThemeContext";
import { DashboardLayout } from "@/components/layout/DashboardLayout";
import Login from "@/pages/Login";
import Register from "@/pages/Register";
import Dashboard from "@/pages/Dashboard";
import SmartDashboard from "@/components/dashboard/SmartDashboard";
import CarbonEmission from "@/pages/CarbonEmission";

import AirQuality from "@/pages/AirQuality";
import EnergyManagement from "@/pages/EnergyManagement";
import FuelMonitoring from "@/pages/FuelMonitoring";
import AIRecommendation from "@/pages/AIRecommendation";
import Reports from "@/pages/Reports";
import Profile from "@/pages/Profile";
import SettingsPage from "@/pages/SettingsPage";
import WorkflowQueue from "@/pages/WorkflowQueue";
import LandingPage from "@/pages/LandingPage";
import NotFound from "@/pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <ThemeProvider>
      <AuthProvider>
        <TooltipProvider>
          <Toaster />
          <Sonner />
          <BrowserRouter>
            <Routes>
              <Route path="/" element={<LandingPage />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route element={<DashboardLayout />}>
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/dashboard/smart" element={<SmartDashboard />} />
                <Route path="/carbon" element={<CarbonEmission />} />


                <Route path="/air-quality" element={<AirQuality />} />
                <Route path="/energy" element={<EnergyManagement />} />
                <Route path="/fuel" element={<FuelMonitoring />} />
                <Route path="/ai-agent" element={<AIRecommendation />} />
                <Route path="/reports" element={<Reports />} />
                <Route path="/workflow" element={<WorkflowQueue />} />
                <Route path="/profile" element={<Profile />} />
                <Route path="/settings" element={<SettingsPage />} />
              </Route>
              <Route path="*" element={<NotFound />} />
            </Routes>
          </BrowserRouter>
        </TooltipProvider>
      </AuthProvider>
    </ThemeProvider>
  </QueryClientProvider>
);

export default App;
