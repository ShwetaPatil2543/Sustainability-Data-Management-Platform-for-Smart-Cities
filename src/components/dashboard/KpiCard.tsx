import { LucideIcon, TrendingDown, TrendingUp } from "lucide-react";
import { cn } from "@/lib/utils";

interface KpiCardProps {
  title: string;
  value: string | number;
  unit: string;
  change: number;
  icon: LucideIcon;
  iconColor?: string;
}

export function KpiCard({ title, value, unit, change, icon: Icon, iconColor }: KpiCardProps) {
  const isPositive = change > 0;
  const isGood = title.includes("Sustainability") ? isPositive : !isPositive;

  return (
    <div className="kpi-card animate-fade-in">
      <div className="flex items-start justify-between">
        <div className="space-y-1.5">
          <p className="text-xs font-medium text-muted-foreground">{title}</p>
          <div className="flex items-baseline gap-1.5">
            <span className="text-2xl font-bold text-card-foreground">
              {typeof value === "number" ? value.toLocaleString() : value}
            </span>
            <span className="text-xs text-muted-foreground">{unit}</span>
          </div>
        </div>
        <div className={cn("flex h-10 w-10 items-center justify-center rounded-lg", iconColor || "bg-primary/10")}>
          <Icon className={cn("h-5 w-5", iconColor ? "text-card-foreground" : "text-primary")} />
        </div>
      </div>
      <div className="mt-3 flex items-center gap-1">
        {isGood ? (
          <TrendingUp className="h-3.5 w-3.5 text-success" />
        ) : (
          <TrendingDown className="h-3.5 w-3.5 text-destructive" />
        )}
        <span className={cn("text-xs font-medium", isGood ? "text-success" : "text-destructive")}>
          {Math.abs(change)}%
        </span>
        <span className="text-xs text-muted-foreground">vs last month</span>
      </div>
    </div>
  );
}
