import { emissionTrends, energyData } from "@/data/mockData";
import { Button } from "@/components/ui/button";
import { FileText, FileSpreadsheet } from "lucide-react";
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend
} from "recharts";

import api from "@/services/api";

export default function Reports() {

  const handleDownload = async (type: "PDF" | "CSV") => {

    try {

      const endpoint =
        type === "PDF"
          ? "/reports/pdf/"
          : "/reports/csv/";

      const response = await api.get(endpoint, {
        responseType: "blob"
      });

      const blob = new Blob([response.data]);

      const url = window.URL.createObjectURL(blob);

      const link = document.createElement("a");
      link.href = url;

      link.download =
        type === "PDF"
          ? "sustainability-report.pdf"
          : "sustainability-report.csv";

      document.body.appendChild(link);

      link.click();

      link.remove();

      window.URL.revokeObjectURL(url);

    } catch (error) {

      console.error("Download failed:", error);

      alert("Unable to download report. Check backend server.");

    }

  };

  return (

    <div className="space-y-6 animate-fade-in">

      {/* HEADER */}

      <div className="flex items-center justify-between">

        <div>
          <h1 className="text-2xl font-bold">
            Reports & Analytics
          </h1>

          <p className="text-sm text-muted-foreground">
            Generate and download sustainability reports
          </p>
        </div>

        <div className="flex gap-2">

          <Button
            variant="outline"
            onClick={() => handleDownload("PDF")}
          >
            <FileText className="mr-2 h-4 w-4" />
            Download PDF
          </Button>

          <Button
            variant="outline"
            onClick={() => handleDownload("CSV")}
          >
            <FileSpreadsheet className="mr-2 h-4 w-4" />
            Download CSV
          </Button>

        </div>

      </div>

      {/* CHARTS */}

      <div className="grid gap-4 lg:grid-cols-2">

        {/* LINE CHART */}

        <div className="chart-container">

          <h3 className="mb-4 text-sm font-semibold">
            Sustainability Performance
          </h3>

          <ResponsiveContainer width="100%" height={300}>

            <LineChart data={emissionTrends}>

              <CartesianGrid strokeDasharray="3 3" />

              <XAxis dataKey="month" />

              <YAxis />

              <Tooltip />

              <Legend />

              <Line
                type="monotone"
                dataKey="co2"
                stroke="#16a34a"
                strokeWidth={2}
                name="CO₂"
              />

              <Line
                type="monotone"
                dataKey="ch4"
                stroke="#0284c7"
                strokeWidth={2}
                name="CH₄"
              />

            </LineChart>

          </ResponsiveContainer>

        </div>

        {/* BAR CHART */}

        <div className="chart-container">

          <h3 className="mb-4 text-sm font-semibold">
            Energy Consumption Comparison
          </h3>

          <ResponsiveContainer width="100%" height={300}>

            <BarChart data={energyData.slice(0, 6)}>

              <CartesianGrid strokeDasharray="3 3" />

              <XAxis dataKey="month" />

              <YAxis />

              <Tooltip />

              <Legend />

              <Bar
                dataKey="renewable"
                fill="#16a34a"
                name="Renewable"
              />

              <Bar
                dataKey="nonRenewable"
                fill="#f59e0b"
                name="Non-Renewable"
              />

            </BarChart>

          </ResponsiveContainer>

        </div>

      </div>

    </div>

  );

}