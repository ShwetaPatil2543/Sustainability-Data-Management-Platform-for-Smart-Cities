import { useEffect, useState } from "react";
import api, { EnergyData, getEnergyData } from "@/services/api"; // import api for POST
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  AreaChart,
  Area,
} from "recharts";

export default function EnergyManagement() {
  const [energyData, setEnergyData] = useState<EnergyData[]>([]);
  const [loading, setLoading] = useState(true);
  const [file, setFile] = useState<File | null>(null);

  // ------------------------
  // Fetch energy data
  // ------------------------
  const fetchData = async () => {
    try {
      setLoading(true);
      const res = await getEnergyData();
      const data = Array.isArray(res.data) ? res.data : [];
      setEnergyData(
        data.map((d) => ({
          id: d.id,
          date: d.date,
          industry: d.industry,
          department: d.department,
          renewable_energy: Number(d.renewable_energy) || 0,
          non_renewable_energy: Number(d.non_renewable_energy) || 0,
          total_energy:
            (Number(d.renewable_energy) || 0) +
            (Number(d.non_renewable_energy) || 0),
        }))
      );
    } catch (err: any) {
      console.error("Energy fetch error:", err.response?.data || err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  // ------------------------
  // Upload CSV/Excel file
  // ------------------------
  const handleUpload = async () => {
    if (!file) {
      alert("Select a CSV or Excel file to upload");
      return;
    }

    try {
      const formData = new FormData();
      formData.append("file", file);

      // ✅ POST to correct endpoint with trailing slash
      const res = await api.post("/energy/upload/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: `Bearer ${localStorage.getItem("sdmp_token")}`,
        },
      });

      if (res.status === 201 || res.status === 200) {
        alert(`Upload successful: ${res.data.created || 0} rows`);
        setFile(null);
        fetchData(); // refresh dashboard
      } else {
        alert(`Upload failed: ${res.data?.message || "Unknown error"}`);
        console.error("Upload response:", res.data);
      }
    } catch (err: any) {
      console.error("Upload failed:", err.response?.data || err.message);
      alert(
        `Upload failed: ${
          err.response?.data?.error || err.response?.data?.detail || err.message
        }`
      );
    }
  };

  // ------------------------
  // Dashboard summary
  // ------------------------
  const totalRenewable = energyData.reduce(
    (sum, d) => sum + (d.renewable_energy || 0),
    0
  );
  const totalNon = energyData.reduce(
    (sum, d) => sum + (d.non_renewable_energy || 0),
    0
  );
  const totalConsumption = totalRenewable + totalNon;
  const renewablePercent =
    totalConsumption > 0 ? Math.round((totalRenewable / totalConsumption) * 100) : 0;

  if (loading) {
    return <div className="p-8 text-center">Loading energy data...</div>;
  }

  return (
    <div className="space-y-6 p-6">
      <div>
        <h1 className="text-2xl font-bold">Energy Management</h1>
        <p className="text-sm text-muted-foreground">
          Monitor electricity consumption and renewable energy adoption
        </p>
      </div>

      {/* File Upload */}
      <div className="flex gap-2">
        <input
          type="file"
          accept=".csv,.xlsx"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />
        <button
          className="px-4 py-2 bg-blue-600 text-white rounded"
          onClick={handleUpload}
        >
          Upload Dataset
        </button>
      </div>

      {/* Dashboard Cards */}
      <div className="grid grid-cols-4 gap-4">
        <div className="p-4 border rounded">
          <h2>Total Consumption</h2>
          <p>{totalConsumption} kWh</p>
        </div>
        <div className="p-4 border rounded">
          <h2>Renewable Share</h2>
          <p>{renewablePercent}%</p>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-2 gap-6">
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={energyData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="renewable_energy" fill="#22c55e" />
            <Bar dataKey="non_renewable_energy" fill="#3b82f6" />
          </BarChart>
        </ResponsiveContainer>

        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={energyData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Area
              type="monotone"
              dataKey="renewable_energy"
              stroke="#22c55e"
              fill="#22c55e"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}