import { useAuth } from "@/contexts/AuthContext";
import { useTheme } from "@/contexts/ThemeContext";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Badge } from "@/components/ui/badge";

export default function SettingsPage() {
  const { user } = useAuth();
  const { theme, toggleTheme } = useTheme();

  return (
    <div className="mx-auto max-w-2xl space-y-8 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold">Settings</h1>
        <p className="text-sm text-muted-foreground">Manage your account and preferences</p>
      </div>

      <div className="chart-container space-y-4">
        <h3 className="text-sm font-semibold">Profile</h3>
        <div className="grid gap-4 sm:grid-cols-2">
          <div className="space-y-1.5">
            <Label>Name</Label>
            <Input defaultValue={user?.name} />
          </div>
          <div className="space-y-1.5">
            <Label>Email</Label>
            <Input defaultValue={user?.email} disabled />
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Label>Role</Label>
          <Badge variant="secondary" className="capitalize">{user?.role}</Badge>
        </div>
        <Button>Save Changes</Button>
      </div>

      <div className="chart-container space-y-4">
        <h3 className="text-sm font-semibold">Appearance</h3>
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm">Dark Mode</p>
            <p className="text-xs text-muted-foreground">Toggle dark/light theme</p>
          </div>
          <Switch checked={theme === "dark"} onCheckedChange={toggleTheme} />
        </div>
      </div>

      <div className="chart-container space-y-4">
        <h3 className="text-sm font-semibold">Notifications</h3>
        {["Email alerts", "AQI threshold warnings", "Monthly report digest"].map((n) => (
          <div key={n} className="flex items-center justify-between">
            <span className="text-sm">{n}</span>
            <Switch defaultChecked />
          </div>
        ))}
      </div>
    </div>
  );
}
