import { useEffect, useState } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import { Plus, Pencil, Trash2, Search, Loader2 } from "lucide-react";
import * as XLSX from "xlsx";

import {
  getCarbonEmissions,
  addCarbonEmission,
  updateCarbonEmission,
  deleteCarbonEmission,
  bulkUploadEmissions,
} from "@/services/api";
import api from "@/services/api";

/* ---------------- TYPES ---------------- */
interface Industry {
  id: number;
  name: string;
}

interface CarbonEmissionRecord {
  id: number;
  industry: number;
  industry_name?: string;
  date: string;
  co2_emission: number;
  methane_emission: number;
  nitrous_emission?: number;
  total_emission?: number;
}

interface FormData {
  industry: number | "";
  date: string;
  co2_emission: string;
  methane_emission: string;
  nitrous_emission: string;
}

/* ---------------- COMPONENT ---------------- */
export default function CarbonEmission() {
  const { user } = useAuth();
  const canModify = user?.role !== "analyst";

  const [records, setRecords] = useState<CarbonEmissionRecord[]>([]);
  const [industries, setIndustries] = useState<Industry[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [unitFilter, setUnitFilter] = useState("all");

  const [openAdd, setOpenAdd] = useState(false);
  const [editData, setEditData] = useState<CarbonEmissionRecord | null>(null);

  const [formData, setFormData] = useState<FormData>({
    industry: "",
    date: "",
    co2_emission: "",
    methane_emission: "",
    nitrous_emission: "",
  });

  // NEW STATE for selected industry for bulk upload
  const [selectedIndustry, setSelectedIndustry] = useState<Industry | null>(null);

  /* ---------------- LOAD DATA ---------------- */
  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const emissionsRes = await getCarbonEmissions();
      const industriesRes = await api.get("/industries/");
      console.debug("API: fetched emissions", emissionsRes?.data?.length ?? 0);
      console.debug("API: fetched industries", industriesRes?.data?.length ?? 0);
      // Normalize records: ensure total_emission exists and nitrous_emission is present
      const normalized = (emissionsRes.data || []).map((r: any) => ({
        ...r,
        nitrous_emission: r.nitrous_emission ?? r.nitrous_oxide ?? 0,
        total_emission:
          r.total_emission ??
          ((r.co2_emission || 0) + (r.methane_emission || 0) + (r.nitrous_emission ?? r.nitrous_oxide ?? 0)),
      }));
      setRecords(normalized);
      setIndustries(industriesRes.data);
    } catch (err: any) {
      // Log useful debugging info: status, statusText, and response body when available
      if (err?.response) {
        console.error(
          "API ERROR:",
          err.response.status,
          err.response.statusText,
          err.response.data
        );
      } else if (err?.request) {
        console.error("API ERROR: no response received", err.request);
      } else {
        console.error("API ERROR:", err.message || err);
      }
    }
    setLoading(false);
  };

  /* ---------------- FORM CHANGE ---------------- */
  const handleChange = (e: any) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  /* ---------------- ADD ENTRY ---------------- */
  const handleSave = async () => {
    if (!formData.industry || !formData.date) {
      alert("Please select industry and date.");
      return;
    }
    try {
      const payload = {
        industry: Number(formData.industry),
        date: formData.date,
        co2_emission: Number(formData.co2_emission) || 0,
        methane_emission: Number(formData.methane_emission) || 0,
        nitrous_emission: Number(formData.nitrous_emission) || 0,
      };
      const res = await addCarbonEmission(payload);
      setRecords([res.data, ...records]);
      setOpenAdd(false);
      setFormData({ industry: "", date: "", co2_emission: "", methane_emission: "", nitrous_emission: "" });
    } catch (err) {
      console.error("Add failed:", err);
      alert("Add failed. Check console for details.");
    }
  };

  /* ---------------- EDIT ENTRY ---------------- */
  const handleUpdate = async () => {
    if (!editData) return;
    try {
      const payload = {
        industry: editData.industry,
        date: editData.date,
        co2_emission: Number(editData.co2_emission) || 0,
        methane_emission: Number(editData.methane_emission) || 0,
        nitrous_emission: Number(editData.nitrous_emission) || 0,
      };
      const res = await updateCarbonEmission(editData.id, payload);
      setRecords(records.map((r) => (r.id === editData.id ? res.data : r)));
      setEditData(null);
    } catch (err) {
      console.error("Update failed:", err);
      alert("Update failed. Check console.");
    }
  };

  /* ---------------- DELETE ---------------- */
  const handleDelete = async (id: number) => {
    if (!window.confirm("Delete this record?")) return;
    try {
      await deleteCarbonEmission(id);
      setRecords(records.filter((r) => r.id !== id));
    } catch (err) {
      console.error("Delete failed:", err);
      alert("Delete failed.");
    }
  };

  /* ---------------- BULK UPLOAD ---------------- */
  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!selectedIndustry) {
      alert("Please select an industry before uploading!");
      return;
    }

    try {
      const data = await file.arrayBuffer();
      // Read workbook with cellDates so date cells become JS Date when possible
      const workbook = XLSX.read(data, { cellDates: true });
      const sheet = workbook.Sheets[workbook.SheetNames[0]];
      const jsonData: any[] = XLSX.utils.sheet_to_json(sheet, { defval: null });

      const findKey = (row: any, candidates: string[]) => {
        const keys = Object.keys(row || {});
        for (const c of candidates) {
          const k = keys.find((kk) => kk.toLowerCase() === c.toLowerCase());
          if (k) return row[k];
        }
        return null;
      };

      const excelSerialToDate = (v: number) => {
        // Excel serial to JS Date (assuming 1900-based serial)
        const epoch = Date.UTC(1899, 11, 30);
        const ms = Math.round((v) * 86400 * 1000);
        return new Date(epoch + ms);
      };

      const payload = jsonData.map((row) => {
        const rawDate = findKey(row, ["Date", "date"]);
        let dateStr = null as string | null;
        if (rawDate instanceof Date) {
          dateStr = rawDate.toISOString().slice(0, 10);
        } else if (typeof rawDate === "number") {
          try {
            dateStr = excelSerialToDate(rawDate).toISOString().slice(0, 10);
          } catch {
            dateStr = String(rawDate);
          }
        } else if (rawDate != null) {
          dateStr = String(rawDate).split("T")[0];
        }

        const co2Raw = findKey(row, ["CO2", "co2", "co2_emission"]);
        const methaneRaw = findKey(row, ["Methane", "methane", "methane_emission"]);
        const nitrousRaw = findKey(row, ["Nitrous", "nitrous", "nitrous_emission"]);

        const parseNumber = (v: any) => {
          if (v == null || v === "") return 0;
          if (typeof v === "number") return v;
          // remove commas and other non-numeric chars
          const n = Number(String(v).replace(/[^0-9.-]+/g, ""));
          return isNaN(n) ? 0 : n;
        };

        return {
          industry: selectedIndustry.id,
          date: dateStr,
          co2_emission: parseNumber(co2Raw),
          methane_emission: parseNumber(methaneRaw),
          nitrous_emission: parseNumber(nitrousRaw),
        };
      });

      console.debug("Bulk upload payload:", payload);

      // use the helper which relies on the API baseURL and interceptor
      const res = await bulkUploadEmissions(payload);
      console.debug("Bulk upload response status:", res.status);
      console.debug("Bulk upload response data:", res.data);

      // Backend returns { created: n, errors?: [...] } or 201
      const created = res.data?.created ?? (res.status === 201 ? payload.length : 0);
      if (created && created > 0) {
        alert(`Upload Successful — created ${created} records`);
        // reload latest records from server
        await loadData();
      } else {
        console.warn("Upload completed but no records reported created:", res.data);
        alert("Upload completed; check console for details.");
      }
    } catch (err: any) {
      console.error("UPLOAD ERROR:", err.response?.data || err.message);
      alert("Upload failed. Check console for details.");
    }
  };

  /* ---------------- FILTER & CHART ---------------- */
  const filteredRecords = records.filter((r) => {
    const name = r.industry_name || "";
    return name.toLowerCase().includes(search.toLowerCase()) && (unitFilter === "all" || name === unitFilter);
  });

  const chartData = [...records].reverse().map((r) => ({ date: r.date, total: r.total_emission }));

  if (loading)
    return (
      <div className="flex h-screen items-center justify-center">
        <Loader2 className="animate-spin" />
      </div>
    );

  return (
    <div className="p-6 space-y-6">
      {/* HEADER */}
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Carbon Emissions</h1>
        {canModify && (
          <div className="flex gap-2 items-center">
            <Button onClick={() => setOpenAdd(true)}>
              <Plus className="mr-2 h-4 w-4" /> Add Entry
            </Button>

            {/* SELECT INDUSTRY FOR BULK UPLOAD */}
            <Select
              value={selectedIndustry ? String(selectedIndustry.id) : ""}
              onValueChange={(v: string) =>
                setSelectedIndustry(industries.find((i) => i.id === Number(v)) || null)
              }
            >
              <SelectTrigger>
                <SelectValue placeholder="Select Industry for Upload" />
              </SelectTrigger>
              <SelectContent>
                {industries.map((i) => (
                  <SelectItem key={i.id} value={String(i.id)}>
                    {i.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            <input type="file" accept=".xlsx,.xls,.csv" onChange={handleFileUpload} />
          </div>
        )}
      </div>

      {/* CHART */}
      <div className="h-64 border rounded-xl p-4">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="total" stroke="#10b981" strokeWidth={2} name="Total CO2e" />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* SEARCH */}
      <div className="flex gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4" />
          <Input
            className="pl-10"
            placeholder="Search industry..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
      </div>

      {/* TABLE */}
      <div className="border rounded-lg">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Date</TableHead>
              <TableHead>Industry</TableHead>
              <TableHead>CO2</TableHead>
              <TableHead>Methane</TableHead>
              <TableHead>Nitrous</TableHead>
              <TableHead>Total</TableHead>
              {canModify && <TableHead />}
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredRecords.map((r) => (
              <TableRow key={r.id}>
                <TableCell>{r.date}</TableCell>
                <TableCell>{r.industry_name}</TableCell>
                <TableCell>{r.co2_emission}</TableCell>
                <TableCell>{r.methane_emission}</TableCell>
                <TableCell>{r.nitrous_emission}</TableCell>
                <TableCell className="font-bold text-emerald-600">{r.total_emission}</TableCell>
                {canModify && (
                  <TableCell className="flex gap-2">
                    <Button size="icon" variant="ghost" onClick={() => setEditData(r)}>
                      <Pencil className="h-4 w-4" />
                    </Button>
                    {user?.role === "admin" && (
                      <Button size="icon" variant="ghost" onClick={() => handleDelete(r.id)}>
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    )}
                  </TableCell>
                )}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      {/* ADD DIALOG */}
      <Dialog open={openAdd} onOpenChange={setOpenAdd}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Add Carbon Emission</DialogTitle>
          </DialogHeader>
          <Select
            value={String(formData.industry)}
            onValueChange={(v) => setFormData({ ...formData, industry: Number(v) })}
          >
            <SelectTrigger>
              <SelectValue placeholder="Select Industry" />
            </SelectTrigger>
            <SelectContent>
              {industries.map((i) => (
                <SelectItem key={i.id} value={String(i.id)}>
                  {i.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Input type="date" name="date" value={formData.date} onChange={handleChange} />
          <Input placeholder="CO2" name="co2_emission" value={formData.co2_emission} onChange={handleChange} />
          <Input placeholder="Methane" name="methane_emission" value={formData.methane_emission} onChange={handleChange} />
          <Input placeholder="Nitrous" name="nitrous_emission" value={formData.nitrous_emission} onChange={handleChange} />
          <DialogFooter>
            <Button onClick={handleSave}>Save</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* EDIT DIALOG */}
      <Dialog open={!!editData} onOpenChange={() => setEditData(null)}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Edit Entry</DialogTitle>
          </DialogHeader>
          <Select
            value={String(editData?.industry)}
            onValueChange={(v) => setEditData({ ...editData!, industry: Number(v) })}
          >
            <SelectTrigger>
              <SelectValue placeholder="Select Industry" />
            </SelectTrigger>
            <SelectContent>
              {industries.map((i) => (
                <SelectItem key={i.id} value={String(i.id)}>
                  {i.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Input type="date" value={editData?.date} onChange={(e) => setEditData({ ...editData!, date: e.target.value })} />
          <Input value={editData?.co2_emission} onChange={(e) => setEditData({ ...editData!, co2_emission: Number(e.target.value) })} />
          <Input value={editData?.methane_emission} onChange={(e) => setEditData({ ...editData!, methane_emission: Number(e.target.value) })} />
          <Input value={editData?.nitrous_emission} onChange={(e) => setEditData({ ...editData!, nitrous_emission: Number(e.target.value) })} />
          <DialogFooter>
            <Button onClick={handleUpdate}>Update</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}