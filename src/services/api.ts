import axios, { AxiosResponse } from "axios";
import { XMLParser } from "fast-xml-parser";

/* ======================================================
   XML PARSER (if needed for any XML responses)
====================================================== */
const parser = new XMLParser({ ignoreAttributes: false, parseTagValue: true });

/* ======================================================
   BASE URL
====================================================== */
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api";

/* ======================================================
   AXIOS INSTANCE
====================================================== */
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { "Content-Type": "application/json" },
});

/* ======================================================
   TOKEN HANDLING (JWT)
====================================================== */
let isRefreshing = false;
let failedQueue: Array<{ resolve: (token: string) => void; reject: (err: any) => void }> = [];

const processQueue = (error: any, token: string | null = null) => {
  failedQueue.forEach((prom) => (token ? prom.resolve(token) : prom.reject(error)));
  failedQueue = [];
};

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("sdmp_token");
  if (token && config.headers) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (response: AxiosResponse) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => failedQueue.push({ resolve, reject })).then((token) => {
          originalRequest.headers.Authorization = `Bearer ${token}`;
          return api(originalRequest);
        });
      }
      originalRequest._retry = true;
      isRefreshing = true;
      const refresh = localStorage.getItem("sdmp_refresh");
      if (!refresh) {
        logoutUser();
        return Promise.reject(error);
      }

      try {
        const res = await axios.post(`${API_BASE_URL}/token/refresh/`, { refresh });
        const newToken = res.data.access;
        localStorage.setItem("sdmp_token", newToken);
        processQueue(null, newToken);
        originalRequest.headers.Authorization = `Bearer ${newToken}`;
        return api(originalRequest);
      } catch (err) {
        processQueue(err, null);
        logoutUser();
        return Promise.reject(err);
      } finally {
        isRefreshing = false;
      }
    }
    return Promise.reject(error);
  }
);

function logoutUser() {
  localStorage.removeItem("sdmp_token");
  localStorage.removeItem("sdmp_refresh");
  localStorage.removeItem("sdmp_user");
  window.location.href = "/login";
}

/* ======================================================
   TYPES
====================================================== */
export interface Industry { id: number; name: string; location?: string; }
export interface Department { id: number; name: string; industry: number; }

export interface CarbonEmissionData {
  id?: number;
  industry: number;
  department?: number;
  date: string;
  co2_emission: number;
  methane_emission: number;
  nitrous_emission?: number;
  total_emission?: number;
  fuel_type?: string;
  fuel_amount?: number;
  emission_factor?: number;
}

export interface AirQualityData {
  id?: number;
  industry?: number;
  department?: number;
  date: string;
  aqi: number;
  pm25: number;
  pm10: number;
  co2: number;
  no2: number;
  so2: number;
  temperature?: number;
  humidity?: number;
}

export interface EnergyData {
  id?: number;
  industry: number;
  department?: number;
  date: string;
  electricity_consumption: number;
  renewable_energy: number;
  non_renewable_energy: number;
  total_energy?: number;
}

export interface AIRecommendation {
  module: string;
  problem: string;
  action: string;
  impact: string;
}

export interface AIRecommendationResponse {
  recommendations: AIRecommendation[];
}

export interface WorkflowRecord {
  id: number;
  content_type: string;
  object_id: number;
  current_status: string;
  assigned_to: number | null;
}

/* ======================================================
   WORKFLOW API
====================================================== */

export const getWorkflowQueue = () => api.get<WorkflowRecord[]>("/workflow/queue/");
export const approveWorkflow = (workflowId: number) => api.post(`/workflow/${workflowId}/approve/`);
export const rejectWorkflow = (workflowId: number) => api.post(`/workflow/${workflowId}/reject/`);
export const escalateWorkflow = (workflowId: number) => api.post(`/workflow/${workflowId}/escalate/`);

/* ======================================================
   FUEL MONITORING TYPES
====================================================== */

export interface FuelConsumption {
  id?: number;
  industry: number;
  department?: number;
  date: string;
  fuel_type: string;
  quantity: number;
  carbon_emission_factor: number;
  total_emission?: number;
  cost?: number;
}

/* ======================================================
   INDUSTRY API
====================================================== */
export const getIndustries = () => api.get<Industry[]>("/emissions/industries/");
export const getDepartments = (industryId: number) =>
  api.get<Department[]>(`/emissions/industries/${industryId}/departments/`);

/* ======================================================
   CARBON EMISSION API
====================================================== */
export const getCarbonEmissions = () => api.get<CarbonEmissionData[]>("/emissions/");
export const addCarbonEmission = (data: CarbonEmissionData) => api.post("/emissions/", data);
export const updateCarbonEmission = (id: number, data: CarbonEmissionData) => api.put(`/emissions/${id}/`, data);
export const deleteCarbonEmission = (id: number) => api.delete(`/emissions/${id}/`);
export const bulkUploadEmissions = (data: CarbonEmissionData[]) =>
  api.post("/emissions/bulk-upload/", data);

/* ======================================================
   AIR QUALITY API
====================================================== */
export const getAirQuality = () => api.get<AirQualityData[]>("/air-quality/");
export const addAirQualityData = (data: AirQualityData) => api.post("/air-quality/", data);
export const updateAirQualityData = (id: number, data: AirQualityData) => api.put(`/air-quality/${id}/`, data);
export const deleteAirQualityData = (id: number) => api.delete(`/air-quality/${id}/`);
export const uploadAirQuality = (file: File) => {
  const formData = new FormData();
  formData.append("file", file);
  return api.post("/air-quality/upload/", formData, { headers: { "Content-Type": "multipart/form-data" } });
};

/* ======================================================
   ENERGY API
====================================================== */
export const getEnergyData = () => api.get<EnergyData[]>("/energy/");
export const addEnergyData = (data: EnergyData) => api.post("/energy/", data);
export const updateEnergyData = (id: number, data: EnergyData) => api.put(`/energy/${id}/`, data);
export const deleteEnergyData = (id: number) => api.delete(`/energy/${id}/`);
export const uploadEnergyData = (file: File) => {
  const formData = new FormData();
  formData.append("file", file);
  return api.post("/energy/upload/", formData, { headers: { "Content-Type": "multipart/form-data" } });
};

/* ======================================================
   AI RECOMMENDATION API
====================================================== */
export const getAIRecommendations = (query: string) =>
  api.post<AIRecommendationResponse>("/ai/recommendations/", { query });

/* ======================================================
   FUEL MONITORING API
====================================================== */

export const getFuelData = () =>
  api.get<FuelConsumption[]>("/fuel-monitoring/fuel/");

export const addFuelData = (data: FuelConsumption) =>
  api.post("/fuel-monitoring/fuel/", data);

export const updateFuelData = (id: number, data: FuelConsumption) =>
  api.put(`/fuel-monitoring/fuel/${id}/`, data);

export const deleteFuelData = (id: number) =>
  api.delete(`/fuel-monitoring/fuel/${id}/`);

export const uploadFuelData = (file: File) => {
  const formData = new FormData();
  formData.append("file", file);

  return api.post("/fuel-monitoring/upload/", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};

/* ======================================================
   EXPORT DEFAULT
====================================================== */
export default api;