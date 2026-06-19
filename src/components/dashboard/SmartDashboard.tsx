import React, { useEffect, useState } from 'react';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { KpiCard } from './KpiCard';
import api from '@/services/api';

interface PredictionItem { date: string; prediction: number }

export default function SmartDashboard() {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    let mounted = true;
    const fetchData = async () => {
      try {
        const res = await api.get('/dashboard/smart/');
        if (!mounted) return;
        setData(res.data);
      } catch (err) {
        console.error('Failed to load smart dashboard', err);
      } finally {
        if (mounted) setLoading(false);
      }
    };
    fetchData();
    return () => { mounted = false; };
  }, []);

  if (loading) return <div className="p-6">Loading Smart Dashboard...</div>;
  if (!data) return <div className="p-6">No data available.</div>;

  const emissionChart = data.emission_chart || [];
  const predictions: PredictionItem[] = (data.prediction?.carbon_emissions || []).map((p: any) => ({ date: p.date, prediction: p.prediction }));
  const industryComparison = data.industry_comparison || [];
  const recommendations = data.recommendations || [];

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <KpiCard title="Total Emissions" value={data.total_emission || 0} unit="kg CO₂e" change={-5} icon={() => <></>} />
        <KpiCard title="Current Alerts" value={Object.keys(data.alerts || {}).length} unit="" change={10} icon={() => <></>} />
        <KpiCard title="Highest Industry" value={industryComparison[0]?.industry || 'N/A'} unit="" change={0} icon={() => <></>} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card p-4">
          <h3 className="mb-2 text-sm font-medium">Emission Trend (last 30 days)</h3>
          <ResponsiveContainer width="100%" height={240}>
            <LineChart data={emissionChart} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="value" stroke="#6366f1" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="card p-4">
          <h3 className="mb-2 text-sm font-medium">7-day Prediction (Carbon)</h3>
          <ResponsiveContainer width="100%" height={240}>
            <LineChart data={predictions} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="prediction" stroke="#10b981" strokeWidth={2} dot={{ r: 3 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card p-4">
          <h3 className="mb-2 text-sm font-medium">Industry Comparison</h3>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={industryComparison} layout="vertical" margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis dataKey="industry" type="category" />
              <Tooltip />
              <Bar dataKey="value" fill="#ef4444" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="card p-4">
          <h3 className="mb-2 text-sm font-medium">AI Recommendations</h3>
          <div className="space-y-3">
            {recommendations.map((r: any, idx: number) => (
              <div key={idx} className="p-3 border rounded">
                <div className="text-xs font-semibold">{r.category}</div>
                <div className="text-sm mt-1">{r.recommendation || r.action}</div>
                <div className="text-xs text-muted-foreground mt-1">Impact: {r.impact}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
