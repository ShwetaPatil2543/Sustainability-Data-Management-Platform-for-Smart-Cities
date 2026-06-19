import { useState, useEffect, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import * as XLSX from "xlsx";
import { toast } from "@/components/ui/use-toast";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts";
import { Droplets, Cloud, Wind, AlertTriangle, Upload } from "lucide-react";
import api from "@/services/api"; // Axios instance with auth headers

interface AirQualityData {
  id?: number;
  date: string;
  aqi: number;
  pm25: number;
  pm10: number;
  co2?: number;
  no2?: number;
  so2?: number;
  temperature?: number;
  humidity?: number;
  industry?: string;
  department?: string;
}

export default function AirQualityDashboard() {
  const [file, setFile] = useState<File | null>(null);
  const [previewData, setPreviewData] = useState<AirQualityData[]>([]);
  const [chartData, setChartData] = useState<AirQualityData[]>([]);
  const [loading, setLoading] = useState(false);

  // -------------------------------
  // Dropzone
  // -------------------------------
  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0]);
      readFilePreview(acceptedFiles[0]);
    }
  }, []);

  const { getRootProps, getInputProps } = useDropzone({ onDrop });

  // -------------------------------
  // Read file preview (first 10 rows)
  // -------------------------------
  const readFilePreview = (file: File) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const data = e.target?.result;
      const workbook = XLSX.read(data, { type: "binary" });
      const sheetName = workbook.SheetNames[0];
      const sheet = workbook.Sheets[sheetName];
      const jsonData: AirQualityData[] = XLSX.utils.sheet_to_json(sheet, { defval: "" });
      setPreviewData(jsonData.slice(0, 10));
      setChartData(jsonData); // full data for chart
    };
    reader.readAsBinaryString(file);
  };

  // -------------------------------
  // Upload file to backend
  // -------------------------------
  const uploadFile = async () => {
    if (!file) return toast({ title: "No file selected" });

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
     const res = await api.post("/air-quality/air-quality/upload/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
      toast({ title: "Upload successful", description: `Created: ${res.data.created}, Updated: ${res.data.updated}` });
      setLoading(false);
      setFile(null);
      setPreviewData([]);
    } catch (err: any) {
      setLoading(false);
      toast({ title: "Upload failed", description: err.response?.data?.error || err.message });
    }
  };

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">Air Quality Dashboard</h1>

      {/* Upload Card */}
      <div {...getRootProps()} className="border-2 border-dashed p-6 rounded-lg cursor-pointer hover:border-blue-500">
        <input {...getInputProps()} />
        <div className="flex flex-col items-center justify-center text-gray-500">
          <Upload className="w-12 h-12 mb-2" />
          <p>{file ? file.name : "Drag & drop file here, or click to select"}</p>
        </div>
      </div>

      <button
        onClick={uploadFile}
        className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
        disabled={!file || loading}
      >
        {loading ? "Uploading..." : "Upload"}
      </button>

      {/* Preview Table */}
      {previewData.length > 0 && (
        <div className="overflow-x-auto border rounded p-4">
          <h2 className="font-semibold mb-2">Preview (first 10 rows)</h2>
          <table className="w-full table-auto border-collapse border">
            <thead>
              <tr>
                {Object.keys(previewData[0]).map((key) => (
                  <th key={key} className="border px-2 py-1">{key}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {previewData.map((row, idx) => (
                <tr key={idx}>
                  {Object.keys(row).map((key) => (
                    <td key={key} className="border px-2 py-1">{row[key]}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* AQI Trend Chart */}
      {chartData.length > 0 && (
        <div className="p-4 border rounded">
          <h2 className="font-semibold mb-2">AQI Trend</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="aqi" stroke="#1E40AF" />
              <Line type="monotone" dataKey="pm25" stroke="#047857" />
              <Line type="monotone" dataKey="pm10" stroke="#DC2626" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}