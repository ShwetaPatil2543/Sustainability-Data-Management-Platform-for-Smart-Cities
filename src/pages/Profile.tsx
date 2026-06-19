import { useState } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { toast } from "@/hooks/use-toast";

export default function Profile() {
  const { user, updateUser } = useAuth();
  const [name, setName] = useState(user?.name ?? "");

  const handleSave = () => {
    if (!user) {
      toast({ title: "Unable to save profile", description: "No user is currently signed in." });
      return;
    }

    updateUser({ name });
    toast({ title: "Profile saved", description: "Your profile information has been updated." });
  };

  return (
    <div className="mx-auto max-w-2xl space-y-8 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold">Profile</h1>
        <p className="text-sm text-muted-foreground">Review and update your account information.</p>
      </div>

      <div className="chart-container space-y-4">
        <h3 className="text-sm font-semibold">Account details</h3>
        <div className="grid gap-4 sm:grid-cols-2">
          <div className="space-y-1.5">
            <Label htmlFor="profile-name">Name</Label>
            <Input id="profile-name" value={name} onChange={(event) => setName(event.target.value)} />
          </div>
          <div className="space-y-1.5">
            <Label htmlFor="profile-email">Email</Label>
            <Input id="profile-email" defaultValue={user?.email} disabled />
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Label>Role</Label>
          <Badge variant="secondary" className="capitalize">{user?.role}</Badge>
        </div>
        <Button type="button" onClick={handleSave}>Save Changes</Button>
      </div>

      <div className="chart-container space-y-4">
        <h3 className="text-sm font-semibold">Security</h3>
        <p className="text-sm text-muted-foreground">Change your password, review login activity, and keep your account secure.</p>
      </div>
    </div>
  );
}
