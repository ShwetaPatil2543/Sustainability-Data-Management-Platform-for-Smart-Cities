import { useEffect, useState } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Loader2 } from "lucide-react";
import {
  getWorkflowQueue,
  approveWorkflow,
  rejectWorkflow,
  escalateWorkflow,
} from "@/services/api";

interface WorkflowRecord {
  id: number;
  content_type: string;
  object_id: number;
  current_status: string;
  assigned_to: number | null;
}

const getStatusColor = (status: string) => {
  switch (status) {
    case "Pending":
      return "bg-yellow-100 text-yellow-800 border border-yellow-200";
    case "Analyst Review":
      return "bg-sky-100 text-sky-800 border border-sky-200";
    case "Manager Approved":
      return "bg-violet-100 text-violet-800 border border-violet-200";
    case "Supervisor Approved":
      return "bg-emerald-100 text-emerald-800 border border-emerald-200";
    case "Rejected":
      return "bg-rose-100 text-rose-800 border border-rose-200";
    default:
      return "bg-muted/10 text-muted-foreground border border-border";
  }
};

const WorkflowQueue = () => {
  const { user } = useAuth();
  const [workflowItems, setWorkflowItems] = useState<WorkflowRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [actionLoadingId, setActionLoadingId] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadQueue();
  }, []);

  const loadQueue = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await getWorkflowQueue();
      setWorkflowItems(response.data || []);
    } catch (err: any) {
      console.error("Workflow load error:", err);
      setError("Failed to load data");
    } finally {
      setLoading(false);
    }
  };

  const performAction = async (workflowId: number, action: "approve" | "reject" | "escalate") => {
    setActionLoadingId(workflowId);
    setError(null);

    try {
      if (action === "approve") {
        await approveWorkflow(workflowId);
      } else if (action === "reject") {
        await rejectWorkflow(workflowId);
      } else {
        await escalateWorkflow(workflowId);
      }
      alert("Action successful");
      await loadQueue();
    } catch (err: any) {
      console.error(`Workflow ${action} error:`, err);
      setError(`Failed to ${action} workflow. Please refresh and try again.`);
    } finally {
      setActionLoadingId(null);
    }
  };

  const canApprove = (status: string) => {
    if (!user) return false;
    if (user.role === "admin") return status !== "Rejected";
    if (user.role === "analyst") return status === "Pending";
    if (user.role === "manager") return status === "Analyst Review";
    if (user.role === "supervisor") return status === "Manager Approved";
    return false;
  };

  const canReject = (status: string) => {
    if (!user) return false;
    return status !== "Rejected" && user.role !== "data_entry";
  };

  const canEscalate = (status: string) => {
    if (!user) return false;
    return status !== "Rejected" && (user.role === "manager" || user.role === "supervisor" || user.role === "admin");
  };

  return (
    <div className="space-y-6 p-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Workflow Queue</h1>
          <p className="text-sm text-muted-foreground">
            Review pending workflow records and take approval actions based on your role.
          </p>
        </div>
        <Button variant="secondary" onClick={loadQueue} disabled={loading}>
          {loading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : "Refresh Queue"}
        </Button>
      </div>

      {error ? (
        <div className="rounded-md border border-destructive/20 bg-destructive/10 p-4 text-sm text-destructive-foreground">
          {error}
        </div>
      ) : null}

      <div className="overflow-hidden rounded-lg border border-border bg-background shadow-sm">
        {loading ? (
          <div className="p-6 text-center text-sm text-muted-foreground">Loading...</div>
        ) : (
          <Table className="min-w-full text-sm">
            <TableHeader>
              <TableRow>
                <TableHead className="px-3 py-3">Record ID</TableHead>
                <TableHead className="px-3 py-3">Type</TableHead>
                <TableHead className="px-3 py-3">Status</TableHead>
                <TableHead className="px-3 py-3">Assigned To</TableHead>
                <TableHead className="px-3 py-3">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {workflowItems.map((item) => (
                <TableRow key={item.id} className="transition-colors hover:bg-muted/50">
                  <TableCell className="px-3 py-3">{item.object_id}</TableCell>
                  <TableCell className="px-3 py-3 capitalize">{item.content_type.replace(/_/g, " ")}</TableCell>
                  <TableCell className="px-3 py-3">
                    <span
                      className={`inline-flex items-center rounded-full px-2 py-1 text-sm font-medium ${getStatusColor(
                        item.current_status,
                      )}`}
                    >
                      {item.current_status}
                    </span>
                  </TableCell>
                  <TableCell className="px-3 py-3">
                    {item.assigned_to ?? "Unassigned"}
                  </TableCell>
                  <TableCell className="px-3 py-3">
                    <div className="flex flex-wrap gap-2">
                    {canApprove(item.current_status) ? (
                      <Button
                        size="sm"
                        onClick={() => performAction(item.id, "approve")}
                        disabled={actionLoadingId === item.id}
                      >
                        {actionLoadingId === item.id ? (
                          <Loader2 className="h-4 w-4 animate-spin" />
                        ) : (
                          "Approve"
                        )}
                      </Button>
                    ) : null}
                    {canReject(item.current_status) ? (
                      <Button
                        size="sm"
                        variant="destructive"
                        onClick={() => performAction(item.id, "reject")}
                        disabled={actionLoadingId === item.id}
                      >
                        {actionLoadingId === item.id ? (
                          <Loader2 className="h-4 w-4 animate-spin" />
                        ) : (
                          "Reject"
                        )}
                      </Button>
                    ) : null}
                    {canEscalate(item.current_status) ? (
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => performAction(item.id, "escalate")}
                        disabled={actionLoadingId === item.id}
                      >
                        {actionLoadingId === item.id ? (
                          <Loader2 className="h-4 w-4 animate-spin" />
                        ) : (
                          "Escalate"
                        )}
                      </Button>
                    ) : null}
                    {!canApprove(item.current_status) && !canReject(item.current_status) && !canEscalate(item.current_status) ? (
                      <span className="text-sm text-muted-foreground">No actions available</span>
                    ) : null}
                  </div>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
          </Table>
        )}

        {!loading && workflowItems.length === 0 ? (
          <div className="px-6 py-10 text-center text-sm text-muted-foreground">
            No workflow tasks available
          </div>
        ) : null}
      </div>
    </div>
  );
};

export const getWorkflowPendingApprovalCount = async (): Promise<number> => {
  const response = await getWorkflowQueue();
  const records = response.data || [];
  return records.filter((item: WorkflowRecord) => item.current_status !== "Rejected").length;
};

export default WorkflowQueue;
