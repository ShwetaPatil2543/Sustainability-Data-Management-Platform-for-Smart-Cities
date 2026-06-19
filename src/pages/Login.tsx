
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Leaf, AlertCircle } from "lucide-react";

export default function Login() {

  const { login } = useAuth();
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {

    e.preventDefault();
    setError("");
    setLoading(true);

    try {

      // login from AuthContext
      await login(username, password);

      // go to dashboard
      navigate("/dashboard");

    } catch (err) {

      console.error(err);
      setError("Invalid username or password");

    } finally {

      setLoading(false);

    }

  };

  return (
    <div className="flex min-h-screen">

      {/* LEFT SIDE */}
      <div className="hidden w-1/2 items-center justify-center gradient-bg lg:flex">
        <div className="max-w-md space-y-6 px-8 text-center">

          <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-primary-foreground/20 backdrop-blur-sm">
            <Leaf className="h-8 w-8 text-primary-foreground" />
          </div>

          <h1 className="text-3xl font-bold text-primary-foreground">
            Sustainability Data Monitoring Platform
          </h1>

          <p className="text-primary-foreground/80">
            Monitor carbon emissions, air quality, energy usage,
            and fuel consumption with AI-powered insights.
          </p>

        </div>
      </div>

      {/* RIGHT SIDE */}
      <div className="flex w-full items-center justify-center bg-background px-6 lg:w-1/2">

        <div className="w-full max-w-sm space-y-6">

          <div>
            <h2 className="text-2xl font-bold">Welcome back</h2>
            <p className="text-sm text-muted-foreground">
              Sign in to your SDMP account
            </p>
          </div>

          {error && (
            <div className="flex items-center gap-2 rounded-lg bg-red-100 px-3 py-2 text-sm text-red-600">
              <AlertCircle className="h-4 w-4" />
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">

            <div>
              <Label>Username</Label>
              <Input
                type="text"
                placeholder="admin"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>

            <div>
              <Label>Password</Label>
              <Input
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            <Button
              type="submit"
              className="w-full"
              disabled={loading}
            >
              {loading ? "Signing in..." : "Sign In"}
            </Button>

          </form>

          <p className="text-center text-xs text-muted-foreground">
            Don't have an account?{" "}
            <Link
              to="/register"
              className="text-primary hover:underline"
            >
              Register
            </Link>
          </p>

          {/* DEMO USERS */}
          <div className="rounded-lg border bg-muted/50 p-3 text-xs">

            <p className="font-medium mb-1">
              Demo Accounts
            </p>

            <p>admin / admin123</p>
            <p>manager / manager123</p>
            <p>analyst / analyst123</p>

          </div>

        </div>
      </div>

    </div>
  );
}

