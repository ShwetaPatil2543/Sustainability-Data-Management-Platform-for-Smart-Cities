import { useEffect, useState } from "react";
import { Factory, Wind, Zap, Fuel, Target } from "lucide-react";
import { KpiCard } from "@/components/dashboard/KpiCard";
import { kpiData, energyData as fallbackEnergyData, fuelData as fallbackFuelData, recentActivities } from "@/data/mockData";
import api, { getCarbonEmissions, getAirQuality, getEnergyData, getWorkflowQueue } from "@/services/api";
import { useAuth } from "@/contexts/AuthContext";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  Cell,
  PieChart,
  Pie,
  BarChart,
  Bar,
} from "recharts";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

const CHART_COLORS = ["hsl(152,58%,38%)", "hsl(199,70%,48%)", "hsl(38,92%,50%)"];

const activityBadge: Record<string, string> = {
  report: "secondary",
  alert: "destructive",
  update: "default",
  entry: "outline",
  success: "default",
};

// -----------------------------
// Types
// -----------------------------
interface CarbonEmission {
  date: string;
  total_emission: number;
}

interface AirQuality {
  date: string;
  AQI: number;
}

interface EnergyRow {
  month: string;
  renewable: number;
  nonRenewable: number;
}

interface FuelRow {
  name: string;
  value: number;
}

interface Activity {
  id: string | number;
  action: string;
  user: string;
  time: string;
  type: string;
}

export default function Dashboard() {
  const { user } = useAuth();

  const [carbonData, setCarbonData] = useState<{ total: number; trends: { date: string; total: number }[] }>({
    total: 0,
    trends: [],
  });
  const [airQualityData, setAirQualityData] = useState<{ aqi: number; trends: { date: string; AQI: number }[] }>({
    aqi: 0,
    trends: [],
  });

  const [energyData, setEnergyData] = useState<EnergyRow[]>([]);
  const [fuelData, setFuelData] = useState<FuelRow[]>([]);
  const [activities, setActivities] = useState<Activity[]>([]);

  const [energyUsage, setEnergyUsage] = useState({ value: 0, change: 0 });
  const [fuelConsumption, setFuelConsumption] = useState({ value: 0, change: 0 });
  const [sustainabilityScore, setSustainabilityScore] = useState({ value: 0, change: 0 });
  const [workflowPendingCount, setWorkflowPendingCount] = useState(0);

  const [loading, setLoading] = useState({ carbon: true, aqi: true, energy: true, fuel: true, score: true, activities: true, workflow: true });
  const [error, setError] = useState({ carbon: "", aqi: "", energy: "", fuel: "", score: "", activities: "", workflow: "" });

  const fetchCarbonData = async () => {
    setLoading((prev) => ({ ...prev, carbon: true }));
    try {
      const res = await getCarbonEmissions();
      const data: CarbonEmission[] = Array.isArray(res.data) ? res.data : ((res.data as any).results || []);
      const total = data.reduce((sum, r) => sum + (r.total_emission ?? 0), 0);
      const trends = data.map((r) => ({ date: r.date, total: r.total_emission ?? 0 })).reverse();
      setCarbonData({ total, trends });
      setError((prev) => ({ ...prev, carbon: "" }));
    } catch (err) {
      console.error("Failed to fetch carbon data:", err);
      setError((prev) => ({ ...prev, carbon: "Failed to load carbon data" }));
      setCarbonData({ total: 0, trends: [] });
    } finally {
      setLoading((prev) => ({ ...prev, carbon: false }));
    }
  };

  const fetchAirQualityData = async () => {
    setLoading((prev) => ({ ...prev, aqi: true }));
    try {
      const res = await getAirQuality();
      const data: AirQuality[] = Array.isArray(res.data) ? res.data : ((res.data as any).results || []);
      if (data.length > 0) {
        const latest = data[data.length - 1];
        const aqi = latest?.AQI ?? 0;
        const trends = data.map((r) => ({ date: r.date, AQI: r.AQI ?? 0 })).reverse();
        setAirQualityData({ aqi, trends });
      }
      setError((prev) => ({ ...prev, aqi: "" }));
    } catch (err) {
      console.error("Failed to fetch AQI data:", err);
      setError((prev) => ({ ...prev, aqi: "Failed to load AQI data" }));
      setAirQualityData({ aqi: 0, trends: [] });
    } finally {
      setLoading((prev) => ({ ...prev, aqi: false }));
    }
  };

  const fetchEnergyData = async () => {
    setLoading((prev) => ({ ...prev, energy: true }));
    try {
      const res = await getEnergyData();
      const rows = Array.isArray(res.data) ? res.data : ((res.data as any).results || []);
      // map backend energy shape to chart shape
      const mapped: EnergyRow[] = rows.slice(-12).map((r: any, idx: number) => ({
        month: r.month || new Date(r.date || Date.now()).toLocaleString("default", { month: "short" }),
        renewable: r.renewable_energy ?? r.renewable ?? 0,
        nonRenewable: r.non_renewable_energy ?? r.nonRenewable ?? 0,
      }));
      if (mapped.length) {
        setEnergyData(mapped);
        const total = mapped.reduce((s, m) => s + (m.renewable + m.nonRenewable), 0);
        setEnergyUsage({ value: Math.round(total), change: 0 });
      } else {
        // fallback to bundled mock data
        const fb = fallbackEnergyData.map((d: any) => ({ month: d.month, renewable: d.renewable, nonRenewable: d.nonRenewable }));
        setEnergyData(fb);
        const total = fb.reduce((s, m) => s + (m.renewable + m.nonRenewable), 0);
        setEnergyUsage({ value: Math.round(total), change: 0 });
      }
      setError((prev) => ({ ...prev, energy: "" }));
    } catch (err) {
      console.error("Failed to fetch energy data:", err);
      setError((prev) => ({ ...prev, energy: "Failed to load energy data" }));
      setEnergyData([]);
    } finally {
      setLoading((prev) => ({ ...prev, energy: false }));
    }
  };

  const fetchFuelData = async () => {
    setLoading((prev) => ({ ...prev, fuel: true }));
    try {
      // attempt to fetch fuel distribution - endpoint may vary
      const res = await api.get('/fuel/').catch(() => null);
      const rows = res ? (Array.isArray(res.data) ? res.data : ((res.data as any).results || [])) : [];
      const mapped: FuelRow[] = rows.length
        ? rows.map((r: any) => ({ name: r.name || r.type, value: r.value ?? r.percentage ?? 0 }))
        : [];
      if (mapped.length) {
        setFuelData(mapped);
        const total = mapped.reduce((s, m) => s + (m.value || 0), 0);
        setFuelConsumption({ value: Math.round(total), change: 0 });
      } else {
        const fb = fallbackFuelData.map((d: any) => ({ name: d.name, value: d.value }));
        setFuelData(fb);
        const total = fb.reduce((s, m) => s + (m.value || 0), 0);
        setFuelConsumption({ value: Math.round(total), change: 0 });
      }
      setError((prev) => ({ ...prev, fuel: "" }));
    } catch (err) {
      console.error("Failed to fetch fuel data:", err);
      setError((prev) => ({ ...prev, fuel: "Failed to load fuel data" }));
      setFuelData([]);
    } finally {
      setLoading((prev) => ({ ...prev, fuel: false }));
    }
  };

  const fetchSustainabilityScore = async () => {
    setLoading((prev) => ({ ...prev, score: true }));
    try {
      // Use the Smart Dashboard aggregation endpoint as the single source
      const res = await api.get('/dashboard/smart/').catch(() => null);
      // Derive a simple score from alerts: penalize warnings/criticals
      const alerts = res?.data?.alerts ?? {};
      const critical = Object.values(alerts).filter((a: any) => a === 'Critical').length;
      const warning = Object.values(alerts).filter((a: any) => a === 'Warning').length;
      let score = kpiData.sustainabilityScore.value ?? 100;
      score = Math.max(0, Math.min(100, score - critical * 30 - warning * 10));
      setSustainabilityScore({ value: Math.round(score), change: 0 });
      setError((prev) => ({ ...prev, score: "" }));
    } catch (err) {
      console.error("Failed to fetch score:", err);
      setError((prev) => ({ ...prev, score: "Failed to load score" }));
      setSustainabilityScore({ value: 0, change: 0 });
    } finally {
      setLoading((prev) => ({ ...prev, score: false }));
    }
  };

  const fetchActivities = async () => {
    setLoading((prev) => ({ ...prev, activities: true }));
    try {
      // Activities API not available yet; use bundled recent activities as fallback
      setActivities(recentActivities);
      setError((prev) => ({ ...prev, activities: "" }));
    } catch (err) {
      console.error("Failed to fetch activities:", err);
      setError((prev) => ({ ...prev, activities: "Failed to load activities" }));
      setActivities([]);
    } finally {
      setLoading((prev) => ({ ...prev, activities: false }));
    }
  };

  const fetchWorkflowStats = async () => {
    setLoading((prev) => ({ ...prev, workflow: true }));
    try {
      const res = await getWorkflowQueue();
      const workflows = Array.isArray(res.data) ? res.data : ((res.data as any).results || []);
      const pendingCount = workflows.filter(
        (item: any) => item.current_status === "Pending" || item.current_status === "Analyst Review",
      ).length;
      setWorkflowPendingCount(pendingCount);
      setError((prev) => ({ ...prev, workflow: "" }));
    } catch (err) {
      console.error("Failed to fetch workflow stats:", err);
      setError((prev) => ({ ...prev, workflow: "Failed to load workflow stats" }));
      setWorkflowPendingCount(0);
    } finally {
      setLoading((prev) => ({ ...prev, workflow: false }));
    }
  };

  useEffect(() => {
    fetchCarbonData();
    fetchAirQualityData();
    fetchEnergyData();
    fetchFuelData();
    fetchSustainabilityScore();
    fetchActivities();
    fetchWorkflowStats();
  }, []);

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold">Welcome back, {user?.name?.split(" ")[0]}</h1>
        <p className="text-sm text-muted-foreground">Here's your sustainability overview for today</p>
      </div>

      {/* KPI Cards */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
        <KpiCard
          title="Total Carbon Emission"
          value={carbonData.total.toFixed(2)}
          unit="tons"
          change={kpiData.totalCarbon.change}
          icon={Factory}
        />
        <KpiCard
          title="Air Quality Index"
          value={airQualityData.aqi.toFixed(0)}
          unit="AQI"
          change={kpiData.aqi.change}
          icon={Wind}
        />
        <KpiCard
          title="Total Energy Usage"
          value={energyUsage.value}
          unit="kWh"
          change={energyUsage.change}
          icon={Zap}
        />
        <KpiCard
          title="Fuel Consumption"
          value={fuelConsumption.value}
          unit="liters"
          change={fuelConsumption.change}
          icon={Fuel}
        />
        <KpiCard
          title="Pending Approvals"
          value={workflowPendingCount}
          unit="tasks"
          change={0}
          icon={Target}
          iconColor="bg-amber-100"
        />
        <KpiCard
          title="Sustainability Score"
          value={sustainabilityScore.value}
          unit="%"
          change={sustainabilityScore.change}
          icon={Target}
        />
      </div>

      {/* Charts */}
      <div className="grid gap-4 lg:grid-cols-2">
        {/* Carbon */}
        <ChartContainer title="Carbon Emission Trends" loading={loading.carbon} error={error.carbon}>
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={carbonData.trends}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
              <XAxis dataKey="date" tick={{ fontSize: 11 }} stroke="hsl(var(--muted-foreground))" />
              <YAxis tick={{ fontSize: 11 }} stroke="hsl(var(--muted-foreground))" />
              <Tooltip
                contentStyle={{
                  background: "hsl(var(--card))",
                  border: "1px solid hsl(var(--border))",
                  borderRadius: 8,
                  fontSize: 12,
                }}
              />
              <Legend wrapperStyle={{ fontSize: 11 }} />
              <Line type="monotone" dataKey="total" stroke={CHART_COLORS[0]} strokeWidth={2} dot={false} name="Total CO₂e" />
            </LineChart>
          </ResponsiveContainer>
        </ChartContainer>

        {/* AQI */}
        <ChartContainer title="Air Quality Trends (AQI)" loading={loading.aqi} error={error.aqi}>
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={airQualityData.trends}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
              <XAxis dataKey="date" tick={{ fontSize: 11 }} stroke="hsl(var(--muted-foreground))" />
              <YAxis tick={{ fontSize: 11 }} stroke="hsl(var(--muted-foreground))" />
              <Tooltip
                contentStyle={{
                  background: "hsl(var(--card))",
                  border: "1px solid hsl(var(--border))",
                  borderRadius: 8,
                  fontSize: 12,
                }}
              />
              <Legend wrapperStyle={{ fontSize: 11 }} />
              <Line type="monotone" dataKey="AQI" stroke={CHART_COLORS[1]} strokeWidth={2} dot={false} name="AQI" />
            </LineChart>
          </ResponsiveContainer>
        </ChartContainer>
      </div>

      {/* Energy & Fuel Charts */}
      <BarChartContainer title="Energy: Renewable vs Non-Renewable" data={energyData} loading={loading.energy} error={error.energy} />
      <PieChartContainer title="Fuel Distribution" data={fuelData} loading={loading.fuel} error={error.fuel} />
      <RecentActivityTable activities={activities} loading={loading.activities} error={error.activities} />
    </div>
  );
}

/* -----------------------------
   Reusable Components
----------------------------- */
const ChartContainer: React.FC<{ title: string; loading?: boolean; error?: string; children: React.ReactNode }> = ({
  title,
  loading,
  error,
  children,
}) => (
  <div className="chart-container">
    <h3 className="mb-4 text-sm font-semibold">{title}</h3>
    {loading ? <p>Loading...</p> : error ? <p className="text-red-500">{error}</p> : children}
  </div>
);

const BarChartContainer: React.FC<{ title: string; data: any[]; loading?: boolean; error?: string }> = ({ title, data, loading, error }) => (
  <div className="chart-container">
    <h3 className="mb-4 text-sm font-semibold">{title}</h3>
    {loading ? (
      <p>Loading...</p>
    ) : error ? (
      <p className="text-red-500">{error}</p>
    ) : data.length > 0 ? (
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
          <XAxis dataKey="month" tick={{ fontSize: 11 }} stroke="hsl(var(--muted-foreground))" />
          <YAxis tick={{ fontSize: 11 }} stroke="hsl(var(--muted-foreground))" />
          <Tooltip contentStyle={{ background: "hsl(var(--card))", border: "1px solid hsl(var(--border))", borderRadius: 8, fontSize: 12 }} />
          <Legend wrapperStyle={{ fontSize: 11 }} />
          <Bar dataKey="renewable" fill={CHART_COLORS[0]} radius={[4, 4, 0, 0]} name="Renewable" />
          <Bar dataKey="nonRenewable" fill={CHART_COLORS[1]} radius={[4, 4, 0, 0]} name="Non-Renewable" />
        </BarChart>
      </ResponsiveContainer>
    ) : (
      <p className="text-muted-foreground">No data available</p>
    )}
  </div>
);

const PieChartContainer: React.FC<{ title: string; data: any[]; loading?: boolean; error?: string }> = ({ title, data, loading, error }) => (
  <div className="chart-container">
    <h3 className="mb-4 text-sm font-semibold">{title}</h3>
    {loading ? (
      <p>Loading...</p>
    ) : error ? (
      <p className="text-red-500">{error}</p>
    ) : data.length > 0 ? (
      <ResponsiveContainer width="100%" height={220}>
        <PieChart>
          <Pie data={data} cx="50%" cy="50%" innerRadius={50} outerRadius={80} dataKey="value" label={({ name, value }) => `${name} ${value}%`}>
            {data.map((_, i) => (
              <Cell key={i} fill={CHART_COLORS[i % CHART_COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    ) : (
      <p className="text-muted-foreground">No data available</p>
    )}
  </div>
);

const RecentActivityTable: React.FC<{ activities: Activity[]; loading?: boolean; error?: string }> = ({ activities, loading, error }) => (
  <div className="chart-container lg:col-span-2">
    <h3 className="mb-4 text-sm font-semibold">Recent Activity</h3>
    {loading ? (
      <p>Loading...</p>
    ) : error ? (
      <p className="text-red-500">{error}</p>
    ) : activities.length > 0 ? (
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="text-xs">Action</TableHead>
            <TableHead className="text-xs">User</TableHead>
            <TableHead className="text-xs">Time</TableHead>
            <TableHead className="text-xs">Type</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {activities.map((a) => (
            <TableRow key={a.id}>
              <TableCell className="text-xs">{a.action}</TableCell>
              <TableCell className="text-xs">{a.user}</TableCell>
              <TableCell className="text-xs text-muted-foreground">{a.time}</TableCell>
              <TableCell>
                <Badge variant={(activityBadge[a.type] as any) || "secondary"} className="text-[10px]">
                  {a.type}
                </Badge>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    ) : (
      <p className="text-muted-foreground">No activities found</p>
    )}
  </div>
);