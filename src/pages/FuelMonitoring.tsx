import { useState, useEffect } from "react";
import { getFuelData, uploadFuelData } from "@/services/api";
import {
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend
} from "recharts";
import { DollarSign, Upload } from "lucide-react";

const COLORS = ["#16a34a", "#0284c7", "#f59e0b"];

interface FuelData {
  fuel_type: string;
  value: number;
  cost: number;
  name: string;
}

interface MonthlyFuelData {
  month: string;
  diesel: number;
  petrol: number;
  gas: number;
}

export default function FuelMonitoring() {

  const [fuelData, setFuelData] = useState<FuelData[]>([]);
  const [fuelMonthly, setFuelMonthly] = useState<MonthlyFuelData[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);

  const fetchFuelData = async () => {

    try {

      setLoading(true);

      const res = await getFuelData();
      const data = Array.isArray(res.data) ? res.data : [];

      if (!data.length) {
        setFuelData([]);
        setFuelMonthly([]);
        return;
      }

      const fuelTypes = ["Diesel", "Petrol", "Natural Gas"];

      const aggregated: FuelData[] = fuelTypes.map((type) => {

        const filtered = data.filter((f: any) => f.fuel_type === type);

        const totalQty = filtered.reduce(
          (sum: number, f: any) => sum + Number(f.quantity || 0),
          0
        );

        const totalCost = filtered.reduce(
          (sum: number, f: any) => sum + Number(f.cost || 0),
          0
        );

        return {
          fuel_type: type,
          name: type,
          value: totalQty,
          cost: totalCost
        };

      });

      const totalValue = aggregated.reduce((sum, f) => sum + f.value, 0);

      const normalized = aggregated.map((f) => ({
        ...f,
        value: totalValue ? Math.round((f.value / totalValue) * 100) : 0
      }));

      setFuelData(normalized);

      const monthlyData: { [key: string]: MonthlyFuelData } = {};

      const fuelKeyMap: Record<string, "diesel" | "petrol" | "gas"> = {
        Diesel: "diesel",
        Petrol: "petrol",
        "Natural Gas": "gas"
      };

      data.forEach((f: any) => {

        const month = new Date(f.date).toLocaleString("default", { month: "short" });

        if (!monthlyData[month]) {
          monthlyData[month] = { month, diesel: 0, petrol: 0, gas: 0 };
        }

        const key = fuelKeyMap[f.fuel_type];

        if (key) {
          monthlyData[month][key] += Number(f.quantity || 0);
        }

      });

      const sortedMonths = Object.values(monthlyData).sort(
        (a, b) =>
          new Date(`${a.month} 1`).getMonth() -
          new Date(`${b.month} 1`).getMonth()
      );

      setFuelMonthly(sortedMonths);

    } catch (error) {

      console.error("Fuel API Error:", error);
      setFuelData([]);
      setFuelMonthly([]);

    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFuelData();
  }, []);

  const handleFileUpload = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {

    if (!event.target.files || event.target.files.length === 0) return;

    const file = event.target.files[0];

    setUploading(true);

    try {

      await uploadFuelData(file);

      await fetchFuelData();

    } catch (err) {

      console.error("Upload failed:", err);
      alert("File upload failed");

    } finally {

      setUploading(false);
      event.target.value = "";

    }
  };

  if (loading) return <p>Loading fuel data...</p>;

  const totalCost = fuelData.reduce((sum, f) => sum + (f.cost || 0), 0);

  return (

    <div className="space-y-6">

      <div className="flex justify-between items-center">

        <div>
          <h1 className="text-2xl font-bold">Fuel Monitoring</h1>
          <p className="text-sm text-gray-500">
            Track fuel consumption and cost
          </p>
        </div>

        <label className="flex items-center gap-2 cursor-pointer border px-3 py-1 rounded">

          <Upload size={16} />

          {uploading ? "Uploading..." : "Upload File"}

          <input
            type="file"
            hidden
            accept=".csv,.xlsx,.xls"
            onChange={handleFileUpload}
          />

        </label>

      </div>

      <div className="grid md:grid-cols-3 gap-4">

        {fuelData.map((f, i) => (

          <div key={i} className="border p-4 rounded shadow-sm">

            <div className="flex items-center gap-2">

              <div
                className="h-3 w-3 rounded-full"
                style={{ background: COLORS[i] }}
              />

              <span className="text-sm">{f.fuel_type}</span>

            </div>

            <h2 className="text-xl font-bold mt-2">{f.value}%</h2>

            <div className="text-sm text-gray-500 flex items-center gap-1">

              <DollarSign size={14} />

              ${f.cost.toLocaleString()}

            </div>

          </div>

        ))}

      </div>

      <div className="grid lg:grid-cols-2 gap-6">

        <div className="border p-4 rounded">

          <h3 className="mb-3 text-sm font-semibold">
            Fuel Distribution
          </h3>

          <ResponsiveContainer width="100%" height={280}>

            <PieChart>

              <Pie
                data={fuelData}
                dataKey="value"
                cx="50%"
                cy="50%"
                outerRadius={100}
                label={({ name, value }) => `${name} ${value}%`}
              >

                {fuelData.map((_, i) => (
                  <Cell key={i} fill={COLORS[i]} />
                ))}

              </Pie>

              <Tooltip />

            </PieChart>

          </ResponsiveContainer>

        </div>

        <div className="border p-4 rounded">

          <h3 className="mb-3 text-sm font-semibold">
            Monthly Fuel Usage
          </h3>

          <ResponsiveContainer width="100%" height={280}>

            <BarChart data={fuelMonthly}>

              <CartesianGrid strokeDasharray="3 3" />

              <XAxis dataKey="month" />

              <YAxis />

              <Tooltip />

              <Legend />

              <Bar dataKey="diesel" fill={COLORS[0]} name="Diesel" />

              <Bar dataKey="petrol" fill={COLORS[1]} name="Petrol" />

              <Bar dataKey="gas" fill={COLORS[2]} name="Natural Gas" />

            </BarChart>

          </ResponsiveContainer>

        </div>

      </div>

      <div className="border p-4 rounded">

        <h3 className="text-sm font-semibold mb-3">
          Total Monthly Cost
        </h3>

        <p className="text-3xl font-bold">
          ${totalCost.toLocaleString()}
        </p>

      </div>

    </div>
  );
}